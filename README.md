# AI Resume ATS (RAG + LLM + Hybrid Scoring)

This project is an AI-powered resume evaluation system that compares multiple resumes against a job description and ranks candidates based on relevance.

I built this to go beyond keyword-based ATS systems by combining retrieval (RAG), LLM reasoning, and deterministic scoring.

---

## What this project does

- Takes multiple resumes (PDFs) + a job description
- Retrieves the most relevant parts of each resume using semantic + keyword search
- Uses an LLM to evaluate candidates
- Computes a hybrid score
- Ranks candidates from best to worst
- Provides reasoning + feedback for each candidate

---

## How it works (high level)

1. Resume is parsed and split into chunks  
2. Hybrid retrieval:
   - Embeddings (semantic search)
   - BM25 (keyword search)
3. Top chunks are reranked using a cross-encoder
4. LLM evaluates candidate using only relevant context
5. System computes final score:
   - LLM score
   - Skill match score
   - Semantic similarity
6. Candidates are ranked


## Scoring logic

Final Score =
0.5 × LLM Score
0.3 × Skill Score
0.2 × Semantic Similarity


## Features

- Hybrid RAG (BM25 + embeddings)
- Cross-encoder reranking
- Structured LLM outputs (JSON enforced)
- Multi-resume ranking
- Explainable results (decision + reasoning)
- Resume improvement feedback
- Retrieval quality scoring
- Logging for debugging and analysis


## Tech Stack

- FastAPI — backend
- Streamlit — frontend :contentReference[oaicite:0]{index=0}
- SentenceTransformers — embeddings
- FAISS — vector search
- BM25 — keyword search
- Groq (LLaMA) — LLM


## Project structure

-app.py # main API
-rag.py # retrieval logic
-embedding.py # embeddings + reranking
-evaluation.py # metrics
-logger.py # logging
-prompts.py # LLM prompt
-streamlit_app.py # UI


##Why I built this

Most ATS tools rely on keyword matching, which is unreliable.
This project tries to solve that by:

-grounding LLM outputs with RAG
-combining ML + LLM + rule-based scoring
-making results explainable


##Limitations


-Skill extraction depends on LLM output
-No section-aware parsing yet
-Retrieval evaluation is approximate
-Static scoring weights


##Future improvements

-Cross-encoder based reranking improvements
-Section-aware resume parsing
-Better evaluation metrics
-Deployment + multi-user support
-Candidate-side assistant (career guidance)

##Notes

This project is meant to demonstrate:

-RAG system design
-LLM integration
-hybrid AI systems
-explainable AI
