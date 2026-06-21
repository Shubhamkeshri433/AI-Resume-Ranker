import streamlit as st
import pandas as pd

from resume_parser import extract_text
from ranker import calculate_similarity_score
from skill_extractor import get_skill_report

st.set_page_config(
    page_title="AI Resume Ranker",
    layout="wide"
)

st.title("🤖 AI Resume Ranker")

jd = st.text_area(
    "Paste Job Description"
)

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if st.button("Rank Resumes"):

    results = []

    for file in uploaded_files:

        resume_text = extract_text(file)

        semantic_score = calculate_similarity_score(
            resume_text,
            jd
        )

        matched, missing, skill_score = get_skill_report(
            resume_text,
            jd
        )

        final_score = round(
            (skill_score * 0.6) +
            (semantic_score * 0.4)
        )

        results.append({
            "Candidate": file.name,
            "Final Score": final_score,
            "Skill Score": skill_score,
            "Similarity Score": semantic_score,
            "Matched Skills": ", ".join(matched),
            "Missing Skills": ", ".join(missing)
        })

    df = pd.DataFrame(results)

    df = df.sort_values(
        by="Final Score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(
        0,
        "Rank",
        range(1, len(df) + 1)
    )

    st.success(
        f"🏆 Top Candidate: {df.iloc[0]['Candidate']}"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    st.subheader("Resume Rankings")

    chart_data = df.set_index(
        "Candidate"
    )["Final Score"]

    st.bar_chart(chart_data)

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "📥 Download Report",
        csv,
        "resume_ranking.csv",
        "text/csv"
    )