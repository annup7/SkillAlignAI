from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_resume_with_jd(resume_text, jd_skills):
    resume_lower = (resume_text or "").lower()
    matched = [s for s in jd_skills if s.lower() in resume_lower]
    missing = [s for s in jd_skills if s.lower() not in resume_lower]

    if jd_skills:
        tfidf = TfidfVectorizer().fit_transform([resume_text or "", " ".join(jd_skills)])
        score = float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0] * 100)
    else:
        score = 0.0
    return matched, missing, score

def get_skill_gap_and_similarity(resume_skills, jd_skills):
    matched = [s for s in jd_skills if s in resume_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0.0
    return missing, float(score)
