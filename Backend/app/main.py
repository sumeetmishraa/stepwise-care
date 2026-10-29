from datetime import date
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.config import settings
from app.database import Base, engine, get_db
from app.models import Patient, Task, AuditEvent
from app.schemas import IntakeCreate, CheckInCreate, EscalationCreate, ApprovePlan, TaskUpdate
from app.agents.care_planner import create_care_plan
from app.agents.risk_assessor import assess_risk
from app.agents.communication import draft_checkin
from app.agents.escalation import triage_escalation
from app.seed import seed_data

app = FastAPI(title="CareSync AI API", version="0.1.0", description="Demo care-coordination API. Not for clinical use.")
origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_data(db)
    finally:
        db.close()

def audit(db: Session, action: str, patient_id: int | None = None, details: str = ""):
    db.add(AuditEvent(action=action, patient_id=patient_id, details=details))
    db.commit()

def patient_dict(p: Patient):
    return {"id": p.id, "name": p.name, "age": p.age, "diagnosis": p.diagnosis, "discharge_date": p.discharge_date,
        "status": p.status, "risk_level": p.risk_level, "risk_score": p.risk_score,
        "readmission_probability": p.readmission_probability, "medications": p.medications or [],
        "care_plan": p.care_plan or {}, "risk_factors": p.risk_factors or [], "follow_up": p.follow_up or [],
        "notes": p.notes, "created_at": p.created_at.isoformat() if p.created_at else None}

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "caresync-ai-api", "demo_mode": True}

@app.get("/api/patients")
def list_patients(search: str = "", status: str = "", db: Session = Depends(get_db)):
    q = db.query(Patient)
    if search:
        q = q.filter((Patient.name.ilike(f"%{search}%")) | (Patient.diagnosis.ilike(f"%{search}%")))
    if status:
        q = q.filter(Patient.status == status)
    return [patient_dict(p) for p in q.order_by(desc(Patient.risk_score)).all()]

@app.get("/api/patients/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.get(Patient, patient_id)
    if not p: raise HTTPException(404, "Patient not found")
    return patient_dict(p)

@app.get("/api/queue")
def queue(db: Session = Depends(get_db)):
    return [patient_dict(p) for p in db.query(Patient).filter(Patient.status != "Completed").order_by(desc(Patient.risk_score)).all()]

@app.post("/api/intake")
def intake(data: IntakeCreate, db: Session = Depends(get_db)):
    risk = assess_risk(data.diagnosis, data.medications, data.discharge_summary)
    plan = create_care_plan(data.diagnosis, data.medications, data.discharge_summary)
    p = Patient(name=data.patient_name, age=data.age, diagnosis=data.diagnosis, discharge_date=data.discharge_date,
        status="Needs review", risk_level=risk["risk_level"], risk_score=risk["risk_score"],
        readmission_probability=risk["readmission_probability"], medications=data.medications,
        care_plan=plan, risk_factors=risk["risk_factors"], follow_up=[x["title"] for x in plan["follow_up_appointments"]],
        notes="Generated from intake; human review required.")
    db.add(p); db.commit(); db.refresh(p)
    audit(db, "Patient intake created", p.id, "Care plan and illustrative risk assessment generated.")
    return patient_dict(p)

@app.post("/api/patients/{patient_id}/checkins")
def checkin(patient_id: int, data: CheckInCreate, db: Session = Depends(get_db)):
    p = db.get(Patient, patient_id)
    if not p: raise HTTPException(404, "Patient not found")
    audit(db, "Check-in recorded", p.id, f"Mood: {data.mood}; medication taken: {data.medication_taken}; symptoms: {data.symptoms}")
    return {"ok": True, "patient_id": p.id, "recorded": data.model_dump()}

@app.post("/api/patients/{patient_id}/escalations")
def escalation(patient_id: int, data: EscalationCreate, db: Session = Depends(get_db)):
    p = db.get(Patient, patient_id)
    if not p: raise HTTPException(404, "Patient not found")
    result = triage_escalation(data.reason, data.urgency)
    p.status = "Escalated"
    db.add(p)
    audit(db, "Escalation created", p.id, f"{data.urgency}: {data.reason}")
    db.commit()
    return {"ok": True, "triage": result}

@app.post("/api/patients/{patient_id}/approve")
def approve(patient_id: int, data: ApprovePlan, db: Session = Depends(get_db)):
    p = db.get(Patient, patient_id)
    if not p: raise HTTPException(404, "Patient not found")
    p.status = "Active" if data.approved else "Needs review"
    if data.coordinator_notes: p.notes = data.coordinator_notes
    db.add(p); db.commit()
    audit(db, "Care plan approved" if data.approved else "Care plan returned for review", p.id, data.coordinator_notes)
    return patient_dict(p)

@app.get("/api/tasks")
def tasks(db: Session = Depends(get_db)):
    rows = db.query(Task).order_by(Task.due_date.asc()).all()
    return [{"id": t.id, "patient_id": t.patient_id, "title": t.title, "due_date": t.due_date, "priority": t.priority, "status": t.status, "owner": t.owner} for t in rows]

@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    t = db.get(Task, task_id)
    if not t: raise HTTPException(404, "Task not found")
    t.status = data.status; db.add(t); db.commit()
    audit(db, "Task updated", t.patient_id, f"{t.title}: {t.status}")
    return {"id": t.id, "status": t.status}

@app.get("/api/metrics")
def metrics(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    tasks = db.query(Task).all()
    total = len(patients)
    return {"total_patients": total, "active_patients": sum(p.status == "Active" for p in patients),
        "needs_review": sum(p.status == "Needs review" for p in patients), "escalated": sum(p.status == "Escalated" for p in patients),
        "high_risk": sum(p.risk_level in ("High", "Critical") for p in patients),
        "open_tasks": sum(t.status != "Completed" for t in tasks),
        "average_risk": round(sum(p.risk_score for p in patients)/total, 1) if total else 0,
        "risk_distribution": [{"name": level, "value": sum(p.risk_level == level for p in patients)} for level in ["Low","Medium","High","Critical"]]}

@app.get("/api/audit")
def audit_events(db: Session = Depends(get_db)):
    rows = db.query(AuditEvent).order_by(desc(AuditEvent.created_at)).limit(100).all()
    return [{"id": x.id, "patient_id": x.patient_id, "actor": x.actor, "action": x.action, "details": x.details, "created_at": x.created_at.isoformat()} for x in rows]

@app.get("/api/patients/{patient_id}/message-draft")
def message_draft(patient_id: int, db: Session = Depends(get_db)):
    p = db.get(Patient, patient_id)
    if not p: raise HTTPException(404, "Patient not found")
    return draft_checkin(p.name, p.diagnosis)
