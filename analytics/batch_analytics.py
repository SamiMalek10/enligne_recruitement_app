"""
Analytics - Big Data Analysis Scripts
Batch processing and reporting
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
from datetime import datetime
import json


async def analyze_recruitment_trends():
    """Analyze recruitment trends using pandas"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://127.0.0.1:27017")
    db = client["recruitment_db"]
    
    # 🔍 Debug info
    print(f"🔗 Connected to: {client.address}")
    print(f"📦 Using database: {db.name}")
    
    # Fetch data
    candidates = await db.candidates.find().to_list(length=None)
    jobs = await db.jobs.find().to_list(length=None)
    
    # 📊 Count check
    count_cand = len(candidates)
    count_jobs = len(jobs)
    print(f"📊 Total Candidates: {count_cand}")
    print(f"💼 Total Jobs: {count_jobs}")
    
    # Convert to DataFrames
    candidates_df = pd.DataFrame(candidates)
    jobs_df = pd.DataFrame(jobs)
    
    print("=" * 60)
    print("📊 BIG DATA ANALYTICS REPORT")
    print("=" * 60)
    
    # Candidates Analysis
    print("\n🎯 CANDIDATES ANALYSIS")
    print(f"Total Candidates: {len(candidates_df)}")
    
    if len(candidates_df) > 0:
        print(f"Average Experience: {candidates_df['experience_years'].mean():.2f} years")
        print(f"Max Experience: {candidates_df['experience_years'].max()} years")
        
        # Top skills
        all_skills = []
        for skills in candidates_df['skills']:
            all_skills.extend(skills)
        
        skills_series = pd.Series(all_skills)
        top_skills = skills_series.value_counts().head(10)
        
        print("\nTop 10 Candidate Skills:")
        for skill, count in top_skills.items():
            print(f"  {skill}: {count}")
    
    # Jobs Analysis
    print("\n💼 JOBS ANALYSIS")
    print(f"Total Jobs: {len(jobs_df)}")
    
    if len(jobs_df) > 0:
        print(f"Active Jobs: {len(jobs_df[jobs_df['status'] == 'active'])}")
        
        # Required skills
        all_req_skills = []
        for skills in jobs_df['required_skills']:
            all_req_skills.extend(skills)
        
        req_skills_series = pd.Series(all_req_skills)
        top_req_skills = req_skills_series.value_counts().head(10)
        
        print("\nTop 10 Required Skills:")
        for skill, count in top_req_skills.items():
            print(f"  {skill}: {count}")
    
    # Skills Gap Analysis
    print("\n⚠️ SKILLS GAP ANALYSIS")
    if len(candidates_df) > 0 and len(jobs_df) > 0:
        candidate_skills = set(all_skills)
        required_skills = set(all_req_skills)
        
        high_demand = required_skills - candidate_skills
        if high_demand:
            print("High demand, low supply skills:")
            for skill in list(high_demand)[:10]:
                print(f"  ⚡ {skill}")
    
    # Time series analysis
    print("\n📈 TREND ANALYSIS")
    if len(candidates_df) > 0:
        candidates_df['created_at'] = pd.to_datetime(candidates_df['created_at'])
        candidates_df['month'] = candidates_df['created_at'].dt.to_period('M')
        
        monthly_candidates = candidates_df.groupby('month').size()
        print("\nCandidates per month:")
        for month, count in monthly_candidates.items():
            print(f"  {month}: {count}")
    
    print("\n" + "=" * 60)
    
    # Save report
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_candidates": len(candidates_df),
        "total_jobs": len(jobs_df),
        "top_candidate_skills": top_skills.to_dict() if len(candidates_df) > 0 else {},
        "top_required_skills": top_req_skills.to_dict() if len(jobs_df) > 0 else {}
    }
    
    with open("analytics_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("📄 Report saved to analytics_report.json")

    # ✅ Supprimé : client.close() — inutile ici


if __name__ == "__main__":
    print("🚀 Starting Big Data Analytics Pipeline...")
    asyncio.run(analyze_recruitment_trends())
    print("✅ Analysis completed!")