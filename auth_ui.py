import streamlit as st
from auth import register_user, login_user_by_email

def signup_form():
    st.subheader("Create your account")
    with st.form("signup_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username", key="signup_username", placeholder="e.g. anup07")
        with col2:
            email = st.text_input("Email", key="signup_email", placeholder="you@example.com")

        password = st.text_input("Password", type="password", key="signup_pwd")
        agree = st.checkbox("I agree to Terms & Privacy", key="signup_agree")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not (username and email and password and agree):
                st.warning("Please fill all fields and agree to terms.")
            else:
                try:
                    register_user(username, email, password)
                    st.success("Account created! Please log in.")
                    st.session_state.auth_page = "login"
                except Exception as e:
                    st.error(f"Signup failed: {e}")

def login_form():
    st.subheader("Welcome back")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_pwd")
        submitted = st.form_submit_button("Log In")

        if submitted:
            user = login_user_by_email(email, password)
            if user:
                st.success("Logged in!")
                st.session_state.logged_in = True
                st.session_state.user_info = user
                st.rerun()
            else:
                st.error("Invalid email or password.")

def auth_interface():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "auth_page" not in st.session_state:
        st.session_state.auth_page = "login"

    tabs = st.tabs(["Login", "Sign up"])
    with tabs[0]:
        login_form()
        st.caption("Use your email and password to sign in.")
    with tabs[1]:
        signup_form()
