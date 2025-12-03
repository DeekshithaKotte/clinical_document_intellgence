import os
import json
import faiss
import numpy as np
from ingestion.clean_text import clean
from backend.core.embeddings import embedder
from backend.config import VECTOR_DB_PATH, CHUNKS_PATH

GUIDELINES_DIR = os.path.join(os.path.dirname(__file__), "sample_guidelines")

def load_guidelines():
    docs = []
    for fname in os.listdir(GUIDELINES_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(GUIDELINES_DIR, fname), "r", encoding="utf-8") as f:
                docs.append((fname, f.read()))
    return docs

def chunk_text(text, chunk_size=800, overlap=120):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def main():
    raw_docs = load_guidelines()

    all_chunks = []
    metadata = []

    for source_name, text in raw_docs:
        text = clean(text)
        chunks = chunk_text(text)

        for c in chunks:
            all_chunks.append(c)
            metadata.append({"source": source_name})

    print(f"Total chunks: {len(all_chunks)}")

    # ⬇ Local embedding → no API calls
    embeddings = embedder.embed_documents(all_chunks)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, VECTOR_DB_PATH)

    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(
            [{"text": t, "meta": m} for t, m in zip(all_chunks, metadata)],
            f,
            indent=2
        )

    print("✔ FAISS index saved →", VECTOR_DB_PATH)
    print("✔ Chunks saved →", CHUNKS_PATH)

if __name__ == "__main__":
    main()
