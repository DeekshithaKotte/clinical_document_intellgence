from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .api.summarize import summarize_clinical_note
from .api.diagnose import generate_differential
from .api.risks import detect_risks
from ingestion.parse_pdf import extract_text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Clinical RAG Intelligence API")

# Serve the UI
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/process")
async def process_document(file: UploadFile):
    text = extract_text(await file.read())
    summary = summarize_clinical_note(text)
    risks = detect_risks(summary)
    diagnosis = generate_differential(summary)
    return {"summary": summary, "risks": risks, "diagnosis": diagnosis}

# catch-all: send index.html
@app.get("/{path:path}")
async def spa(path: str):
    return FileResponse("static/index.html")
