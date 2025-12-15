from fastapi import APIRouter, HTTPException, Depends
from typing import List
from bson import ObjectId

from app.database import get_database, get_redis
from app.ml.matching_engine import MatchingEngine
import json

router = APIRouter(prefix="/api/matching", tags=["Matching"])
matching_engine = MatchingEngine()


@router.post("/score")
async def calculate_match_score(
    candidate_id: str,
    job_id: str,
    db=Depends(get_database)
):
    """Calculate match score between a candidate and a job"""
    
    # Get candidate
    try:
        candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Get job
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Calculate score
        score_data = matching_engine.calculate_match_score(candidate, job)
        
        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate.get("name"),
            "job_id": job_id,
            "job_title": job.get("title"),
            **score_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommend/{job_id}")
async def recommend_candidates_for_job(
    job_id: str,
    top_n: int = 10,
    min_score: float = 0.3,
    db=Depends(get_database),
    redis=Depends(get_redis)
):
    """Get top recommended candidates for a job"""
    
    # Check cache
    cache_key = f"job_recommendations:{job_id}:{top_n}:{min_score}"
    cached_result = redis.get(cache_key)
    
    if cached_result:
        return json.loads(cached_result)
    
    try:
        # Get job
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get all candidates
        candidates = await db.candidates.find().to_list(length=None)
        
        # Rank candidates
        ranked_candidates = matching_engine.rank_candidates(candidates, job, top_n=top_n)
        
        # Filter by minimum score and format results
        recommendations = []
        for candidate, score_data in ranked_candidates:
            if score_data['total_score'] >= min_score:
                recommendations.append({
                    "candidate_id": str(candidate["_id"]),
                    "name": candidate.get("name"),
                    "email": candidate.get("email"),
                    "skills": candidate.get("skills", []),
                    "experience_years": candidate.get("experience_years", 0),
                    **score_data
                })
        
        result = {
            "job_id": job_id,
            "job_title": job.get("title"),
            "total_candidates_evaluated": len(candidates),
            "recommendations": recommendations
        }
        
        # Cache result for 5 minutes
        redis.setex(cache_key, 300, json.dumps(result))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/jobs-for-candidate/{candidate_id}")
async def recommend_jobs_for_candidate(
    candidate_id: str,
    top_n: int = 10,
    min_score: float = 0.3,
    db=Depends(get_database),
    redis=Depends(get_redis)
):
    """Get top recommended jobs for a candidate"""
    
    # Check cache
    cache_key = f"candidate_recommendations:{candidate_id}:{top_n}:{min_score}"
    cached_result = redis.get(cache_key)
    
    if cached_result:
        return json.loads(cached_result)
    
    try:
        # Get candidate
        candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Get active jobs
        jobs = await db.jobs.find({"status": "active"}).to_list(length=None)
        
        # Recommend jobs
        recommended_jobs = matching_engine.recommend_jobs(candidate, jobs, top_n=top_n)
        
        # Filter by minimum score and format results
        recommendations = []
        for job, score_data in recommended_jobs:
            if score_data['total_score'] >= min_score:
                recommendations.append({
                    "job_id": str(job["_id"]),
                    "title": job.get("title"),
                    "company": job.get("company"),
                    "required_skills": job.get("required_skills", []),
                    "min_experience": job.get("min_experience", 0),
                    "location": job.get("location"),
                    "remote": job.get("remote", False),
                    **score_data
                })
        
        result = {
            "candidate_id": candidate_id,
            "candidate_name": candidate.get("name"),
            "total_jobs_evaluated": len(jobs),
            "recommendations": recommendations
        }
        
        # Cache result for 5 minutes
        redis.setex(cache_key, 300, json.dumps(result))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/batch-match")
async def batch_match_candidates(
    job_id: str,
    candidate_ids: List[str],
    db=Depends(get_database)
):
    """Calculate match scores for multiple candidates in batch"""
    
    try:
        # Get job
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        results = []
        for candidate_id in candidate_ids:
            try:
                candidate = await db.candidates.find_one({"_id": ObjectId(candidate_id)})
                if candidate:
                    score_data = matching_engine.calculate_match_score(candidate, job)
                    results.append({
                        "candidate_id": candidate_id,
                        "name": candidate.get("name"),
                        **score_data
                    })
            except:
                continue
        
        # Sort by score
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return {
            "job_id": job_id,
            "job_title": job.get("title"),
            "total_evaluated": len(results),
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
