def extract_skills_from_jd(jd_text: str):
    jd = (jd_text or "").lower()
    skills = [
        "python","java","sql","html","css","javascript","machine learning",
        "data analysis","flask","django","pandas","numpy","react","node.js",
        "deep learning","communication","problem solving","teamwork","streamlit",
        "git","api","rest","postgresql","mongodb","aws","docker","kubernetes",
    ]
    return sorted({s for s in skills if s in jd})
