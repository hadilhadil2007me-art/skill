from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Determine connect args for SQLite (needed for check_same_thread)
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Check connection health before checking out of pool
    connect_args=connect_args,
)

# SessionLocal is the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Dependency generator that yields a database session and ensures it gets closed
    after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
