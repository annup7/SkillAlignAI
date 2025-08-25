from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import os

def generate_resume(full_name, skills, job_title, jd_skills, missing_skills,
                    projects=None, certifications=None, summary=""):
    """
    Generate an optimized resume PDF.

    Args:
        full_name (str): User's name
        skills (list): Extracted skills from resume
        job_title (str): Target job title
        jd_skills (list): Skills extracted from job description
        missing_skills (list): Skills missing from resume
        projects (list): List of projects (strings)
        certifications (list): List of certifications (strings)
        summary (str): Professional summary
    """

    # ✅ Save path
    resume_path = os.path.join("output", f"{full_name.replace(' ', '_')}_Optimized_Resume.pdf")
    os.makedirs("output", exist_ok=True)

    # ✅ PDF Setup
    doc = SimpleDocTemplate(resume_path, pagesize=A4)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    heading = ParagraphStyle("Heading", fontSize=14, spaceAfter=10, alignment=TA_LEFT, bold=True)
    subheading = ParagraphStyle("SubHeading", fontSize=12, spaceAfter=8, alignment=TA_LEFT, textColor="blue")

    content = []

    # 📌 Name & Target Role
    content.append(Paragraph(f"<b>{full_name}</b>", heading))
    content.append(Paragraph(f"Target Role: {job_title}", subheading))
    content.append(Spacer(1, 12))

    # 📌 Summary Section
    if summary:
        short_summary = summary[:400]  # ✅ Limit to 400 characters
        content.append(Paragraph("<b>Summary</b>", subheading))
        content.append(Paragraph(short_summary, normal))
        content.append(Spacer(1, 12))

    # 📌 Skills Section
    combined_skills = list(set(skills + jd_skills))  # ✅ Combine existing + required skills
    content.append(Paragraph("<b>Skills</b>", subheading))
    skill_list = ListFlowable([ListItem(Paragraph(s, normal)) for s in combined_skills], bulletType="bullet")
    content.append(skill_list)
    content.append(Spacer(1, 12))

    # 📌 Projects Section
    if projects:
        content.append(Paragraph("<b>Projects</b>", subheading))
        project_list = ListFlowable([ListItem(Paragraph(p, normal)) for p in projects if p.strip()], bulletType="bullet")
        content.append(project_list)
        content.append(Spacer(1, 12))

    # 📌 Certifications Section
    if certifications:
        content.append(Paragraph("<b>Certifications</b>", subheading))
        cert_list = ListFlowable([ListItem(Paragraph(c, normal)) for c in certifications if c.strip()], bulletType="bullet")
        content.append(cert_list)
        content.append(Spacer(1, 12))

    # 📌 Missing Skills (recommendation)
    if missing_skills:
        content.append(Paragraph("<b>Recommended Skills to Add</b>", subheading))
        missing_list = ListFlowable([ListItem(Paragraph(ms, normal)) for ms in missing_skills], bulletType="bullet")
        content.append(missing_list)
        content.append(Spacer(1, 12))

    # ✅ Build PDF
    doc.build(content)
    return resume_path
