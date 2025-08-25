import streamlit as st
from db.user_queries import fetch_fresh_user, is_profile_complete
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.resume_parser import extract_skills_from_resume
from utils.matcher import get_skill_gap_and_similarity
from utils.resume_writer import generate_resume
import base64

st.set_page_config(page_title="SkillAlignAI - Skill Matcher", layout="centered")

if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

st.title("🎯 Target Job Role Skill Matcher")

username = st.session_state["user_info"]["username"]
user = fetch_fresh_user(username)
if not is_profile_complete(user):
    st.error("Your profile is incomplete. Please complete it before using the Skill Matcher.")
    if st.button("Go to Profile", key="sm_to_profile"):
        st.switch_page("pages/3_User_Profile.py")
    st.stop()

st.markdown(f"Welcome back, **{user['full_name']}**!")

with st.expander("🔧 Do you want to update your profile before generating a resume?"):
    if st.button("✏️ Update Profile Now", key="sm_update_profile"):
        st.switch_page("pages/3_User_Profile.py")

resume_file = st.file_uploader("📄 Upload your current resume (PDF or TXT)", type=['pdf', 'txt'], key="sm_resume")
job_title = st.text_input("💼 Target Job Title", key="sm_job_title")
job_description = st.text_area("📝 Paste Job Description", key="sm_jd")

if st.button("Analyze & Generate Resume", key="sm_analyze"):
    if not resume_file or not job_title or not job_description:
        st.warning("Please upload a resume and fill in job details.")
    else:
        # Extract user resume skills (parser handles pdf/txt)
        user_resume_skills = extract_skills_from_resume(resume_file)
        jd_skills = extract_skills_from_jd(job_description)
        missing_skills, similarity_score = get_skill_gap_and_similarity(user_resume_skills, jd_skills)

        st.success("✅ Analysis Complete!")
        st.metric("Similarity Score", f"{similarity_score:.2f}%")
        st.markdown("**🔧 Missing Skills:**")
        st.write(", ".join(missing_skills) if missing_skills else "No major gaps found!")

        # Tailored resume – include profile skills if toggled
        include_profile_skills = st.checkbox(
            "Include relevant skills from my profile that are not in my current resume",
            value=True, key="sm_include_profile"
        )

        profile_skills = [s.strip() for s in (user.get("skills") or "").split(",") if s.strip()]
        final_jd_skills = set(jd_skills)
        if include_profile_skills:
            for s in profile_skills:
                if s.lower() in [x.lower() for x in jd_skills]:
                    final_jd_skills.add(s)

        tailored_resume_path = generate_resume(
            user_name=user["full_name"],
            user_skills=", ".join(sorted(set(user_resume_skills) | final_jd_skills)),
            job_title=job_title,
            matched_skills=sorted(list(final_jd_skills)),
            missing_skills=missing_skills
        )

        # Recommendations: projects/certs/summary
        projects_lines = [p.strip() for p in (user.get("projects") or "").splitlines() if p.strip()]
        certs_lines = [c.strip() for c in (user.get("certifications") or "").splitlines() if c.strip()]
        suggested_projects = projects_lines[:3]
        suggested_certs = certs_lines[:3]
        summary = (user.get("summary") or "")[:300]

        st.markdown("**📌 Recommended to highlight:**")
        st.write("- Projects: " + (", ".join(suggested_projects) if suggested_projects else "Add at least one project relevant to the JD"))
        st.write("- Certifications: " + (", ".join(suggested_certs) if suggested_certs else "Consider adding certifications relevant to the JD"))
        st.write(f"- Summary: {summary if summary else 'Write a concise 2–3 line summary tailored to the JD.'}")

        with open(tailored_resume_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Tailored_Resume.pdf">📥 Download Optimized Resume</a>'
            st.markdown(href, unsafe_allow_html=True)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", key="sm_logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.rerun()
