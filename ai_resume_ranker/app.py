import streamlit as st
import pandas as pd

from resume_parser import extract_text
from ranker import calculate_similarity_score
from skill_extractor import get_skill_report
from experience_extractor import estimate_experience

st.set_page_config(
    page_title="AI Resume Ranker",
    layout="wide"
)

st.title("🤖 AI Recruiter Copilot")

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

        experience_years = estimate_experience(
            resume_text
        )

        experience_score = min(
            experience_years * 10,
            100
        )

        final_score = round(
            (semantic_score * 0.40)
            + (skill_score * 0.40)
            + (experience_score * 0.20)
        )

        if final_score >= 85:
            recommendation = "Strong Fit"

        elif final_score >= 70:
            recommendation = "Good Fit"

        else:
            recommendation = "Low Fit"

        if missing:
            recruiter_notes = (
                "Missing Skills: "
                + ", ".join(missing)
            )
        else:
            recruiter_notes = (
                "All required skills found"
            )

        results.append({

            "Candidate": file.name,

            "Final Score": final_score,

            "Semantic Score": semantic_score,

            "Skill Score": skill_score,

            "Experience (Years)": experience_years,

            "Matched Skills":
                ", ".join(matched),

            "Missing Skills":
                ", ".join(missing),

            "Recommendation":
                recommendation,

            "Recruiter Notes":
                recruiter_notes
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

    st.subheader(
        "Candidate Ranking Scores"
    )

    chart_data = df.set_index(
        "Candidate"
    )["Final Score"]

    st.bar_chart(chart_data)

    st.subheader(
        "Top Candidate Analysis"
    )

    top_candidate = df.iloc[0]

    st.info(
        f"""
        Candidate: {top_candidate['Candidate']}

        Final Score: {top_candidate['Final Score']}

        Recommendation:
        {top_candidate['Recommendation']}

        Recruiter Notes:
        {top_candidate['Recruiter Notes']}
        """
    )

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        "📥 Download Ranked Candidates",
        csv,
        "ranked_candidates.csv",
        "text/csv"
    )