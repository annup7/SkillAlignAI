from fpdf import FPDF
import os

def _write_multiline(pdf: FPDF, label: str, body: str):
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, label, ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, body)
    pdf.ln(2)

def generate_resume(full_name: str,
                    profile_skills: list[str],
                    job_title: str,
                    jd_skills: list[str],
                    missing_skills: list[str],
                    projects: list[str] | None = None,
                    certifications: list[str] | None = None,
                    summary: str = "") -> str:
    """
    Create an ATS-friendly PDF resume.
    """

    os.makedirs("output", exist_ok=True)
    file_path = os.path.join("output", f"{(full_name or 'User').replace(' ', '_')}_Optimized_Resume.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"{full_name or 'User'}", ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Target Role: {job_title}", ln=1)
    pdf.ln(3)

    # Summary (limit 400 chars)
    if summary:
        short = summary.strip()[:400]
        _write_multiline(pdf, "Summary", short)

    # Skills (merge profile+jd unique)
    combined = sorted(list(set([*(profile_skills or []), *(jd_skills or [])])))
    _write_multiline(pdf, "Skills", ", ".join(combined) if combined else "—")

    # Projects (as bullets)
    if projects:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Projects", ln=1)
        pdf.set_font("Arial", "", 11)
        for p in [p for p in projects if p.strip()]:
            pdf.multi_cell(0, 6, f"• {p.strip()}")
        pdf.ln(2)

    # Certifications (as bullets)
    if certifications:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Certifications", ln=1)
        pdf.set_font("Arial", "", 11)
        for c in [c for c in certifications if c.strip()]:
            pdf.multi_cell(0, 6, f"• {c.strip()}")
        pdf.ln(2)

    # Recommended skills to add
    if missing_skills:
        _write_multiline(pdf, "Recommended Skills to Add", ", ".join(missing_skills))

    pdf.output(file_path)
    return file_path
