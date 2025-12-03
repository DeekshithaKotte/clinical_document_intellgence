import faiss
import numpy as np
from backend.config import VECTOR_DB_PATH
from backend.core.embeddings import embedder

_index = None

def load_index():
    global _index
    if _index is None:
        _index = faiss.read_index(VECTOR_DB_PATH)
    return _index

def search(query: str, k=3):
    index = load_index()
    q_emb = embedder.embed_query(query)
    q_emb = np.array(q_emb).astype("float32").reshape(1, -1)
    distances, indices = index.search(q_emb, k)
    return indices[0].tolist(), distances[0].tolist()
