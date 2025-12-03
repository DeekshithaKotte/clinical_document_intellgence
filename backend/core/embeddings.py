from sentence_transformers import SentenceTransformer

# Local embedding model
# MiniLM-L6-v2 → small, fast, strong for clinical text
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class LocalEmbedder:
    def embed_documents(self, docs):
        # expects a list of strings
        return _model.encode(docs, convert_to_numpy=True).tolist()

    def embed_query(self, query):
        return _model.encode([query], convert_to_numpy=True)[0].tolist()

embedder = LocalEmbedder()
