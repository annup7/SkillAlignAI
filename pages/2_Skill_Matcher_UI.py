import streamlit as st
from db.user_queries import get_user_by_email, is_profile_complete
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.resume_parser import extract_skills_from_resume
from utils.matcher import get_skill_gap_and_similarity
from utils.resume_writer import generate_resume
import base64

st.set_page_config(page_title="SkillAlignAI – Skill Matcher", page_icon="🧠", layout="centered")

if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

user = get_user_by_email(st.session_state["user_info"]["email"])
if not is_profile_complete(user):
    st.error("Please complete your profile before using the Skill Matcher.")
    if st.button("Go to Profile"):
        st.switch_page("pages/3_User_Profile.py")
    st.stop()

st.title("🧠 Skill Matcher")
st.caption("Compare your resume’s skills with a job description.")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_title = st.text_input("Target Job Title")
jd_text = st.text_area("Paste Job Description", height=160)

if st.button("Analyze"):
    if not (resume_file and job_title and jd_text):
        st.warning("Please provide all inputs.")
    else:
        with st.spinner("Analyzing..."):
            resume_skills = extract_skills_from_resume(resume_file)
            jd_skills = extract_skills_from_jd(jd_text)
            missing, score = get_skill_gap_and_similarity(resume_skills, jd_skills)

        st.success("Done!")
        st.metric("Similarity", f"{score:.2f}%")
        st.write("**Your Resume Skills:**", ", ".join(resume_skills) if resume_skills else "—")
        st.write("**JD Skills:**", ", ".join(jd_skills) if jd_skills else "—")
        st.write("**Missing:**", ", ".join(missing) if missing else "None 🎉")

        st.subheader("Generate Tailored Resume")
        include_projects = st.checkbox("Include Projects", value=True)
        include_certs = st.checkbox("Include Certifications", value=True)

        # Compose CSV of user's profile skills + add JD skills (optional)
        skills_csv = user.get("skills") or ""
        path = generate_resume(
            user_name=user.get("full_name"),
            user_skills_csv=skills_csv,
            job_title=job_title,
            matched_skills=[s for s in jd_skills if s in resume_skills],
            missing_skills=missing,
            summary=user.get("summary"),
            projects_text=user.get("projects"),
            certs_text=user.get("certifications"),
            include_projects=include_projects,
            include_certs=include_certs
        )
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Tailored_Resume.pdf">📥 Download Tailored Resume</a>'
            st.markdown(href, unsafe_allow_html=True)

with st.sidebar:
    if st.button("🏠 Home"):
        st.switch_page("pages/0_Home.py")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.rerun()
