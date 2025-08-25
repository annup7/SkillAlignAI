import streamlit as st
from db.user_queries import fetch_fresh_user, is_profile_complete
from utils.jd_skill_extractor import extract_skills_from_jd
from utils.matcher import match_resume_with_jd
from utils.resume_writer import generate_resume
import base64

st.set_page_config(page_title="SkillAlign AI - Dashboard", layout="centered")

if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

st.title("📄 SkillAlign AI Dashboard")

username = st.session_state["user_info"]["username"]
user = fetch_fresh_user(username)
if not is_profile_complete(user):
    st.error("Your profile is incomplete. Please complete it before using the Dashboard.")
    if st.button("Go to Profile", key="dash_to_profile"):
        st.switch_page("pages/3_User_Profile.py")
    st.stop()

st.markdown(f"Welcome, **{user.get('full_name')}** 👋")

# Offer quick update prompt
with st.expander("🔧 Do you want to update your profile before generating a resume?"):
    if st.button("✏️ Update Profile Now", key="dash_update_profile"):
        st.switch_page("pages/3_User_Profile.py")

# Upload resume and job info
st.header("📥 Upload Resume & Job Details")

uploaded_resume = st.file_uploader("Upload your existing resume (PDF or TXT)", type=["pdf", "txt"], key="dash_resume")
job_title = st.text_input("Enter the Job Title you're targeting", key="dash_job_title")
job_description = st.text_area("Paste the Job Description here", key="dash_jd")

if st.button("🔍 Analyze", key="dash_analyze"):
    if uploaded_resume and job_description and job_title:
        # Read resume text (pdf/txt)
        ext = (uploaded_resume.name or "").lower()
        if ext.endswith(".pdf"):
            try:
                from utils.resume_parser import extract_text_from_pdf_fileobj
                resume_text = extract_text_from_pdf_fileobj(uploaded_resume)
            except Exception:
                resume_text = uploaded_resume.read().decode("latin-1", errors="ignore")
        else:
            resume_text = uploaded_resume.read().decode("utf-8", errors="ignore")

        jd_skills = extract_skills_from_jd(job_description)
        matched, missing, score = match_resume_with_jd(resume_text, jd_skills)

        st.success(f"✅ Similarity Score: {score:.2f}%")
        st.subheader("🧠 Skill Gap Report")
        st.markdown(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
        st.markdown(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")

        st.subheader("📄 Generate Optimized Resume")
        # Build current skills from profile to recommend inclusion
        profile_skills = [s.strip() for s in (user.get("skills") or "").split(",") if s.strip()]
        st.info("We will include your matched skills and can add recommended profile skills if relevant.")

        include_profile_skills = st.checkbox(
            "Include relevant skills from my profile that are not in my current resume",
            value=True, key="dash_include_profile"
        )

        final_skills = set(matched)
        if include_profile_skills:
            for s in profile_skills:
                if s.lower() in [x.lower() for x in jd_skills]:
                    final_skills.add(s)

        # Projects & Certs recommendation (simple heuristic)
        projects_lines = [p.strip() for p in (user.get("projects") or "").splitlines() if p.strip()]
        certs_lines = [c.strip() for c in (user.get("certifications") or "").splitlines() if c.strip()]
        # keep top 3 each for now
        suggested_projects = projects_lines[:3]
        suggested_certs = certs_lines[:3]

        # Summary (limit to 300 already in profile)
        summary = (user.get("summary") or "")[:300]

        # Generate resume (basic PDF)
        optimized_resume_path = generate_resume(
            user_name=user.get("full_name") or user.get("username"),
            user_skills=", ".join(sorted(final_skills)),
            job_title=job_title,
            matched_skills=sorted(list(final_skills)),
            missing_skills=missing
        )

        st.markdown("**📌 Recommended to highlight:**")
        st.write("- Projects: " + (", ".join(suggested_projects) if suggested_projects else "Add at least one project relevant to the JD"))
        st.write("- Certifications: " + (", ".join(suggested_certs) if suggested_certs else "Consider adding certifications relevant to the JD"))
        st.write(f"- Summary: {summary if summary else 'Write a concise 2–3 line summary tailored to the JD.'}")

        with open(optimized_resume_path, "rb") as file:
            b64 = base64.b64encode(file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Optimized_Resume.pdf">📥 Download Optimized Resume</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Please upload resume and fill Job Title + Job Description.")

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", key="dash_logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.rerun()
