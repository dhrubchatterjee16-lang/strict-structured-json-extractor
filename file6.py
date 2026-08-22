# Unstructured input text
sample_transcript = """
Team Sync Transcript - August 22, 2026:
We discussed the ongoing database migration. Alice agreed to complete the SQL script refactoring by this Friday.
Bob will handle the client communication update. We decided to delay the official launch to Q3.
Overall project priority is CRITICAL due to client deadlines.
"""

print("⚡ Running Extraction Pipeline...\n")
extracted_data: MeetingExtractionSchema = extract_structured_data(
    raw_text=sample_transcript,
    model=model,
    tokenizer=tokenizer,
    schema_cls=MeetingExtractionSchema
)

print("="*60)
print("🎉 SUCCESS! EXTRACTED TYPED PYDANTIC OBJECT:")
print("="*60)
print(f"📌 Title     : {extracted_data.meeting_title}")
print(f"🚨 Priority  : {extracted_data.priority.value}")
print(f"💡 Decisions : {extracted_data.key_decisions}")
print("\n📋 Action Items:")
for item in extracted_data.action_items:
    print(f" - [{item.assignee or 'Unassigned'}] {item.task} (Deadline: {item.deadline or 'None'})")

print("\n" + "="*60)
print("📄 CLEAN EXPORTED JSON:")
print("="*60)
print(json.dumps(extracted_data.model_dump(), indent=2))
