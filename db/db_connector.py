from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

NEON_DB_URL = os.getenv("NEON_DB_URL", "")

# Ensure psycopg2 + sslmode
if NEON_DB_URL.startswith("postgresql://") and "psycopg2" not in NEON_DB_URL:
    NEON_DB_URL = NEON_DB_URL.replace("postgresql://", "postgresql+psycopg2://")
if "sslmode=" not in NEON_DB_URL:
    joiner = "&" if "?" in NEON_DB_URL else "?"
    NEON_DB_URL = f"{NEON_DB_URL}{joiner}sslmode=require"

engine = create_engine(NEON_DB_URL, pool_pre_ping=True)

def get_engine():
    return engine

def get_connection():
    return engine.connect()
