from datetime import date, timedelta
from app.models import Patient, Task

def seed_data(db):
    if db.query(Patient).count():
        return
    samples = [
        ("Margaret Wilson", 72, "Heart failure", "High", 76, 47.1, ["Furosemide", "Lisinopril", "Metoprolol", "Potassium"], ["Medication reconciliation", "Cardiology follow-up"]),
        ("James Carter", 64, "Pneumonia", "High", 68, 42.2, ["Amoxicillin", "Albuterol"], ["Breathing symptom check", "Primary care follow-up"]),
        ("Maria Garcia", 58, "Type 2 diabetes", "Medium", 51, 31.6, ["Metformin", "Insulin"], ["Glucose monitoring", "Dietary support"]),
        ("Robert Chen", 81, "Hip replacement", "Medium", 46, 28.5, ["Acetaminophen", "Aspirin"], ["Mobility check", "Physical therapy"]),
        ("Aisha Patel", 49, "Hypertension", "Low", 28, 17.4, ["Amlodipine"], ["Blood pressure check"]),
        ("David Thompson", 67, "COPD exacerbation", "Critical", 91, 56.4, ["Tiotropium", "Albuterol", "Prednisone", "Oxygen"], ["Respiratory check", "Pulmonology follow-up"]),
        ("Linda Brown", 55, "Dehydration", "Low", 22, 13.6, ["Oral rehydration"], ["Hydration check"]),
    ]
    for i, (name, age, diagnosis, level, score, probability, meds, tasks) in enumerate(samples):
        plan = {
            "patient_summary": f"Demo transition-of-care plan for {diagnosis}. Validate with the discharge paperwork.",
            "medications": [{"name": m, "instruction": "Use exactly as prescribed; confirm with clinician."} for m in meds],
            "follow_up_appointments": [{"title": t, "day": 7 if j == 0 else 14, "owner": "Care coordinator"} for j, t in enumerate(tasks)],
            "checkpoints": [{"day": d, "action": a, "responsible_party": "Care coordinator" if d in (1,7,30) else "Patient / caregiver"} for d, a in [(1,"Confirm discharge instructions"),(3,"Check symptoms and medication access"),(7,"Review follow-up appointment"),(14,"Review recovery progress"),(30,"Complete transition-of-care review")]],
            "review_required": True
        }
        patient = Patient(name=name, age=age, diagnosis=diagnosis, discharge_date=(date.today()-timedelta(days=i+1)).isoformat(),
            status="Needs review" if i in (0,5) else "Active", risk_level=level, risk_score=score,
            readmission_probability=probability, medications=meds, care_plan=plan,
            risk_factors=[f"Follow-up needed for {diagnosis.lower()}", "Medication and symptom review recommended"],
            follow_up=tasks, notes="Demo patient record. Not real patient data.")
        db.add(patient)
    db.commit()
    patients = db.query(Patient).all()
    for p in patients:
        db.add(Task(patient_id=p.id, title=f"Day 3 check-in — {p.name}", due_date=(date.today()+timedelta(days=1)).isoformat(), priority=p.risk_level, status="Open", owner="Care coordinator"))
        db.add(Task(patient_id=p.id, title=f"Review follow-up plan — {p.name}", due_date=(date.today()+timedelta(days=4)).isoformat(), priority="Medium", status="Open", owner="Care coordinator"))
    db.commit()
