from fpdf import FPDF

def generate_resume(user_name, user_skills_csv, job_title, matched_skills, missing_skills,
                    summary=None, projects_text=None, certs_text=None,
                    include_projects=True, include_certs=True):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, txt=user_name or "Your Name", ln=True, align='L')

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, txt=f"Target Role: {job_title}", ln=True)

    # Summary
    if summary:
        pdf.ln(3)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "Summary", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 6, summary)

    # Skills
    pdf.ln(3)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "Skills", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, user_skills_csv or "")

    # JD Match
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 8, "JD Match", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, f"Matched: {', '.join(matched_skills) if matched_skills else '—'}")
    pdf.multi_cell(0, 6, f"Suggested (add): {', '.join(missing_skills) if missing_skills else '—'}")

    # Projects
    if include_projects and projects_text:
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "Projects", ln=True)
        pdf.set_font("Arial", size=11)
        for line in projects_text.splitlines():
            if line.strip():
                pdf.multi_cell(0, 6, f"• {line.strip()}")

    # Certifications
    if include_certs and certs_text:
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 13)
        pdf.cell(0, 8, "Certifications", ln=True)
        pdf.set_font("Arial", size=11)
        for line in certs_text.splitlines():
            if line.strip():
                pdf.multi_cell(0, 6, f"• {line.strip()}")

    output_path = "Optimized_Resume.pdf"
    pdf.output(output_path)
    return output_path
