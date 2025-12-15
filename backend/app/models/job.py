from pydantic import BaseModel, Field
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


class Job(BaseModel):
    """Job model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    company: str = "TechCorp"
    description: str
    required_skills: List[str] = []
    nice_to_have_skills: List[str] = []
    min_experience: int = 0
    max_experience: Optional[int] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: str = "Full-time"  # Full-time, Part-time, Contract
    remote: bool = False
    status: str = "active"  # active, closed, draft
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True


class JobCreate(BaseModel):
    """Create job schema"""
    title: str
    company: str = "TechCorp"
    description: str
    required_skills: List[str] = []
    nice_to_have_skills: List[str] = []
    min_experience: int = 0
    max_experience: Optional[int] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    job_type: str = "Full-time"
    remote: bool = False


class JobResponse(BaseModel):
    """Job response schema"""
    id: str
    title: str
    company: str
    required_skills: List[str]
    min_experience: int
    created_at: datetime
    status: str
