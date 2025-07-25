# utils/pdf_report.py

from fpdf import FPDF
import unicodedata

def sanitize_text(text):
    """Converts Unicode text to ASCII-safe text for FPDF."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    return text.encode("latin-1", "ignore").decode("latin-1")

def generate_pdf_report(data, matched_jobs=None, output_path="resume_analysis_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 10, "AI Resume Analysis Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    def add_line(title, value):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(40, 10, f"{title}:")
        pdf.set_font("Arial", size=12)
        safe_value = sanitize_text(value if value else "Not Found")
        pdf.multi_cell(0, 10, safe_value)
        pdf.ln(2)

    # Add parsed resume info
    add_line("Name", data.get("Name"))
    add_line("Email", data.get("Email"))
    add_line("Phone", data.get("Phone"))
    add_line("Education", ", ".join(data.get("Education", [])))
    add_line("Skills", ", ".join(data.get("Skills", [])))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resume Text Preview:", ln=True)
    pdf.set_font("Arial", size=11)
    preview = sanitize_text(data.get("RawText", "")[:1000])
    pdf.multi_cell(0, 8, preview)

    # Add matched job descriptions if provided
    if matched_jobs is not None and not matched_jobs.empty:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Top Matching Jobs", ln=True)
        pdf.ln(5)
        for index, row in matched_jobs.iterrows():
            title = sanitize_text(str(row.get("title", "")))
            company = sanitize_text(str(row.get("company", "")))
            location = sanitize_text(str(row.get("location", "")))
            description = sanitize_text(str(row.get("description", "")))

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"{title} at {company}", ln=True)
            pdf.set_font("Arial", size=11)
            pdf.cell(0, 10, f"Location: {location}", ln=True)
            pdf.multi_cell(0, 8, f"Description: {description}")
            pdf.ln(4)

    pdf.output(output_path)
    return output_path
