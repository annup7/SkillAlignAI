import streamlit as st
from db.user_queries import get_user_by_email, upsert_profile
import json

st.set_page_config(page_title="SkillAlignAI – Profile", page_icon="👤", layout="centered")
st.title("👤 Your Profile")

if not st.session_state.get("logged_in"):
    st.warning("Please log in first.")
    st.stop()

user = get_user_by_email(st.session_state["user_info"]["email"])
if not user:
    st.error("User not found.")
    st.stop()

with st.form("profile_form", clear_on_submit=False):
    st.subheader("Basic Info")
    full_name = st.text_input("Full name", value=user.get("full_name") or "", max_chars=120, help="This will appear on your resume.")
    summary = st.text_area("Professional summary", value=user.get("summary") or "", max_chars=600, height=120, help="Max 600 characters.")
    education = st.text_area("Education (list your degrees)", value=user.get("education") or "", height=120, help="Example: B.Tech in CSE, 2023 – XYZ University")

    st.subheader("Skills")
    st.caption("Enter comma-separated skills (we'll show them as tags).")
    skills_raw = st.text_input("Skills", value=user.get("skills") or "", placeholder="Python, SQL, Data Analysis, Flask")
    skill_tokens = [s.strip() for s in skills_raw.split(",") if s.strip()]
    if skill_tokens:
        st.write("**Detected skills:**")
        st.write(" ".join([f"`{s}`" for s in skill_tokens]))

    st.subheader("Projects")
    st.caption("Enter each project on a new line (title – tech – short description).")
    projects_text = st.text_area("Projects", value=user.get("projects") or "", height=150)

    st.subheader("Certifications")
    st.caption("Enter each certification on a new line.")
    certs_text = st.text_area("Certifications", value=user.get("certifications") or "", height=120)

    submitted = st.form_submit_button("💾 Save Profile")
    if submitted:
        profile = {
            "full_name": full_name.strip(),
            "summary": summary.strip(),
            "education": education.strip(),
            "skills": ", ".join(skill_tokens),  # store normalized comma string
            "projects": projects_text.strip(),
            "certifications": certs_text.strip(),
        }
        try:
            upsert_profile(user["email"], profile)
            st.success("Profile saved! ✅")
            # refresh session
            st.session_state.user_info.update(profile)
        except Exception as e:
            st.error(f"Failed to save profile: {e}")

st.divider()
colA, colB = st.columns(2)
with colA:
    if st.button("🏠 Back to Home"):
        st.switch_page("pages/0_Home.py")
with colB:
    if st.button("📊 Go to Skill Matcher"):
        st.switch_page("pages/2_Skill_Matcher_UI.py")
