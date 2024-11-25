"""
Database models for the RMS application.

This module defines SQLAlchemy ORM models for the core entities in the Rating Management System.
"""
from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, JSON, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

class Gender(enum.Enum):
    """Enum for gender categories in content analysis."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class Rasa(enum.Enum):
    """Enum for the nine emotional essences (Navarasa)."""
    SHRINGARA = "shringara"  # Aesthetic Pleasure
    HASYA = "hasya"          # Joy
    KARUNA = "karuna"        # Empathy
    VEERA = "veera"          # Heroic
    BHAYANAKA = "bhayanaka"  # Horrific
    ADBHUTA = "adbhuta"      # Wonder
    SHANTA = "shanta"        # Serene
    BIBHATSA = "bibhatsa"    # Disgust
    RAUDRA = "raudra"        # Fiery

class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    projects = relationship("Project", back_populates="creator")
    ratings = relationship("Rating", back_populates="user")

class Project(Base):
    """Project model for content creation initiatives."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id"))
    expected_rasa = Column(Enum(Rasa), nullable=False)
    reference_links = Column(JSON)  # Store list of reference URLs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="projects")
    content_items = relationship("ContentItem", back_populates="project")
    ratings = relationship("Rating", back_populates="project")

class ContentItem(Base):
    """Model for individual content pieces within a project."""
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(255), nullable=False)
    content_type = Column(String(50))  # e.g., "image", "video", "text"
    content_url = Column(String(512))  # URL or path to content
    content_data = Column(JSON)  # Store additional metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="content_items")
    philosophical_analysis = relationship("PhilosophicalAnalysis", back_populates="content_item")
    ratings = relationship("Rating", back_populates="content_item")

class PhilosophicalAnalysis(Base):
    """Model for philosophical analysis of content."""
    __tablename__ = "philosophical_analyses"

    id = Column(Integer, primary_key=True)
    content_item_id = Column(Integer, ForeignKey("content_items.id"))
    gender_perspective = Column(Enum(Gender))
    race_perspective = Column(String(100))  # e.g., "North Indian", "South Indian"
    religious_perspective = Column(String(100))  # e.g., "Hindu", "Muslim"
    analysis_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    content_item = relationship("ContentItem", back_populates="philosophical_analysis")

class Rating(Base):
    """Model for content ratings based on Navarasa."""
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    content_item_id = Column(Integer, ForeignKey("content_items.id"))
    rasa = Column(Enum(Rasa), nullable=False)
    rating_value = Column(Integer)  # Scale of 1-10
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="ratings")
    project = relationship("Project", back_populates="ratings")
    content_item = relationship("ContentItem", back_populates="ratings")
