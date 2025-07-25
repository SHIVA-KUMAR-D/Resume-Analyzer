# utils/pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import os

def generate_pdf(parsed_data, matched_jobs):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_file.name

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Resume Analysis Report")

    c.setFont("Helvetica", 12)
    y -= 40
    c.drawString(50, y, f"Name: {parsed_data.get('Name', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Email: {parsed_data.get('Email', 'N/A')}")
    y -= 20
    c.drawString(50, y, f"Phone: {parsed_data.get('Phone', 'N/A')}")

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Skills:")
    c.setFont("Helvetica", 12)
    y -= 20
    c.drawString(50, y, ", ".join(parsed_data.get("Skills", [])) or "None")

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Education:")
    c.setFont("Helvetica", 12)
    y -= 20
    c.drawString(50, y, ", ".join(parsed_data.get("Education", [])) or "None")

    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Top Job Matches:")
    c.setFont("Helvetica", 12)
    y -= 20

    if matched_jobs is not None and not matched_jobs.empty:
        for _, row in matched_jobs.iterrows():
            job_line = f"{row.get('title', '')} at {row.get('company', '')} ({row.get('location', '')}) - Score: {row.get('score', 0)}"
            c.drawString(50, y, job_line)
            y -= 20
            if y < 100:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 12)
    else:
        c.drawString(50, y, "No matched jobs found.")

    c.save()
    return pdf_path
