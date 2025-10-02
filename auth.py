import hashlib
from sqlalchemy import text
from db.db_connector import get_engine

ENGINE = get_engine()

def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username: str, email: str, password: str):
    """Signup: store only essential account fields. Profile is completed later."""
    hashed = _hash_password(password)
    with ENGINE.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO users (username, email, password)
                VALUES (:username, :email, :password)
            """),
            {"username": username, "email": email, "password": hashed}
        )

def login_user_by_email(email: str, password: str):
    hashed = _hash_password(password)
    with ENGINE.connect() as conn:
        row = conn.execute(
            text("""
                SELECT * FROM users
                WHERE email = :email AND password = :password
            """),
            {"email": email, "password": hashed}
        ).mappings().fetchone()
        return dict(row) if row else None
