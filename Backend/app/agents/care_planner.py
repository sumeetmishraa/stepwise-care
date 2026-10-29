from datetime import date, timedelta

def create_care_plan(diagnosis: str, medications: list[str], summary: str) -> dict:
    # Deterministic demo plan. Replace with a clinically validated agent/provider.
    meds = medications or ["Medication list — confirm with discharge paperwork"]
    return {
        "patient_summary": f"Recently discharged following {diagnosis.lower()}. Confirm all details against the discharge paperwork.",
        "medications": [{"name": m, "instruction": "Follow the prescribing clinician's instructions; verify dose and timing."} for m in meds],
        "follow_up_appointments": [
            {"title": "Primary care follow-up", "day": 7, "owner": "Care coordinator"},
            {"title": "Specialist follow-up (if prescribed)", "day": 14, "owner": "Patient / caregiver"}
        ],
        "checkpoints": [
            {"day": 1, "action": "Confirm discharge instructions, medication access, and contact details", "responsible_party": "Care coordinator"},
            {"day": 3, "action": "Check symptoms and whether medications are being taken as prescribed", "responsible_party": "Patient / caregiver"},
            {"day": 7, "action": "Confirm primary care follow-up and review any concerns", "responsible_party": "Care coordinator"},
            {"day": 14, "action": "Review recovery progress and outstanding appointments", "responsible_party": "Patient / caregiver"},
            {"day": 30, "action": "Complete transition-of-care review and document outcomes", "responsible_party": "Care coordinator"}
        ],
        "source_summary_received": bool(summary.strip()),
        "review_required": True
    }
