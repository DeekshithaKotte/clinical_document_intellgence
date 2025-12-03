from openai import OpenAI
from backend.config import OPENAI_API_KEY
import httpx

# force no proxies anywhere
http_client = httpx.Client(proxies=None)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=http_client
)

def llm_chat(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content
