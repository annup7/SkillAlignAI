from PyPDF2 import PdfReader

def extract_text_from_pdf(file) -> str:
    # file is a streamlit UploadedFile
    reader = PdfReader(file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_skills_from_resume(file):
    # use extracted text to match against common skills
    resume_text = (extract_text_from_pdf(file) or "").lower()
    common_skills = [
        "python","java","sql","html","css","javascript","machine learning",
        "data analysis","flask","django","pandas","numpy","react","node.js",
        "deep learning","communication","problem solving","teamwork","streamlit",
        "git","api","rest","postgresql","mongodb","aws","docker","kubernetes",
    ]
    found = [s for s in common_skills if s in resume_text]
    return sorted(set(found))
