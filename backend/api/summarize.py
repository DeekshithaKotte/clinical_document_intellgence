from backend.core.llm import llm_chat
from backend.core.retriever import retrieve_context

def summarize_clinical_note(text: str):
    context = retrieve_context(text)

    prompt = f"""
You are a clinical AI assistant. 
Summarize the following patient note into structured fields:

Chief Complaint:
HPI:
Medications:
Labs:
Assessment:
Plan:
Red Flags:

Document:
{text}

Use this evidence for accuracy:
{context}
"""

    response = llm_chat(prompt)
    return response
