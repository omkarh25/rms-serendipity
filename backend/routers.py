"""
API routers for the RMS application.

This module contains FastAPI routers for handling different API endpoints
including projects, ratings, and user management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime
from pydantic import BaseModel

import models
from database import get_db_session
from config import get_settings

# Configure logging
logger = logging.getLogger(__name__)

# Pydantic models for request validation
class ProjectCreate(BaseModel):
    """Schema for project creation request."""
    title: str
    description: Optional[str] = None
    expected_rasa: Optional[str] = "SHRINGARA"

class RatingCreate(BaseModel):
    """Schema for rating creation request."""
    project_id: int
    rasa: str
    rating_value: int
    feedback: Optional[str] = None

# Create routers
projects_router = APIRouter(prefix="/projects", tags=["Projects"])
ratings_router = APIRouter(prefix="/ratings", tags=["Ratings"])
users_router = APIRouter(prefix="/users", tags=["Users"])

# Project endpoints
@projects_router.get("/")
async def get_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    """
    Get list of projects with pagination.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        List of projects
    """
    logger.info(f"Fetching projects with skip={skip}, limit={limit}")
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@projects_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db_session)
):
    """
    Create a new project.
    
    Args:
        project: Project creation data
        db: Database session
    
    Returns:
        Created project
    """
    logger.info(f"Creating new project: {project.title}")
    try:
        rasa_enum = models.Rasa[project.expected_rasa.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid rasa value. Must be one of: {', '.join(models.Rasa.__members__.keys())}"
        )

    db_project = models.Project(
        title=project.title,
        description=project.description,
        expected_rasa=rasa_enum
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Rating endpoints
@ratings_router.get("/")
async def get_ratings(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db_session)
):
    """
    Get list of ratings with optional project filter.
    
    Args:
        project_id: Optional project ID to filter ratings
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
    
    Returns:
        List of ratings
    """
    logger.info(f"Fetching ratings for project_id={project_id}")
    query = db.query(models.Rating)
    if project_id:
        query = query.filter(models.Rating.project_id == project_id)
    return query.offset(skip).limit(limit).all()

@ratings_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db_session)
):
    """
    Create a new rating for a project.
    
    Args:
        rating: Rating creation data
        db: Database session
    
    Returns:
        Created rating
    """
    logger.info(f"Creating new rating for project {rating.project_id}")
    # Verify project exists
    project = db.query(models.Project).filter(models.Project.id == rating.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {rating.project_id} not found"
        )
    
    try:
        rasa_enum = models.Rasa[rating.rasa.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid rasa value. Must be one of: {', '.join(models.Rasa.__members__.keys())}"
        )

    db_rating = models.Rating(
        project_id=rating.project_id,
        rasa=rasa_enum,
        rating_value=rating.rating_value,
        feedback=rating.feedback
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

# User endpoints
@users_router.get("/me")
async def get_current_user():
    """Get current user profile."""
    # TODO: Implement user authentication
    return {"message": "Current user profile"}

@users_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db_session)
):
    """
    Register a new user.
    
    Args:
        username: Username
        email: Email address
        password: Password
        db: Database session
    
    Returns:
        Created user
    """
    logger.info(f"Registering new user: {username}")
    # TODO: Implement password hashing and user creation
    return {"message": "User registration endpoint"}
