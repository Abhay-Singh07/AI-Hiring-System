# 🚀 AI Hiring Intelligence Platform

An end-to-end AI-powered hiring system that helps recruiters evaluate resumes against job descriptions using **LLMs, Retrieval-Augmented Generation (RAG), semantic similarity, and hybrid scoring**.

This project was built to simulate how a modern intelligent Applicant Tracking System (ATS) should work — not just keyword matching, but deeper contextual understanding of candidate fit.

---

## 🌐 Live Demo

👉 Streamlit App: https://gen-ai-hiring-system.streamlit.app/

---

# 📌 Why I Built This

Traditional ATS systems often reject strong candidates because they rely heavily on exact keyword matches.

I wanted to build a smarter system that can:

- Understand resume context
- Compare candidates fairly
- Identify missing skills
- Rank multiple applicants
- Provide recruiter insights
- Help candidates improve

The result is a deployable AI hiring platform with real-world architecture.

---

# ✨ Core Features

## 👔 Recruiter Features

### ✅ Multi Resume Screening
Upload multiple resumes and compare candidates instantly.

### ✅ Intelligent Candidate Ranking
Ranks candidates using a **hybrid score** based on:

- LLM evaluation
- Skills match ratio
- Semantic similarity
- Retrieval relevance

### ✅ Explainable Hiring Decisions

For every candidate:

- Match score
- Selected / Borderline / Rejected
- Matched skills
- Missing skills
- Summary
- Feedback
- Decision reasoning

### ✅ Recruiter Copilot

Ask natural language questions such as:

- Who is the best fit and why?
- Why was candidate #2 rejected?
- Which candidate has strongest Python skills?
- Compare top 2 applicants

---

## 🧑‍💻 Candidate Features

### ✅ Candidate Copilot

Candidates can ask:

- How can I improve for this role?
- What skills am I missing?
- How do I rewrite my resume for this JD?
- What should I learn next?


- # 🧠 How It Works

## Step 1: Resume Upload

Users upload one or more PDF resumes.

## Step 2: Resume Parsing

PDF text is extracted and cleaned.

## Step 3: Smart Chunking

Resumes are split into meaningful chunks for retrieval.

## Step 4: Hybrid Retrieval (RAG)

Uses:

- FAISS dense vector search
- BM25 keyword retrieval
- Reranking

This ensures only relevant resume content is sent to the LLM.

## Step 5: LLM Evaluation

Groq-hosted LLaMA model evaluates candidate fit against job description.

## Step 6: Hybrid Scoring Engine

Final score combines:

50% LLM Score  
30% Skills Match Score  
20% Semantic Similarity Score

## Step 7: Frontend Dashboard

Results are shown in a recruiter-friendly UI with charts, rankings, and copilots.

---

# 🏗️ Architecture


Frontend (Streamlit)
        ↓
FastAPI Backend
        ↓
Resume Parsing + Chunking
        ↓
FAISS + BM25 Retrieval
        ↓
Groq LLM Evaluation
        ↓
Hybrid Scoring Engine
        ↓
Recruiter / Candidate Copilots


🛠️ Tech Stack

# Backend
Python
FastAPI
Groq API (LLaMA)
Cohere Embeddings
FAISS
BM25
NumPy

# Frontend
Streamlit
Plotly
Pandas

# Deployment
Railway (Backend)
Streamlit Community Cloud (Frontend)



---

## Part 3

# 📊 Example Output

## Candidate Ranking

| Rank | Candidate | Score | Decision |
|------|----------|------|----------|
| 1 | Candidate_A.pdf | 84 | Selected |
| 2 | Candidate_B.pdf | 71 | Borderline |
| 3 | Candidate_C.pdf | 56 | Rejected |

---

# 🤖 Dual Copilot System

## 👔 Recruiter Copilot

Helps hiring teams make faster decisions using AI.

## 🧑‍💻 Candidate Copilot

Helps applicants improve their resumes and skills.

This makes the platform valuable for **both sides of hiring**.



# ⚡ Why This Project Is Different

Most ATS projects only do:

- Keyword matching
- Basic filtering
- Resume parsing

This platform adds:

✅ RAG-based contextual reasoning  
✅ LLM candidate evaluation  
✅ Multi-resume ranking  
✅ Explainable decisions  
✅ Dual AI copilots  
✅ Full cloud deployment  


# 📁 Project Structure

AI-Hiring-Platform/
│── app.py
│── streamlit_app.py
│── prompts.py
│── rag.py
│── embedding.py
│── evaluation.py
│── logger.py
│── requirements.txt
│── README.md


📈 Future Improvements

Planned upgrades:

User authentication
Recruiter dashboards
PDF report exports
JD PDF upload
Interview question generation
Candidate pipeline tracking
SaaS billing model
React frontend version



# 💡 What I Learned Building This

While building this project, I gained practical experience in:

- Full-stack AI systems
- LLM integration
- Retrieval-Augmented Generation
- Vector search
- API deployment
- Product thinking
- Prompt engineering
- Real-world system design


# 🤝 Ideal Use Cases

- Recruiters screening candidates
- Startups hiring quickly
- HR teams comparing applicants
- Candidates improving resumes
- AI hiring automation demos




