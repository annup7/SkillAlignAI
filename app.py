import streamlit as st
from auth_ui import auth_interface

# IMPORTANT: set_page_config must be first Streamlit call in this file
st.set_page_config(page_title="SkillAlignAI", layout="centered")

def main():
    st.title("📄 SkillAlignAI - ATS-Friendly Resume Generator")

    # 🔐 Auth: show login/signup when not logged in
    if not st.session_state.get("logged_in"):
        auth_interface()
        return

    # ✅ Logged in: simple home landing
    user = st.session_state.get("user_info", {})
    st.success(f"Welcome, {user.get('full_name') or user.get('username') or 'User'} 👋")

    st.markdown("Use the sidebar or buttons below to navigate.")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🏠 Home"):
            st.switch_page("pages/0_Home.py")
    with col2:
        if st.button("📊 Dashboard"):
            st.switch_page("pages/1_Dashboard.py")
    with col3:
        if st.button("🧠 Skill Matcher"):
            st.switch_page("pages/2_Skill_Matcher_UI.py")

    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = {}
        st.rerun()

if __name__ == "__main__":
    main()
