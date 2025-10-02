import streamlit as st
from auth_ui import auth_interface

st.set_page_config(page_title="SkillAlignAI – Login", page_icon="🔐", layout="centered")

def main():
    st.title("🔐 SkillAlignAI")
    st.caption("Login or create an account to continue.")

    if not st.session_state.get("logged_in"):
        auth_interface()
        return

    # Logged in → send user to Home page
    st.success(f"Welcome, {st.session_state['user_info'].get('full_name') or st.session_state['user_info']['email']} 👋")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Go to Home"):
            st.switch_page("pages/0_Home.py")
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_info = {}
            st.rerun()

if __name__ == "__main__":
    main()
