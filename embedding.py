import os
import requests
import numpy as np

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def embed_text(texts):
    try:
        if isinstance(texts, str):
            texts = [texts]

        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": texts}
        )

        if response.status_code != 200:
            print("HF API Error:", response.text)
            return np.zeros((len(texts), 384))

        embeddings = response.json()
        return np.array(embeddings)

    except Exception as e:
        print("Embedding exception:", str(e))
        return np.zeros((len(texts), 384))


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def rerank(query, chunks):
    query_vec = embed_text([query])[0]
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
