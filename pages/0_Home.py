import streamlit as st

st.set_page_config(page_title="SkillAlignAI - Home", layout="wide")

# -------------------------
# 🔐 Authentication Check
# -------------------------
if not st.session_state.get("logged_in"):
    st.warning("🔐 Please log in from the Login/Signup page to access SkillAlignAI.")
    st.stop()

user_info = st.session_state.get("user_info", {})
st.title("💼 SkillAlignAI")
st.subheader("Your AI-Powered Resume Optimizer & Skill Matcher")

st.success(f"👋 Welcome back, **{user_info.get('full_name', 'User')}**!")

# -------------------------
# 🚪 Sidebar Logout
# -------------------------
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.experimental_rerun()

# -------------------------
# ⚠️ Profile Completion Check
# -------------------------
required_fields = ["full_name", "education", "skills", "projects", "certifications", "summary"]
missing_fields = [f for f in required_fields if not user_info.get(f)]

if missing_fields:
    st.warning(
        "⚠️ Your profile is incomplete! Please complete your profile before using Dashboard or Skill Matcher."
    )

# -------------------------
# 🎯 Navigation in Card Layout
# -------------------------
st.markdown("### 🔧 What would you like to do?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 Dashboard")
    st.write("Analyze your resume against job descriptions and get a skill-gap report.")
    if st.button("Go to Dashboard", key="dashboard_btn", use_container_width=True, disabled=bool(missing_fields)):
        st.switch_page("pages/1_Dashboard.py")

with col2:
    st.markdown("### 🧠 Skill Matcher")
    st.write("Match your skills, projects & certifications with a target job role.")
    if st.button("Open Skill Matcher", key="matcher_btn", use_container_width=True, disabled=bool(missing_fields)):
        st.switch_page("pages/2_Skill_Matcher_UI.py")

with col3:
    st.markdown("### 👤 Profile")
    st.write("Update your personal info, education, skills, projects & certifications.")
    if st.button("Edit Profile", key="profile_btn", use_container_width=True):
        st.switch_page("pages/3_User_Profile.py")

st.markdown("---")
st.info("💡 Tip: Keep your profile updated with new skills, projects, and certifications for best results!")
