from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Candidate(BaseModel):
    """Candidate model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: List[str] = []
    experience_years: int = 0
    education: Optional[str] = None
    cv_text: Optional[str] = None
    cv_file_path: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    desired_salary: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


class CandidateCreate(BaseModel):
    """Create candidate schema"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    skills: List[str] = []
    experience_years: int = 0
    education: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    location: Optional[str] = None
    desired_salary: Optional[float] = None


class CandidateResponse(BaseModel):
    """Candidate response schema"""
    id: str
    name: str
    email: str
    skills: List[str]
    experience_years: int
    created_at: datetime
