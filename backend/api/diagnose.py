from backend.core.llm import llm_chat
from backend.core.retriever import retrieve_context

def generate_differential(summary: str):
    ctx = retrieve_context(summary)

    prompt = f"""
You are a senior physician. Based on the clinical summary below, 
provide the top 3 differential diagnoses. For each diagnosis include:

- Probability (0-1)
- Reasoning
- Supporting evidence from guidelines

SUMMARY:
{summary}

EVIDENCE:
{ctx}
"""

    return llm_chat(prompt)
