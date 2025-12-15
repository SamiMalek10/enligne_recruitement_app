"""
Sample data generator for testing
"""

import requests
import random

API_URL = "http://localhost:8000"

# Sample data
NAMES = ["Alice Martin", "Bob Dubois", "Claire Petit", "David Bernard", "Emma Durand",
         "François Simon", "Gabriel Laurent", "Hélène Michel", "Ivan Lefebvre", "Julie Moreau"]

SKILLS_POOL = [
    ["Python", "Django", "PostgreSQL", "Docker"],
    ["Java", "Spring Boot", "Kubernetes", "AWS"],
    ["JavaScript", "React", "Node.js", "MongoDB"],
    ["Python", "Machine Learning", "TensorFlow", "Pandas"],
    ["DevOps", "Docker", "Kubernetes", "Jenkins", "Terraform"],
    ["Big Data", "Spark", "Hadoop", "Kafka", "Hive"],
    ["Data Analyst", "SQL", "Power BI", "Python", "Excel"],
    ["Full Stack", "React", "Django", "PostgreSQL", "Redis"],
    ["Cloud", "AWS", "Azure", "Terraform", "Ansible"],
    ["Security", "Cybersecurity", "Penetration Testing", "SIEM"]
]

JOB_TITLES = [
    ("Data Engineer", ["Python", "Spark", "Kafka", "Docker", "Airflow"]),
    ("Full Stack Developer", ["React", "Node.js", "MongoDB", "Docker"]),
    ("DevOps Engineer", ["Kubernetes", "Docker", "Jenkins", "AWS", "Terraform"]),
    ("ML Engineer", ["Python", "TensorFlow", "MLflow", "Docker", "Kubernetes"]),
    ("Backend Developer", ["Java", "Spring Boot", "PostgreSQL", "Redis"]),
    ("Cloud Architect", ["AWS", "Azure", "Terraform", "Kubernetes"]),
    ("Data Scientist", ["Python", "Machine Learning", "Pandas", "SQL"]),
    ("Frontend Developer", ["React", "TypeScript", "CSS", "JavaScript"]),
]


def create_sample_candidates(n=10):
    """Create sample candidates"""
    print(f"Creating {n} sample candidates...")
    
    for i in range(n):
        candidate = {
            "name": NAMES[i % len(NAMES)] + f" {i+1}",
            "email": f"candidate{i+1}@example.com",
            "phone": f"+33612345{i:03d}",
            "skills": random.choice(SKILLS_POOL),
            "experience_years": random.randint(0, 15),
            "location": random.choice(["Paris", "Lyon", "Marseille", "Toulouse"]),
            "education": random.choice(["Bachelor", "Master", "PhD"])
        }
        
        try:
            response = requests.post(f"{API_URL}/api/candidates/", json=candidate)
            if response.status_code == 200:
                print(f"✅ Created: {candidate['name']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")


def create_sample_jobs(n=8):
    """Create sample jobs"""
    print(f"\nCreating {n} sample jobs...")
    
    for i in range(n):
        title, skills = JOB_TITLES[i % len(JOB_TITLES)]
        
        job = {
            "title": title,
            "company": random.choice(["TechCorp", "DataSoft", "CloudVentures", "AILabs"]),
            "description": f"We are looking for a talented {title} to join our team. This role involves working with cutting-edge technologies and solving complex problems.",
            "required_skills": skills,
            "nice_to_have_skills": random.sample(["Agile", "Scrum", "Git", "CI/CD", "Testing"], 2),
            "min_experience": random.choice([0, 2, 3, 5, 8]),
            "location": random.choice(["Paris", "Remote", "Lyon"]),
            "remote": random.choice([True, False]),
            "job_type": "Full-time"
        }
        
        try:
            response = requests.post(f"{API_URL}/api/jobs/", json=job)
            if response.status_code == 200:
                print(f"✅ Created: {job['title']} at {job['company']}")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Exception: {e}")


if __name__ == "__main__":
    print("🚀 Generating sample data...")
    print("=" * 60)
    
    create_sample_candidates(10)
    create_sample_jobs(8)
    
    print("=" * 60)
    print("✅ Sample data generation completed!")
    print("\n📊 You can now:")
    print("  - View dashboard: http://localhost:3000")
    print("  - Check API docs: http://localhost:8000/docs")
    print("  - Run analytics: python analytics/batch_analytics.py")
