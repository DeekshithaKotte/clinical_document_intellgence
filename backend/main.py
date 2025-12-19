import asyncio
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load env first (before anything that reads env vars)
load_dotenv()

# If this file is backend/app/main.py, these imports should be RELATIVE:
from .api.summarize import summarize_clinical_note
from .api.diagnose import generate_differential
from .api.risks import detect_risks

# This one depends on your folder structure (see note below)
from .ingestion.parse_pdf import extract_text


app = FastAPI(title="Clinical RAG Intelligence API")

# Serve UI (make sure the folder exists at runtime)
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
    file_bytes = await file.read()
    filename = (file.filename or "").lower()
    ctype = (file.content_type or "").lower()

    # 1) Read text safely based on file type
    if filename.endswith(".txt") or ctype.startswith("text/"):
        text = file_bytes.decode("utf-8", errors="ignore")

    elif filename.endswith(".pdf") or ctype == "application/pdf":
        try:
            text = extract_text(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"PDF parse failed: {e}")

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a .pdf or .txt file.")

    # 2) Run steps with timeout
    try:
        summary = await asyncio.wait_for(
            asyncio.to_thread(summarize_clinical_note, text),
            timeout=90
        )

        # Run dependent tasks in parallel after summary is ready
        risks, diagnosis = await asyncio.wait_for(
            asyncio.gather(
                asyncio.to_thread(detect_risks, summary),
                asyncio.to_thread(generate_differential, summary),
            ),
            timeout=90
        )

    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Processing timed out. Try a smaller file or use a smaller model."
        )

    return {"summary": summary, "risks": risks, "diagnosis": diagnosis}

# catch-all: send index.html
@app.get("/{path:path}")
async def spa(path: str):
    return FileResponse("static/index.html")
