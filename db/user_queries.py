from sqlalchemy import text
from db.db_connector import get_connection

REQUIRED_FIELDS = ["full_name", "education", "skills", "projects", "certifications", "summary"]

def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        ).fetchone()
    return dict(row._mapping) if row else None

def get_user_by_email(email):
    with get_connection() as conn:
        row = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()
    return dict(row._mapping) if row else None

def update_user_info(username, field, value):
    allowed = {"full_name","education","skills","projects","certifications","summary","email"}
    if field not in allowed:
        raise ValueError("Invalid profile field")
    with get_connection() as conn:
        conn.execute(
            text(f"UPDATE users SET {field} = :val WHERE username = :username"),
            {"val": value, "username": username}
        )

def is_profile_complete(user_dict: dict) -> bool:
    if not user_dict:
        return False
    for f in REQUIRED_FIELDS:
        v = user_dict.get(f)
        if v is None:
            return False
        # skills might be empty list or empty string
        if isinstance(v, str) and not v.strip():
            return False
    return True

def fetch_fresh_user(username):
    """Always fetch latest user from DB (not session copy)."""
    return get_user_by_username(username)
