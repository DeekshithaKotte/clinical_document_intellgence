import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma:2b")

def llm_chat(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 120,
            "temperature": 0.2,
            "stop": ["\n\n", "###"]
        }
    }

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=40
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()

    except requests.Timeout:
        return "LLM Error: request timed out"
    except requests.RequestException as e:
        return f"LLM Error: {e}"
