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

### 1) Build vector index
```bash
cd clinical-rag-assistant
pip install -r backend/requirements.txt
python ingestion/build_index.py
```

### 2) Run backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 3) Run UI
```bash
cd ui
npm install
npm run dev
```

Open UI at http://localhost:5173
