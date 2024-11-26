"""
Configuration management for RMS.

This module handles environment variables and application settings using Pydantic.
It provides a centralized way to manage configuration across the application.
"""
import os
import logging
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    
    Attributes:
        app_name: Name of the application
        debug: Debug mode flag
        database_url: Database connection URL
        secret_key: Secret key for JWT token generation
        algorithm: Algorithm used for JWT token
        access_token_expire_minutes: JWT token expiration time
    """
    # Application Settings
    app_name: str = "RMS - Rating Management System"
    debug: bool = True
    api_prefix: str = "/api/v1"
    
    # Database Settings
    db_path: Path = Path(__file__).parent.parent / "data" / "rms.db"
    database_url: str = f"sqlite:///{db_path}"

    
    # Security Settings
    secret_key: str = "your-secret-key-here"  # Change in production
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    
    # File Upload Settings
    upload_folder: str = "uploads"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = ["image/jpeg", "image/png", "video/mp4"]
    
    # Logging Settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        """Pydantic configuration class."""
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings with caching.
    
    Returns:
        Settings: Application settings instance
    
    Note:
        Uses LRU cache to prevent multiple reads of environment variables
    """
    logger.debug("Loading application settings")
    return Settings()

def init_logging() -> None:
    """Initialize logging configuration."""
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format=settings.log_format
    )
    logger.info(f"Logging initialized at {settings.log_level} level")

def create_upload_folder() -> None:
    """Create upload folder if it doesn't exist."""
    settings = get_settings()
    os.makedirs(settings.upload_folder, exist_ok=True)
    logger.info(f"Upload folder created at {settings.upload_folder}")
