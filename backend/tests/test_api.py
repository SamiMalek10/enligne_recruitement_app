import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "app" in response.json()


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_candidate():
    """Test creating a candidate"""
    candidate_data = {
        "name": "Test User",
        "email": "test@example.com",
        "skills": ["Python", "Docker"],
        "experience_years": 3
    }
    
    response = client.post("/api/candidates/", json=candidate_data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_create_job():
    """Test creating a job"""
    job_data = {
        "title": "Software Engineer",
        "company": "TestCorp",
        "description": "We are looking for a talented engineer",
        "required_skills": ["Python", "Docker"],
        "min_experience": 2
    }
    
    response = client.post("/api/jobs/", json=job_data)
    assert response.status_code == 200
    assert "id" in response.json()
