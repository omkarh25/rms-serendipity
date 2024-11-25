"""
Test suite for RMS API endpoints.

This module contains tests for the FastAPI endpoints using pytest and the TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add parent directory to path to import from parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base, get_db_session
from models import Project, Rating, User, Rasa

# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database session for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database session with our test database
app.dependency_overrides[get_db_session] = override_get_db

# Create test client
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_main():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "active"

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_project():
    """Test project creation endpoint."""
    project_data = {
        "title": "Test Project",
        "description": "Test Description",
        "expected_rasa": "SHRINGARA"
    }
    response = client.post("/api/v1/projects/", json=project_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == project_data["title"]
    assert data["description"] == project_data["description"]

def test_get_projects():
    """Test getting list of projects."""
    # Create test projects
    project_data = [
        {"title": "Project 1", "description": "Description 1"},
        {"title": "Project 2", "description": "Description 2"}
    ]
    for project in project_data:
        client.post("/api/v1/projects/", json=project)
    
    response = client.get("/api/v1/projects/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Project 1"
    assert data[1]["title"] == "Project 2"

def test_create_rating():
    """Test rating creation endpoint."""
    # First create a project
    project_response = client.post("/api/v1/projects/", 
        json={"title": "Test Project", "description": "Test Description"})
    project_id = project_response.json()["id"]
    
    # Create rating for the project
    rating_data = {
        "project_id": project_id,
        "rasa": "SHRINGARA",
        "rating_value": 8,
        "feedback": "Great content!"
    }
    response = client.post("/api/v1/ratings/", json=rating_data)
    assert response.status_code == 201
    data = response.json()
    assert data["project_id"] == project_id
    assert data["rating_value"] == 8

def test_get_ratings():
    """Test getting list of ratings."""
    # Create a project and some ratings
    project_response = client.post("/api/v1/projects/", 
        json={"title": "Test Project", "description": "Test Description"})
    project_id = project_response.json()["id"]
    
    rating_data = [
        {"project_id": project_id, "rasa": "SHRINGARA", "rating_value": 8},
        {"project_id": project_id, "rasa": "HASYA", "rating_value": 7}
    ]
    
    for rating in rating_data:
        client.post("/api/v1/ratings/", json=rating)
    
    response = client.get(f"/api/v1/ratings/?project_id={project_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["rating_value"] == 8
    assert data[1]["rating_value"] == 7

def test_invalid_project_id():
    """Test rating creation with invalid project ID."""
    rating_data = {
        "project_id": 999,  # Non-existent project ID
        "rasa": "SHRINGARA",
        "rating_value": 8
    }
    response = client.post("/api/v1/ratings/", json=rating_data)
    assert response.status_code == 404

def test_invalid_rating_value():
    """Test rating creation with invalid rating value."""
    # First create a project
    project_response = client.post("/api/v1/projects/", 
        json={"title": "Test Project", "description": "Test Description"})
    project_id = project_response.json()["id"]
    
    rating_data = {
        "project_id": project_id,
        "rasa": "SHRINGARA",
        "rating_value": 11  # Invalid rating value (should be 1-10)
    }
    response = client.post("/api/v1/ratings/", json=rating_data)
    assert response.status_code == 422  # Validation error
