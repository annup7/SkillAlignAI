import os
import hashlib
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv(".env")

DB_URL = os.getenv("NEON_DB_URL")

if not DB_URL:
    raise ValueError("❌ Database URL not found. Please check your .env file.")

# Create SQLAlchemy engine
engine = create_engine(DB_URL, echo=True, pool_pre_ping=True)

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------
# Register new user
# ---------------------------
def register_user(username, email, password):
    hashed_pwd = hash_password(password)
    try:
        with engine.begin() as conn:  # ✅ auto-commit
            conn.execute(
                text("""
                    INSERT INTO users (username, email, password, full_name, education, skills, projects, certifications, summary)
                    VALUES (:username, :email, :password, NULL, NULL, NULL, NULL, NULL, NULL)
                """),
                {"username": username, "email": email, "password": hashed_pwd}
            )
        print("✅ User inserted successfully")
        return True
    except Exception as e:
        print("❌ Error inserting user:", e)
        return False

# ---------------------------
# Login user (via email)
# ---------------------------
def login_user_by_email(email, password):
    hashed_pwd = hash_password(password)
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE email = :email AND password = :password"),
                {"email": email, "password": hashed_pwd}
            ).fetchone()
        return result
    except Exception as e:
        print("❌ Login error:", e)
        return None
