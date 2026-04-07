from embedding import embed_text, cosine_similarity
import numpy as np


# -------------------------------
# 📊 Retrieval Evaluation
# -------------------------------
def retrieval_score(query, chunks):
    """
    Measures how relevant retrieved chunks are to query
    using cosine similarity.
    """

    query_vec = embed_text([query])[0]
    chunk_vecs = embed_text(chunks)

    scores = [
        cosine_similarity(query_vec, chunk_vec)
        for chunk_vec in chunk_vecs
    ]

    return np.mean(scores) * 100


# -------------------------------
# 🔍 RAG vs NO-RAG Comparison
# -------------------------------
def compare_rag_vs_no_rag(llm_fn, query, context):
    """
    Runs LLM with and without RAG context.
    """

    # With RAG
    rag_response = llm_fn(context, query)

    # Without RAG
    no_rag_response = llm_fn("", query)

    return {
        "with_rag": rag_response,
        "without_rag": no_rag_response
    }


# -------------------------------
# 🔁 Consistency Check
# -------------------------------
def consistency_score(llm_fn, context, query, runs=3):
    """
    Measures stability of LLM outputs.
    """

    scores = []

    for _ in range(runs):
        result = llm_fn(context, query)

        llm_score = result.get("llm_score", 0)
        scores.append(llm_score)

    return np.std(scores)  # lower = more stable