def triage_escalation(reason: str, urgency: str) -> dict:
    return {
        "urgency": urgency,
        "recommended_route": "On-call clinical team" if urgency in ("Urgent", "Emergency") else "Care coordinator",
        "reason": reason,
        "human_confirmation_required": True
    }
