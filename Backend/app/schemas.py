from pydantic import BaseModel, Field
from typing import Literal

RiskLevel = Literal["Low", "Medium", "High", "Critical"]

class CheckInCreate(BaseModel):
    mood: str = "Okay"
    symptoms: str = "No new symptoms reported"
    medication_taken: bool = True
    notes: str = ""

class EscalationCreate(BaseModel):
    reason: str = Field(min_length=3, max_length=500)
    urgency: Literal["Routine", "Urgent", "Emergency"] = "Urgent"

class IntakeCreate(BaseModel):
    patient_name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=0, le=120)
    diagnosis: str = Field(min_length=2, max_length=200)
    discharge_date: str
    discharge_summary: str = Field(min_length=10)
    medications: list[str] = []

class ApprovePlan(BaseModel):
    coordinator_notes: str = ""
    approved: bool = True

class TaskUpdate(BaseModel):
    status: Literal["Open", "In progress", "Completed"]
