from backend.core.rules_engine import check_risk_rules
from backend.core.llm import llm_chat

def detect_risks(summary: str):
    rule_based = check_risk_rules(summary)

    llm_prompt = f"""
Extract clinical red flags from this summary:

{summary}

Return 3-5 high-risk clinical signals.
"""

    llm_risks = llm_chat(llm_prompt)

    return {
        "rule_based": rule_based,
        "llm_detected": llm_risks
    }
