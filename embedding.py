from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(texts):
    return model.encode(texts)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))



# Cross-encoder model for reranking
reranker_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, documents):
    pairs = [(query, doc) for doc in documents]
    scores = reranker_model.predict(pairs)

    ranked = sorted(
        zip(documents, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked]