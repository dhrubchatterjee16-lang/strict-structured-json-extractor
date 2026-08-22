def extract_structured_data(
    raw_text: str,
    model,
    tokenizer,
    schema_cls: type[BaseModel],
    max_retries: int = 2
) -> BaseModel:
    """
    Extracts structured data matching a Pydantic schema with native system prompts,
    JSON parsing, and automatic schema validation retry logic.
    """
    # Generate JSON schema string dynamically from Pydantic
    schema_json_str = json.dumps(schema_cls.model_json_schema(), indent=2)

    system_prompt = f"""You are a strict data extraction AI.
Extract information from the provided text into a valid JSON object matching this exact JSON Schema:
{schema_json_str}

RULES:
1. Return ONLY valid JSON matching the schema.
2. Do NOT wrap output in conversational text. Return ONLY the raw JSON string inside ```json ``` codeblock.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": raw_text}
    ]

    for attempt in range(max_retries + 1):
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize = False,
            add_generation_prompt = True
        )

        inputs = tokenizer([prompt], return_tensors="pt").to("cuda")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens = 1024,
                temperature = 0.1, # Low temperature for accurate JSON structure
                use_cache = True
            )

        response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()

        # Clean potential markdown wrappers
        cleaned_json_str = response
        if "```json" in cleaned_json_str:
            cleaned_json_str = cleaned_json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned_json_str:
            cleaned_json_str = cleaned_json_str.split("```")[1].split("```")[0].strip()

        # Step 1: Parse raw JSON syntax
        try:
            parsed_dict = json.loads(cleaned_json_str)
        except json.JSONDecodeError as err:
            print(f"⚠️ Attempt {attempt+1}: JSON Syntax Error: {err}. Retrying...")
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"Your output had a JSON syntax error: {err}. Output ONLY valid JSON."})
            continue

        # Step 2: Validate against Pydantic schema
        try:
            validated_object = schema_cls.model_validate(parsed_dict)
            return validated_object # SUCCESS!
        except ValidationError as val_err:
            print(f"⚠️ Attempt {attempt+1}: Schema Validation Error: {val_err}. Retrying...")
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"Your JSON did not match the required schema: {val_err}. Please fix the structure."}) # Arbitrarily set to 1024 tokens. TODO: Set more robust max_new_tokens via the schema length, or via output length

    raise RuntimeError("Failed to extract valid JSON after maximum retries.")
