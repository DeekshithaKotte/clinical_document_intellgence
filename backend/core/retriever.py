import json
from backend.core.vectorstore import search
from backend.config import CHUNKS_PATH

def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

CHUNKS = load_chunks()

def retrieve_context(query: str, k=3):
    idxs, dists = search(query, k=k)

    docs = []
    for i, d in zip(idxs, dists):
        if i < len(CHUNKS):
            docs.append(
                f"[source={CHUNKS[i]['meta']['source']} score={d:.4f}]\n{CHUNKS[i]['text']}"
            )

    return "\n\n---\n\n".join(docs)
