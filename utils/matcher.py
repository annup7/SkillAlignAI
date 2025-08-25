from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_with_jd(resume_text, jd_skills):
    matched_skills = []
    missing_skills = []

    resume_lower = (resume_text or "").lower()

    for skill in jd_skills:
        if skill.lower() in resume_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    tfidf = TfidfVectorizer().fit_transform([resume_text or "", ' '.join(jd_skills)])
    score = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]) * 100 if jd_skills else 0.0

    return matched_skills, missing_skills, score

def get_skill_gap_and_similarity(resume_skills, jd_skills):
    matched = [skill for skill in jd_skills if skill in resume_skills]
    missing = [skill for skill in jd_skills if skill not in resume_skills]
    score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0
    return missing, float(score)
