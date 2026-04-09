from fastapi import FastAPI, UploadFile, Form, File
from rag import load_pdf, chunk_text, VectorStore
from prompts import ATS_PROMPT
from embedding import embed_text, cosine_similarity, rerank
from evaluation import retrieval_score
from logger import log_entry

from groq import Groq
import json
import time
import numpy as np
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()


def clean_query(text):
    return " ".join(text.lower().split())


@app.post("/analyze")
async def analyze_resumes(files: list[UploadFile]= File(...), job_description: str = Form(...)):

    results = []

    cleaned_jd = clean_query(job_description)
    jd_vec = embed_text([job_description])[0]
    if jd_vec is None or len(jd_vec) == 0:
        jd_vec = np.zeros(384)

    for file in files:

        vector_store = VectorStore()

        resume_text = load_pdf(file.file)
        chunks = chunk_text(resume_text)

        vector_store.build(chunks)

        retrieved = vector_store.query(cleaned_jd, k=8, alpha=0.6)

        if not retrieved:
            continue

        reranked = rerank(cleaned_jd, retrieved)
        top_chunks = reranked[:4]
        context = "\n".join(top_chunks)
        retrieval_quality = retrieval_score(cleaned_jd, top_chunks)

        prompt = ATS_PROMPT.format(
            resume_context=context,
            job_description=job_description
        )

        start_time = time.time()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        latency = time.time() - start_time

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(raw)
            original_result = result.copy()
        except Exception:
            results.append({
                "candidate": file.filename,
                "error": "LLM did not return valid JSON",
                "raw_output": raw
            })
            continue

        #Skill Score
        matched = result.get("matched_skills", [])
        missing = result.get("missing_skills", [])

        total = len(matched) + len(missing)

        if total == 0:
            skill_score = 0
        else:
            skill_score = len(matched) / total * 100

        # Semantic Similarity
        chunk_vecs = embed_text(chunks)
        resume_vec = chunk_vecs.mean(axis=0)

        semantic_score = cosine_similarity(resume_vec, jd_vec) * 100

        #LLM Score
        llm_score = result.get("llm_score", 50)

        # Hybrid Score
        final_score = (
            0.5 * llm_score +
            0.3 * skill_score +
            0.2 * semantic_score
        )

        final_score = round(final_score)
        if final_score >= 80:
            decision = "Selected"
        elif final_score >= 60:
            decision = "Borderline"
        else:
            decision = "Rejected"

        result["match_score"] = final_score
        result["selection_decision"] = decision

        result["score_breakdown"] = {
            "llm_score": float(round(llm_score)),
            "skill_score": float(round(skill_score)),
            "semantic_score": float(round(semantic_score)),
            "retrieval_score": float(round(retrieval_quality))
        }

        log_entry({
            "candidate": file.filename,
            "job_description": job_description,
            "retrieved_chunks": retrieved,
            "reranked_chunks": top_chunks,
            "retrieval_score": float(retrieval_quality),
            "llm_output": raw,
            "parsed_output": original_result,
            "latency": float(latency),
            "scores": {
                "llm_score": float(llm_score),
                "skill_score": float(skill_score),
                "semantic_score": float(semantic_score),
                "final_score": float(final_score)
            }
        })

        results.append({
            "candidate": file.filename,
            "score": float(final_score),
            "analysis": result
        })

    #Ranking
    valid_results = [r for r in results if "score" in r]

    ranked_results = sorted(valid_results, key=lambda x: x["score"], reverse=True)

    return {
        "ranking": ranked_results
    }
