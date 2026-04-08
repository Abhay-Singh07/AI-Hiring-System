import numpy as np

# Lazy-loaded model (avoids startup delay on deployment)
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_text(texts):
    try:
        if isinstance(texts, str):
            texts = [texts]

        model = get_model()
        embeddings = model.encode(texts)

        return np.array(embeddings)

    except Exception as e:
        print("Embedding error:", str(e))
        return np.zeros((len(texts), 384))


def cosine_similarity(a, b):
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def rerank(query, chunks):
    try:
        if not chunks:
            return []

        query_vec = embed_text([query])[0]

        # Safety check
        if np.linalg.norm(query_vec) == 0:
            return chunks

        chunk_vecs = embed_text(chunks)

        scores = [
            cosine_similarity(query_vec, chunk_vec)
            for chunk_vec in chunk_vecs
        ]

        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [chunk for chunk, _ in ranked]

    except Exception as e:
        print("Rerank error:", str(e))
        return chunks
