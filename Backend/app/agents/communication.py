def draft_checkin(patient_name: str, diagnosis: str) -> dict:
    return {
        "channel": "SMS",
        "message": f"Hello {patient_name}, we're checking in after your recent discharge for {diagnosis}. How are you feeling, and have you been able to follow your discharge instructions? If you have urgent or worsening symptoms, contact your clinician or local emergency service.",
        "requires_human_review": True
    }
