# ===== PHASE 1: Project Setup =====
"""
Database connection setup.
Structured for SQLite now, designed to scale to PostgreSQL later.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite for development - easy to swap to PostgreSQL
DATABASE_URL = "sqlite:///./smartqr.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite-specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for FastAPI routes - yields database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
