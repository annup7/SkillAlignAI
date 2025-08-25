def extract_skills_from_jd(jd_text):
    common_skills = [
        "python", "java", "sql", "html", "css", "javascript", "machine learning",
        "data analysis", "flask", "django", "pandas", "numpy", "react", "node.js",
        "deep learning", "communication", "problem solving", "teamwork", "aws",
        "docker", "kubernetes", "nlp"
    ]
    jd_text_lower = (jd_text or "").lower()
    extracted_skills = [skill for skill in common_skills if skill in jd_text_lower]
    return list(set(extracted_skills))
