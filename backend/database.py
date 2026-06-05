import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
load_dotenv(BASE_DIR / ".env")

# Get connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory; sessionmaker is a function that makes a class
# SessionLocal is only defined once in the entire program
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency function required specifically for FASTAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    from backend.models import Base
    # Create tables; can be done directly with the engine
    Base.metadata.create_all(bind=engine)