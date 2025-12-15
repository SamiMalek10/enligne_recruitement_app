import re
import os
from typing import Optional
from pathlib import Path
import PyPDF2
from docx import Document


class CVParser:
    """Parse CV files and extract text"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error extracting TXT: {e}")
            return ""
    
    @classmethod
    def parse_cv(cls, file_path: str) -> str:
        """Parse CV and extract text based on file type"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return cls.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return cls.extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            return cls.extract_text_from_txt(file_path)
        else:
            return ""
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from text"""
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None
    
    @staticmethod
    def extract_skills(text: str, skill_list: list) -> list:
        """Extract skills from text based on known skill list"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_list:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return list(set(found_skills))


# Common skills database
COMMON_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "PHP", "Ruby",
    "Scala", "Kotlin", "Swift", "R", "MATLAB", "SQL", "HTML", "CSS",
    
    # Frameworks & Libraries
    "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI", "Spring", "Node.js",
    "Express", "ASP.NET", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
    
    # Big Data & Analytics
    "Hadoop", "Spark", "Kafka", "Flink", "Storm", "Hive", "Pig", "HBase",
    "Cassandra", "MongoDB", "Redis", "Elasticsearch", "Tableau", "Power BI",
    
    # DevOps & Cloud
    "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions", "Terraform",
    "Ansible", "AWS", "Azure", "GCP", "Prometheus", "Grafana", "ELK Stack",
    
    # MLOps & Data Science
    "MLflow", "Kubeflow", "Airflow", "DVC", "Weights & Biases", "Machine Learning",
    "Deep Learning", "NLP", "Computer Vision", "Data Mining", "Statistical Analysis",
    
    # Databases
    "PostgreSQL", "MySQL", "Oracle", "SQL Server", "MongoDB", "DynamoDB",
    "Neo4j", "InfluxDB", "Snowflake",
    
    # Soft Skills
    "Leadership", "Communication", "Team Work", "Problem Solving", "Agile", "Scrum"
]
