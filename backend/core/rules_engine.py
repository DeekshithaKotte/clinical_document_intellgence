def check_risk_rules(summary: str):
    risks = []

    if "chest pain" in summary.lower():
        risks.append("Chest pain: possible cardiac origin")

    if "shortness of breath" in summary.lower():
        risks.append("Respiratory distress risk")

    if "blood thinner" in summary.lower() and "nsaid" in summary.lower():
        risks.append("Medication conflict: NSAID + anticoagulant")

    return risks
