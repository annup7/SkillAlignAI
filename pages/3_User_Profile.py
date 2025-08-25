import streamlit as st
from db.user_queries import fetch_fresh_user, update_user_info, is_profile_complete, REQUIRED_FIELDS

st.set_page_config(page_title="SkillAlignAI - Profile", layout="centered")
st.title("👤 Your Profile")

if not st.session_state.get("logged_in"):
    st.warning("Please log in to view your profile.")
    st.stop()

username = st.session_state["user_info"]["username"]
user_data = fetch_fresh_user(username)
if not user_data:
    st.error("User not found.")
    st.stop()

st.markdown("### 🧾 Profile Details")
st.info("You must complete your profile before using Dashboard or Skill Matcher.")

updated_data = {}

# Full Name
updated_data["full_name"] = st.text_input(
    "Full Name", 
    value=user_data.get("full_name") or "", 
    key="prof_full_name"
)

# Email (read-only here; login uses email)
st.text_input("Email", value=user_data.get("email") or "", disabled=True, key="prof_email")

# Education dropdown
degree_options = ["", "B.Tech", "M.Tech", "B.Sc", "M.Sc", "MBA", "Other"]
cur_edu = user_data.get("education") or ""
updated_data["education"] = st.selectbox(
    "Highest Education",
    options=degree_options,
    index=degree_options.index(cur_edu) if cur_edu in degree_options else 0,
    key="prof_edu"
)

# Skills multiselect
all_skills = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "NLP",
    "Java", "C++", "AWS", "React", "Data Analysis", "Django",
    "Flask", "NumPy", "Pandas", "Docker", "Kubernetes"
]
current_skills = [s.strip() for s in (user_data.get("skills") or "").split(",") if s.strip()]
updated_data["skills"] = st.multiselect(
    "Skills (select multiple)", 
    options=all_skills, 
    default=current_skills,
    key="prof_skills"
)

# Projects: one per line
projects_text = user_data.get("projects") or ""
updated_data["projects"] = st.text_area(
    "Projects (one per line)", 
    value=projects_text, 
    height=120,
    key="prof_projects"
)

# Certifications: one per line
certs_text = user_data.get("certifications") or ""
updated_data["certifications"] = st.text_area(
    "Certifications (one per line)", 
    value=certs_text, 
    height=100,
    key="prof_certs"
)

# Summary with character limit
summary_text = user_data.get("summary") or ""
updated_data["summary"] = st.text_area(
    "Professional Summary (max 300 characters)", 
    value=summary_text, 
    max_chars=300, 
    height=120,
    key="prof_summary"
)

# Save Button
if st.button("💾 Save Changes", key="prof_save"):
    for field, value in updated_data.items():
        if isinstance(value, list):  # skills list
            value = ",".join(value)
        update_user_info(username, field, value)
    st.success("✅ Profile updated successfully! (Re-open the page to see fresh data)")
    st.stop()

# Completeness meter
fresh_user = fetch_fresh_user(username)
complete = is_profile_complete(fresh_user)

st.markdown("---")
st.markdown("### ✅ Profile Completeness")
filled = sum(1 for f in REQUIRED_FIELDS if fresh_user.get(f) and str(fresh_user.get(f)).strip())
st.progress(filled / len(REQUIRED_FIELDS))
st.caption(f"{filled}/{len(REQUIRED_FIELDS)} required fields filled")

if not complete:
    st.warning("⚠️ Complete all fields to access Dashboard and Skill Matcher.")
else:
    st.success("🎉 Your profile is complete. You can now use the tools.")
