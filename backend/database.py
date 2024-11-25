"""
Database configuration and connection management for RMS.

This module handles database connection setup, session management,
and provides utility functions for database operations.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator
from config import get_settings

# Configure logging
logger = logging.getLogger(__name__)

def get_database_url() -> str:
    """Get database URL from settings."""
    settings = get_settings()
    return settings.database_url

# Create SQLAlchemy engine
engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,  # Enable connection health checks
    echo=True  # Log SQL queries (disable in production)
)

# Create sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        with get_db() as db:
            db.query(User).all()
    """
    db = SessionLocal()
    try:
        logger.debug("Creating database session")
        yield db
        db.commit()
        logger.debug("Committing database session")
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        db.rollback()
        logger.debug("Rolling back database session")
        raise
    finally:
        logger.debug("Closing database session")
        db.close()

def init_db() -> None:
    """Initialize database tables."""
    from models import Base
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully initialized database tables")
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI endpoints that need database access.
    
    Yields:
        Session: SQLAlchemy database session
    
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db_session)):
            return db.query(User).all()
    """
    with get_db() as session:
        yield session
