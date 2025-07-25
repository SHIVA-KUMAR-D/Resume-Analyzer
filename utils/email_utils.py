# utils/email_utils.py

import fitz  # PyMuPDF
import re
import spacy
import pandas as pd
from utils.email_sender import send_email_with_attachment  # ✅ Correct import path

nlp = spacy.load("en_core_web_sm")

COMMON_SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning", "nlp",
    "data analysis", "sql", "excel", "django", "react", "aws", "git", "html", "css", "javascript"
]

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", text)
    return match.group() if match else None

def extract_phone(text):
    match = re.search(r"(\+?\d{1,3})?[\s-]?\(?\d{3,5}\)?[\s-]?\d{3,5}[\s-]?\d{3,5}", text)
    return match.group() if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text):
    text = text.lower()
    found = [skill for skill in COMMON_SKILLS if skill in text]
    return list(set(found))

def extract_education(text):
    education_keywords = ['b.tech', 'm.tech', 'bachelor', 'master', 'b.sc', 'm.sc', 'phd', 'mba']
    found = [kw.upper() for kw in education_keywords if kw in text.lower()]
    return list(set(found))

def parse_resume(file_path):
    if not file_path.endswith(".pdf"):
        raise ValueError("Only PDF files are supported")

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    extracted = {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text),
        "Education": extract_education(text),
        "RawText": text[:500]  # preview
    }

    return extracted

def match_jobs(parsed_data, jobs_df):
    candidate_skills = set(skill.lower() for skill in parsed_data.get("Skills", []))
    matched_jobs = []

    for _, row in jobs_df.iterrows():
        job_skills = set(skill.lower() for skill in row["Skills"])
        match_score = len(candidate_skills & job_skills)

        if match_score > 0:
            matched_jobs.append({
                "Title": row["Title"],
                "Company": row["Company"],
                "MatchScore": match_score,
                "RequiredSkills": row["Skills"]
            })

    matched_jobs.sort(key=lambda x: x["MatchScore"], reverse=True)
    return matched_jobs

# ✅ Sends matched jobs via email
def email_results_to_candidate(resume_path, jobs_df):
    parsed = parse_resume(resume_path)
    matches = match_jobs(parsed, jobs_df)

    if not matches:
        print("No matching jobs found.")
        return

    candidate_email = parsed.get("Email")
    if not candidate_email:
        print("Candidate email not found in resume.")
        return

    subject = "Top Job Matches for You 🎯"
    body = f"Hello {parsed.get('Name', 'Candidate')},\n\nHere are your top job matches:\n\n"

    for job in matches:
        body += f"- {job['Title']} at {job['Company']} (Skills: {', '.join(job['RequiredSkills'])})\n"

    body += "\nGood luck!\nTeam ResumeMatcher"

    send_email_with_attachment(candidate_email, subject, body, resume_path)
