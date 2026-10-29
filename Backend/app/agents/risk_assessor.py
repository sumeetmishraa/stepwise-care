def assess_risk(diagnosis: str, medications: list[str], summary: str) -> dict:
    # Illustrative heuristics only; not a medical prediction.
    text = f"{diagnosis} {summary}".lower()
    factors = []
    if any(word in text for word in ["heart failure", "sepsis", "stroke", "pneumonia", "renal"]):
        factors.append("Diagnosis may require close transition follow-up")
    if len(medications) >= 5:
        factors.append("Medication list has five or more entries")
    if any(word in text for word in ["lives alone", "transport", "no caregiver", "cannot afford"]):
        factors.append("Possible support or access barrier mentioned")
    if not factors:
        factors.append("Routine post-discharge follow-up still required")
    score = min(92, 24 + len(medications) * 5 + (25 if len(factors) > 1 else 0))
    level = "Critical" if score >= 85 else "High" if score >= 65 else "Medium" if score >= 40 else "Low"
    return {"risk_level": level, "risk_score": score, "readmission_probability": round(min(75, score * .62), 1), "risk_factors": factors}
