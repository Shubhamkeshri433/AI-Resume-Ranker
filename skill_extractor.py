import re

SKILLS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "dax",
    "java",
    "r",
    "tableau",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
    "statistics",
    "dashboard",
    "reporting",
    "data cleaning"
]

def skill_exists(skill, text):

    # Special handling for R language
    if skill == "r":
        return bool(re.search(r"\br\b", text))

    return skill in text


def get_skill_report(resume_text, jd_text):

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    required_skills = [
        skill for skill in SKILLS
        if skill in jd_text
    ]

    matched = [
        skill
        for skill in required_skills
        if skill_exists(skill, resume_text)
    ]

    missing = [
        skill
        for skill in required_skills
        if not skill_exists(skill, resume_text)
    ]

    skill_score = 0

    if len(required_skills) > 0:
        skill_score = round(
            (len(matched) / len(required_skills)) * 100
        )

    return matched, missing, skill_score