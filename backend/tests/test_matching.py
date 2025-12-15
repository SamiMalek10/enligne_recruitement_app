import pytest
from app.ml.matching_engine import MatchingEngine


def test_skill_match():
    """Test skill matching"""
    engine = MatchingEngine()
    
    candidate_skills = ["Python", "Docker", "Kubernetes"]
    required_skills = ["Python", "Docker"]
    
    score = engine.calculate_skill_match(candidate_skills, required_skills)
    assert score == 1.0  # Perfect match


def test_experience_match():
    """Test experience matching"""
    engine = MatchingEngine()
    
    # Exact match
    score = engine.calculate_experience_match(5, 5)
    assert score == 1.0
    
    # Underqualified
    score = engine.calculate_experience_match(2, 5)
    assert score < 1.0
    
    # Overqualified
    score = engine.calculate_experience_match(15, 5, 10)
    assert score == 0.8


def test_matching_score():
    """Test comprehensive matching score"""
    engine = MatchingEngine()
    
    candidate = {
        "skills": ["Python", "ML", "Docker"],
        "experience_years": 5,
        "cv_text": "Experienced Python developer with ML expertise"
    }
    
    job = {
        "required_skills": ["Python", "ML"],
        "min_experience": 3,
        "description": "Looking for Python ML engineer"
    }
    
    result = engine.calculate_match_score(candidate, job)
    
    assert "total_score" in result
    assert "skill_match" in result
    assert "experience_match" in result
    assert 0 <= result["total_score"] <= 1
