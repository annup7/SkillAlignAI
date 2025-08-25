def _extract_text_from_pdf_bytes(pdf_bytes) -> str:
    text = ""
    try:
        import PyPDF2
        from io import BytesIO
        reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception:
        # Fallback decode if library not available
        return pdf_bytes.decode("latin-1", errors="ignore")

def extract_text_from_pdf_fileobj(fileobj) -> str:
    # Streamlit file_uploader returns a file-like object
    data = fileobj.read()
    return _extract_text_from_pdf_bytes(data)

def extract_skills_from_resume(fileobj):
    name = (fileobj.name or "").lower()
    if name.endswith(".pdf"):
        text = extract_text_from_pdf_fileobj(fileobj)
    else:
        # TXT
        text = fileobj.read().decode("utf-8", errors="ignore")
    text = text.lower()
    common_skills = [
        "python", "java", "sql", "html", "css", "javascript", "machine learning",
        "data analysis", "flask", "django", "pandas", "numpy", "react", "node.js",
        "deep learning", "communication", "problem solving", "teamwork", "aws",
        "docker", "kubernetes", "nlp"
    ]
    found_skills = [skill for skill in common_skills if skill in text]
    return list(set(found_skills))
