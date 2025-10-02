from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

load_dotenv()

NEON_DB_URL = os.getenv("NEON_DB_URL")
if not NEON_DB_URL:
    raise RuntimeError("NEON_DB_URL missing in .env")

# psycopg2 + sslmode=require is expected in NEON_DB_URL
engine = create_engine(
    NEON_DB_URL,
    pool_pre_ping=True,
    poolclass=NullPool,  # Neon free tier sometimes hates long-lived pools locally
)

def get_engine():
    return engine

def get_connection():
    return engine.connect()
