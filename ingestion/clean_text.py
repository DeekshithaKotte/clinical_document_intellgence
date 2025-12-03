import re

def clean(text: str):
    text = re.sub(r"\s+", " ", text)
    return text.strip()
