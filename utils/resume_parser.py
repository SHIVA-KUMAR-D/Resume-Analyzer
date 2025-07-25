import fitz  # PyMuPDF
import spacy
import subprocess
import sys
import re

def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Automatically download the model if not present
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_emails(text):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

def extract_phone_numbers(text):
    return re.findall(r"\+?\d[\d \-\(\)]{8,}\d", text)

def extract_skills(text):
    skills_keywords = [
        "python", "java", "c++", "c#", "javascript", "typescript", "react", "node.js",
        "angular", "vue", "html", "css", "sql", "nosql", "mongodb", "mysql", "postgresql",
        "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "tensorflow",
        "pytorch", "linux", "flask", "django", "fastapi", "nlp", "machine learning",
        "deep learning", "data science", "pandas", "numpy", "scikit-learn"
    ]
    text = text.lower()
    return list(set(skill for skill in skills_keywords if skill in text))

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def parse_resume(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    return {
        "name": extract_name(text),
        "email": extract_emails(text),
        "phone": extract_phone_numbers(text),
        "skills": extract_skills(text),
        "raw_text": text
    }
