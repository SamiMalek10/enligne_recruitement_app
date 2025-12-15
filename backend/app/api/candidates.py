from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import os
from pathlib import Path

from app.models.candidate import Candidate, CandidateCreate, CandidateResponse
from app.database import get_database
from app.utils.cv_parser import CVParser, COMMON_SKILLS
from app.config import settings

router = APIRouter(prefix="/api/candidates", tags=["Candidates"])


@router.post("/", response_model=dict)
async def create_candidate(candidate: CandidateCreate, db=Depends(get_database)):
    """Create a new candidate"""
    candidate_dict = candidate.model_dump()
    candidate_dict["created_at"] = datetime.utcnow()
    candidate_dict["updated_at"] = datetime.utcnow()
    
    result = await db.candidates.insert_one(candidate_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Candidate created successfully"
    }


@router.get("/{candidate_id}")
async def get_candidate(candidate_id: str, db=Depends(get_database)):
    """Get candidate by ID"""
    try:
        candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        candidate["id"] = str(candidate["_id"])
        del candidate["_id"]
        return candidate
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def list_candidates(
    skip: int = 0,
    limit: int = 50,
    skills: Optional[str] = None,
    db=Depends(get_database)
):
    """List all candidates with optional filtering"""
    query = {}
    
    if skills:
        skill_list = [s.strip() for s in skills.split(",")]
        query["skills"] = {"$in": skill_list}
    
    cursor = db.candidates.find(query).skip(skip).limit(limit)
    candidates = await cursor.to_list(length=limit)
    
    for candidate in candidates:
        candidate["id"] = str(candidate["_id"])
        del candidate["_id"]
    
    return {
        "total": await db.candidates.count_documents(query),
        "candidates": candidates
    }


@router.post("/upload-cv")
async def upload_cv(
    file: UploadFile = File(...),
    candidate_id: str = Form(...),
    db=Depends(get_database)
):
    """Upload and parse CV for a candidate"""
    
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Create upload directory if not exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, f"{candidate_id}_{file.filename}")
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")
        buffer.write(content)
    
    # Parse CV
    cv_text = CVParser.parse_cv(file_path)
    
    # Extract skills
    extracted_skills = CVParser.extract_skills(cv_text, COMMON_SKILLS)
    
    # Update candidate
    try:
        result = await db.candidates.update_one(
            {"_id": ObjectId(candidate_id)},
            {
                "$set": {
                    "cv_text": cv_text,
                    "cv_file_path": file_path,
                    "updated_at": datetime.utcnow()
                },
                "$addToSet": {"skills": {"$each": extracted_skills}}
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        return {
            "message": "CV uploaded and parsed successfully",
            "extracted_skills": extracted_skills,
            "cv_length": len(cv_text)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{candidate_id}")
async def update_candidate(
    candidate_id: str,
    candidate: CandidateCreate,
    db=Depends(get_database)
):
    """Update candidate information"""
    candidate_dict = candidate.model_dump()
    candidate_dict["updated_at"] = datetime.utcnow()
    
    try:
        result = await db.candidates.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": candidate_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        return {"message": "Candidate updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{candidate_id}")
async def delete_candidate(candidate_id: str, db=Depends(get_database)):
    """Delete a candidate"""
    try:
        result = await db.candidates.delete_one({"_id": ObjectId(candidate_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        return {"message": "Candidate deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
