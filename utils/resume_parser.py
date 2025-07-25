import fitz  # PyMuPDF
import re
import en_core_web_sm

# Load the spaCy model correctly (no runtime download)
nlp = en_core_web_sm.load()

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
        "RawText": text[:1000]  # Preview of resume text
    }

    return extracted
