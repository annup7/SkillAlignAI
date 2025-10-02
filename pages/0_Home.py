import streamlit as st
from db.user_queries import get_user_by_email, is_profile_complete

st.set_page_config(page_title="SkillAlignAI – Home", page_icon="🏠", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning("Please log in to use the platform.")
    st.stop()

user = st.session_state.get("user_info", {})
user = get_user_by_email(user["email"]) or user
st.session_state.user_info = user  # keep fresh

st.title("💼 SkillAlignAI")
st.subheader("Your AI-Powered Resume Optimizer & Skill Matcher")

with st.container():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Profile Status", "Complete ✅" if is_profile_complete(user) else "Incomplete ❗")
    with c2:
        st.metric("Account", user.get("email", "—"))
    with c3:
        st.metric("Name", user.get("full_name") or "—")

st.divider()
st.markdown("### What would you like to do?")

b1, b3 = st.columns(2)
with b1:
    if st.button("👤 Profile"):
        st.switch_page("pages/3_User_Profile.py")

with b3:
    disabled = not is_profile_complete(user)
    if st.button("🧠 Skill Matcher", disabled=disabled):
        st.switch_page("pages/2_Skill_Matcher_UI.py")
    if disabled:
        st.caption("Complete your profile first.")

with st.sidebar:
    st.markdown("### Account")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.rerun()
