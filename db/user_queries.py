from sqlalchemy import text
from db.db_connector import get_engine

ENGINE = get_engine()

# only allow these fields to be updated
ALLOWED_PROFILE_FIELDS = {
    "full_name", "summary", "education",
    "skills", "projects", "certifications"
}

def get_user_by_email(email: str):
    with ENGINE.connect() as conn:
        row = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        ).mappings().fetchone()
        return dict(row) if row else None

def get_user_by_username(username: str):
    with ENGINE.connect() as conn:
        row = conn.execute(
            text("SELECT * FROM users WHERE username = :username"),
            {"username": username}
        ).mappings().fetchone()
        return dict(row) if row else None

def update_user_info(email: str, field: str, value: str):
    if field not in ALLOWED_PROFILE_FIELDS:
        raise ValueError("Invalid field update")
    with ENGINE.begin() as conn:
        conn.execute(
            text(f"UPDATE users SET {field} = :value WHERE email = :email"),
            {"value": value, "email": email}
        )

def upsert_profile(email: str, profile: dict):
    # Only keep allowed fields
    safe = {k: v for k, v in profile.items() if k in ALLOWED_PROFILE_FIELDS}
    if not safe:
        return
    sets = ", ".join([f"{k} = :{k}" for k in safe.keys()])
    params = {**safe, "email": email}
    with ENGINE.begin() as conn:
        conn.execute(
            text(f"UPDATE users SET {sets} WHERE email = :email"),
            params
        )

def is_profile_complete(user: dict) -> bool:
    """Require these to be non-empty: full_name, summary, education, skills"""
    if not user:
        return False
    required = ["full_name", "summary", "education", "skills"]
    return all((user.get(k) or "").strip() for k in required)
