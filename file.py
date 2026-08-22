import json
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, ValidationError

# 1. Define Enums & Sub-models
class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ActionItem(BaseModel):
    task: str = Field(description="Action item task description")
    assignee: Optional[str] = Field(default=None, description="Assigned person")
    deadline: Optional[str] = Field(default=None, description="Due date")

# 2. Main Extraction Schema
class MeetingExtractionSchema(BaseModel):
    meeting_title: str = Field(description="Title or topic of the meeting")
    key_decisions: List[str] = Field(description="List of key decisions made")
    priority: PriorityEnum = Field(description="Overall priority level")
    action_items: List[ActionItem] = Field(description="List of action items")

print("✅ Pydantic Schema compiled successfully!")
