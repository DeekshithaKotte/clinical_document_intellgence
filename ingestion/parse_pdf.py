import io
import PyPDF2

def extract_text(file_bytes):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text() or ""
        text += extracted + "\n"
    return text
