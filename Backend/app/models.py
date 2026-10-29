from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    diagnosis: Mapped[str] = mapped_column(String(200))
    discharge_date: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(40), default="Needs review")
    risk_level: Mapped[str] = mapped_column(String(20), default="Medium")
    risk_score: Mapped[float] = mapped_column(Float, default=50)
    readmission_probability: Mapped[float] = mapped_column(Float, default=25)
    medications: Mapped[list] = mapped_column(JSON, default=list)
    care_plan: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_factors: Mapped[list] = mapped_column(JSON, default=list)
    follow_up: Mapped[list] = mapped_column(JSON, default=list)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(180))
    due_date: Mapped[str] = mapped_column(String(20))
    priority: Mapped[str] = mapped_column(String(20), default="Medium")
    status: Mapped[str] = mapped_column(String(30), default="Open")
    owner: Mapped[str] = mapped_column(String(100), default="Care coordinator")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    actor: Mapped[str] = mapped_column(String(100), default="Demo coordinator")
    action: Mapped[str] = mapped_column(String(120))
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
