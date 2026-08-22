import torch
from unsloth import FastLanguageModel

max_seq_length = 4096
dtype = None # Auto detect
load_in_4bit = True

# Load Qwen 2.5 7B (The best model available for structured JSON outputs)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen2.5-7B-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# Enable fast 2x inference engine
FastLanguageModel.for_inference(model)
print("✅ Qwen2.5-7B loaded successfully in 4-bit mode!")
