# Clinical Document Intelligence (RAG + LLM)

Healthcare-grade assistant that:
- summarizes clinical notes
- flags safety risks
- provides evidence-backed differential diagnoses with citations
- uses RAG to ground outputs

**Data note:** Use synthetic or publicly available de-identified examples only.

## Tech
FastAPI, Python, LangChain, OpenAI, FAISS, React, Docker-ready

## Setup

How to Run This Project (For Anyone)
1. Install Python 3.10–3.12
2. Install Ollama (Free)

https://ollama.com/download

3. Pull the model:
ollama pull llama3.1

4. Clone this repo:
git clone <your-repo-url>

5. Create a virtual environment:
python -m venv .venv


Activate:

Windows:

.venv\Scripts\activate


Mac/Linux:

source .venv/bin/activate

6. Install dependencies:
pip install -r requirements.txt

7. Start backend:
python -m uvicorn backend.main:app --reload --port 8000

8. Start frontend:
cd ui
npm install
npm run dev


Now open:

👉 http://localhost:5173