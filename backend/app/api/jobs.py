from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from bson import ObjectId
from datetime import datetime

from app.models.job import Job, JobCreate, JobResponse
from app.database import get_database

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("/", response_model=dict)
async def create_job(job: JobCreate, db=Depends(get_database)):
    """Create a new job posting"""
    job_dict = job.model_dump()
    job_dict["created_at"] = datetime.utcnow()
    job_dict["updated_at"] = datetime.utcnow()
    job_dict["status"] = "active"
    
    result = await db.jobs.insert_one(job_dict)
    
    return {
        "id": str(result.inserted_id),
        "message": "Job created successfully"
    }


@router.get("/{job_id}")
async def get_job(job_id: str, db=Depends(get_database)):
    """Get job by ID"""
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job["id"] = str(job["_id"])
        del job["_id"]
        return job
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def list_jobs(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = "active",
    skills: Optional[str] = None,
    db=Depends(get_database)
):
    """List all jobs with optional filtering"""
    query = {}
    
    if status:
        query["status"] = status
    
    if skills:
        skill_list = [s.strip() for s in skills.split(",")]
        query["required_skills"] = {"$in": skill_list}
    
    cursor = db.jobs.find(query).skip(skip).limit(limit).sort("created_at", -1)
    jobs = await cursor.to_list(length=limit)
    
    for job in jobs:
        job["id"] = str(job["_id"])
        del job["_id"]
    
    return {
        "total": await db.jobs.count_documents(query),
        "jobs": jobs
    }


@router.put("/{job_id}")
async def update_job(
    job_id: str,
    job: JobCreate,
    db=Depends(get_database)
):
    """Update job information"""
    job_dict = job.model_dump()
    job_dict["updated_at"] = datetime.utcnow()
    
    try:
        result = await db.jobs.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": job_dict}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": "Job updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{job_id}/status")
async def update_job_status(
    job_id: str,
    status: str,
    db=Depends(get_database)
):
    """Update job status (active, closed, draft)"""
    if status not in ["active", "closed", "draft"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    try:
        result = await db.jobs.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"status": status, "updated_at": datetime.utcnow()}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": f"Job status updated to {status}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{job_id}")
async def delete_job(job_id: str, db=Depends(get_database)):
    """Delete a job"""
    try:
        result = await db.jobs.delete_one({"_id": ObjectId(job_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": "Job deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
