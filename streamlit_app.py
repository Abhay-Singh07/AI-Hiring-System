import streamlit as st
import requests

st.title("GenAI Resume ATS")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area("Paste Job Description")


if st.button("Analyze Candidates"):

    if uploaded_files and job_description:

        files = [
            ("files", (file.name, file.getvalue(), "application/pdf"))
            for file in uploaded_files
        ]

        data = {
            "job_description": job_description
        }

        try:
            response = requests.post(
                "http://localhost:8000/analyze",
                files=files,
                data=data
            )

            result = response.json()

        except Exception as e:
            st.error("Backend connection failed")
            st.stop()

        ranking = result.get("ranking", [])

        st.header("🏆 Candidate Ranking")

        for idx, candidate in enumerate(ranking, start=1):

            st.subheader(f"{idx}. {candidate['candidate']}")

            analysis = candidate["analysis"]

            st.metric("Match Score", f"{candidate['score']}%")

            st.write("Decision")
            st.write(analysis.get("selection_decision", "N/A"))

            st.write("Score Breakdown")
            st.write(analysis.get("score_breakdown", {}))

            st.write("Matched Skills")
            st.write(analysis.get("matched_skills", []))

            st.write("Missing Skills")
            st.write(analysis.get("missing_skills", []))

            st.write("Summary")
            st.write(analysis.get("summary", ""))

            st.write("Decision Reasoning")
            st.write(analysis.get("decision_reasoning", []))

            st.write("Resume Feedback")
            st.write(analysis.get("resume_feedback", ""))

            st.divider()

    else:
        st.warning("Upload at least one resume and paste a job description.")