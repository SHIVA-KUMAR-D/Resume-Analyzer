# utils/job_matcher.py

import pandas as pd

def match_jobs(resume_skills, job_csv_path="data/job_descriptions.csv"):
    if not resume_skills:
        return pd.DataFrame()

    jobs = pd.read_csv(job_csv_path)
    resume_skills_set = set(skill.lower() for skill in resume_skills)

    def calculate_score(description):
        desc_words = set(description.lower().split())
        return len(resume_skills_set & desc_words)

    jobs["score"] = jobs["description"].apply(calculate_score)
    matched = jobs[jobs["score"] > 0].sort_values(by="score", ascending=False)
    return matched.head(5)
