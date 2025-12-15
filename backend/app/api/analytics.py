from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from datetime import datetime, timedelta
from bson import ObjectId
import pandas as pd

from app.database import get_database, get_redis
import json

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard_stats(db=Depends(get_database)):
    """Get dashboard statistics"""
    
    # Total counts
    total_candidates = await db.candidates.count_documents({})
    total_jobs = await db.jobs.count_documents({})
    active_jobs = await db.jobs.count_documents({"status": "active"})
    
    # Recent stats (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_candidates = await db.candidates.count_documents({
        "created_at": {"$gte": thirty_days_ago}
    })
    recent_jobs = await db.jobs.count_documents({
        "created_at": {"$gte": thirty_days_ago}
    })
    
    # Average experience
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_experience": {"$avg": "$experience_years"}
        }}
    ]
    avg_exp_result = await db.candidates.aggregate(pipeline).to_list(length=1)
    avg_experience = avg_exp_result[0]["avg_experience"] if avg_exp_result else 0
    
    return {
        "total_candidates": total_candidates,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "recent_candidates_30d": recent_candidates,
        "recent_jobs_30d": recent_jobs,
        "average_experience_years": round(avg_experience, 2),
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/skills-trends")
async def get_skills_trends(
    limit: int = 20,
    db=Depends(get_database),
    redis=Depends(get_redis)
):
    """Get trending skills from jobs and candidates"""
    
    cache_key = "skills_trends"
    cached_result = redis.get(cache_key)
    
    if cached_result:
        return json.loads(cached_result)
    
    # Skills from jobs (demand)
    jobs_pipeline = [
        {"$unwind": "$required_skills"},
        {"$group": {
            "_id": "$required_skills",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    
    job_skills = await db.jobs.aggregate(jobs_pipeline).to_list(length=limit)
    
    # Skills from candidates (supply)
    candidates_pipeline = [
        {"$unwind": "$skills"},
        {"$group": {
            "_id": "$skills",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    
    candidate_skills = await db.candidates.aggregate(candidates_pipeline).to_list(length=limit)
    
    result = {
        "most_demanded_skills": [
            {"skill": item["_id"], "jobs_count": item["count"]}
            for item in job_skills
        ],
        "most_common_candidate_skills": [
            {"skill": item["_id"], "candidates_count": item["count"]}
            for item in candidate_skills
        ],
        "last_updated": datetime.utcnow().isoformat()
    }
    
    # Cache for 1 hour
    redis.setex(cache_key, 3600, json.dumps(result))
    
    return result


@router.get("/hiring-metrics")
async def get_hiring_metrics(db=Depends(get_database)):
    """Get hiring metrics and trends"""
    
    # Jobs by status
    status_pipeline = [
        {"$group": {
            "_id": "$status",
            "count": {"$sum": 1}
        }}
    ]
    
    jobs_by_status = await db.jobs.aggregate(status_pipeline).to_list(length=10)
    
    # Jobs by experience level
    exp_pipeline = [
        {"$bucket": {
            "groupBy": "$min_experience",
            "boundaries": [0, 2, 5, 8, 15],
            "default": "15+",
            "output": {
                "count": {"$sum": 1}
            }
        }}
    ]
    
    jobs_by_exp = await db.jobs.aggregate(exp_pipeline).to_list(length=10)
    
    # Candidate distribution by experience
    candidate_exp_pipeline = [
        {"$bucket": {
            "groupBy": "$experience_years",
            "boundaries": [0, 2, 5, 8, 15],
            "default": "15+",
            "output": {
                "count": {"$sum": 1}
            }
        }}
    ]
    
    candidates_by_exp = await db.candidates.aggregate(candidate_exp_pipeline).to_list(length=10)
    
    # Remote vs On-site jobs
    remote_stats = await db.jobs.aggregate([
        {"$group": {
            "_id": "$remote",
            "count": {"$sum": 1}
        }}
    ]).to_list(length=10)
    
    return {
        "jobs_by_status": {
            item["_id"]: item["count"] for item in jobs_by_status
        },
        "jobs_by_experience_level": jobs_by_exp,
        "candidates_by_experience_level": candidates_by_exp,
        "remote_vs_onsite": {
            "remote": next((item["count"] for item in remote_stats if item["_id"]), 0),
            "onsite": next((item["count"] for item in remote_stats if not item["_id"]), 0)
        },
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/skills-gap")
async def analyze_skills_gap(db=Depends(get_database)):
    """Analyze skills gap between demand and supply"""
    
    # Get all required skills from jobs
    job_skills_pipeline = [
        {"$match": {"status": "active"}},
        {"$unwind": "$required_skills"},
        {"$group": {
            "_id": "$required_skills",
            "demand": {"$sum": 1}
        }}
    ]
    
    job_skills = await db.jobs.aggregate(job_skills_pipeline).to_list(length=None)
    job_skills_dict = {item["_id"]: item["demand"] for item in job_skills}
    
    # Get all skills from candidates
    candidate_skills_pipeline = [
        {"$unwind": "$skills"},
        {"$group": {
            "_id": "$skills",
            "supply": {"$sum": 1}
        }}
    ]
    
    candidate_skills = await db.candidates.aggregate(candidate_skills_pipeline).to_list(length=None)
    candidate_skills_dict = {item["_id"]: item["supply"] for item in candidate_skills}
    
    # Calculate gap
    all_skills = set(job_skills_dict.keys()) | set(candidate_skills_dict.keys())
    
    skills_analysis = []
    for skill in all_skills:
        demand = job_skills_dict.get(skill, 0)
        supply = candidate_skills_dict.get(skill, 0)
        gap = demand - supply
        gap_percentage = (gap / demand * 100) if demand > 0 else 0
        
        skills_analysis.append({
            "skill": skill,
            "demand": demand,
            "supply": supply,
            "gap": gap,
            "gap_percentage": round(gap_percentage, 2),
            "status": "shortage" if gap > 0 else "surplus" if gap < 0 else "balanced"
        })
    
    # Sort by gap (highest shortage first)
    skills_analysis.sort(key=lambda x: x["gap"], reverse=True)
    
    return {
        "skills_gap_analysis": skills_analysis,
        "high_demand_low_supply": [s for s in skills_analysis if s["gap"] > 5][:10],
        "last_updated": datetime.utcnow().isoformat()
    }


@router.get("/company-stats/{company_name}")
async def get_company_stats(company_name: str, db=Depends(get_database)):
    """Get statistics for a specific company"""
    
    total_jobs = await db.jobs.count_documents({"company": company_name})
    active_jobs = await db.jobs.count_documents({"company": company_name, "status": "active"})
    
    # Most required skills for this company
    skills_pipeline = [
        {"$match": {"company": company_name}},
        {"$unwind": "$required_skills"},
        {"$group": {
            "_id": "$required_skills",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    
    top_skills = await db.jobs.aggregate(skills_pipeline).to_list(length=10)
    
    return {
        "company": company_name,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "top_required_skills": [
            {"skill": item["_id"], "count": item["count"]}
            for item in top_skills
        ]
    }
