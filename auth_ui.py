import streamlit as st
from auth import register_user, login_user_by_email

def signup_form():
    st.subheader("Create an Account")
    with st.form("signup_form"):
        username = st.text_input("Username", key="su_username")
        email = st.text_input("Email", key="su_email")
        password = st.text_input("Password", type="password", key="su_password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if username and email and password:
                try:
                    register_user(username, email, password)
                    st.success("Account created successfully! Please login.")
                    st.session_state.page = "login"
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please fill username, email and password.")

def login_form():
    st.subheader("Login")
    with st.form("login_form"):
        email = st.text_input("Email", key="li_email")
        password = st.text_input("Password", type="password", key="li_password")
        submitted = st.form_submit_button("Login")

        if submitted:
            row = login_user_by_email(email, password)
            if row:
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user_info = dict(row._mapping)
            else:
                st.error("Invalid credentials.")

def auth_interface():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    tabs = st.tabs(["Login", "Sign Up"])
    with tabs[0]:
        login_form()
    with tabs[1]:
        signup_form()
