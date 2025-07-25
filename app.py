import streamlit as st
import pandas as pd
import os
import spacy
import matplotlib.pyplot as plt

from utils.resume_parser import parse_resume
from utils.pdf_report import generate_pdf_report
from utils.email_sender import send_email_with_attachment

# Load spaCy model once
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

# Load job data
@st.cache_data
def load_jobs(csv_path="data/job_descriptions.csv"):
    return pd.read_csv(csv_path)

# Match jobs based on skills
def match_jobs(parsed_skills, job_df):
    def compute_score(description):
        description = description.lower()
        score = sum(skill.lower() in description for skill in parsed_skills)
        return score

    job_df["score"] = job_df["description"].apply(compute_score)
    return job_df.sort_values(by="score", ascending=False).head(5)

# Plotting skill match bar chart
def plot_skill_match(skills, job_descriptions):
    skill_counts = {skill: 0 for skill in skills}
    for desc in job_descriptions:
        desc = desc.lower()
        for skill in skills:
            if skill.lower() in desc:
                skill_counts[skill] += 1

    fig, ax = plt.subplots()
    ax.bar(skill_counts.keys(), skill_counts.values(), color='skyblue')
    ax.set_title("Skill Match Count")
    ax.set_ylabel("Matches in Job Descriptions")
    ax.set_xticks(range(len(skill_counts)))
    ax.set_xticklabels(skill_counts.keys(), rotation=45, ha='right')
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("🔮 AI-Powered Resume Analyzer")
st.write("Upload your resume (PDF), and get matched job roles + a detailed analysis report!")

# Upload and email input
uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])
receiver_email = st.text_input("Enter your Email to receive the report:")

if uploaded_file and receiver_email:
    with st.spinner("Processing Resume..."):
        # Save uploaded file
        temp_path = "temp_resume.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())

        # Step 1: Parse resume
        parsed_data = parse_resume(temp_path)
        skills = parsed_data.get("Skills", [])

        # Step 2: Match jobs
        job_df = load_jobs()
        matched_jobs = match_jobs(skills, job_df)

        # Step 3: Generate PDF report
        report_path = generate_pdf_report(parsed_data, matched_jobs)

        # Step 4: Send Email
        subject = "Your Resume Analysis & Matched Jobs Report"
        body = "Hi,\n\nAttached is your AI-generated Resume Analysis Report with top job matches.\n\nBest regards,\nAI Resume Analyzer"
        email_status = send_email_with_attachment(receiver_email, subject, body, report_path)

        # Step 5: Show analysis on screen
        st.subheader("📊 Resume Analysis")
        st.write(f"**Name:** {parsed_data.get('Name', 'N/A')}")
        st.write(f"**Email:** {parsed_data.get('Email', 'N/A')}")
        st.write(f"**Phone:** {parsed_data.get('Phone', 'N/A')}")
        st.write(f"**Skills Extracted:** {', '.join(skills) if skills else 'None Found'}")

        st.subheader("✅ Top Job Matches")
        st.dataframe(matched_jobs[["title", "company", "location", "description"]])

        st.subheader("📈 Skill Match Visualization")
        plot_skill_match(skills, matched_jobs["description"].tolist())

        # Download report
        with open(report_path, "rb") as pdf_file:
            st.download_button("📥 Download PDF Report", pdf_file.read(), file_name="Resume_Report.pdf")

        if email_status is True:
            st.success("✅ Report sent successfully to your email!")
        else:
            st.error(f"❌ Failed to send email: {email_status}")
