import numpy as np
import cohere
import os

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def embed_text(texts):
    try:
        if isinstance(texts, str):
            texts = [texts]

        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )

        embeddings = np.array(response.embeddings)

        return embeddings

    except Exception as e:
        print("Embedding error:", str(e))
        return np.zeros((len(texts), 1024))


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
