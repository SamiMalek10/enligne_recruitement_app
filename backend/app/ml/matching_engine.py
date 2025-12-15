from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Tuple
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class MatchingEngine:
    """ML-based matching engine for candidates and jobs"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            stop_words='english'
        )
        # Download NLTK data if not present
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            nltk.download('punkt')
            self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for matching"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords
        tokens = [word for word in tokens if word not in self.stop_words]
        
        return ' '.join(tokens)
    
    def calculate_skill_match(self, 
                            candidate_skills: List[str], 
                            required_skills: List[str],
                            nice_to_have_skills: List[str] = None) -> float:
        """Calculate skill match percentage"""
        if not required_skills:
            return 0.0
        
        candidate_skills_lower = [s.lower() for s in candidate_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        # Required skills match
        required_match = sum(1 for skill in required_skills_lower 
                           if skill in candidate_skills_lower)
        required_score = required_match / len(required_skills_lower) if required_skills_lower else 0
        
        # Nice-to-have skills match (bonus)
        bonus_score = 0
        if nice_to_have_skills:
            nice_to_have_lower = [s.lower() for s in nice_to_have_skills]
            nice_match = sum(1 for skill in nice_to_have_lower 
                           if skill in candidate_skills_lower)
            bonus_score = (nice_match / len(nice_to_have_lower)) * 0.2 if nice_to_have_lower else 0
        
        return min(required_score + bonus_score, 1.0)
    
    def calculate_experience_match(self, 
                                  candidate_exp: int,
                                  required_exp: int,
                                  max_exp: int = None) -> float:
        """Calculate experience match score"""
        if candidate_exp >= required_exp:
            if max_exp and candidate_exp > max_exp + 3:
                # Overqualified penalty
                return 0.8
            return 1.0
        else:
            # Underqualified
            diff = required_exp - candidate_exp
            if diff <= 1:
                return 0.8
            elif diff <= 2:
                return 0.6
            else:
                return 0.3
    
    def calculate_text_similarity(self, 
                                 text1: str, 
                                 text2: str) -> float:
        """Calculate text similarity using TF-IDF and cosine similarity"""
        if not text1 or not text2:
            return 0.0
        
        # Preprocess texts
        text1_clean = self.preprocess_text(text1)
        text2_clean = self.preprocess_text(text2)
        
        try:
            # Calculate TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([text1_clean, text2_clean])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except:
            return 0.0
    
    def calculate_match_score(self,
                            candidate_data: Dict,
                            job_data: Dict) -> Dict:
        """Calculate comprehensive match score between candidate and job"""
        
        # 1. Skill match (40% weight)
        skill_score = self.calculate_skill_match(
            candidate_data.get('skills', []),
            job_data.get('required_skills', []),
            job_data.get('nice_to_have_skills', [])
        )
        
        # 2. Experience match (30% weight)
        exp_score = self.calculate_experience_match(
            candidate_data.get('experience_years', 0),
            job_data.get('min_experience', 0),
            job_data.get('max_experience')
        )
        
        # 3. Text similarity - CV vs Job Description (30% weight)
        text_similarity = self.calculate_text_similarity(
            candidate_data.get('cv_text', ''),
            job_data.get('description', '')
        )
        
        # Calculate weighted total score
        total_score = (
            skill_score * 0.4 +
            exp_score * 0.3 +
            text_similarity * 0.3
        )
        
        return {
            'total_score': round(total_score, 3),
            'skill_match': round(skill_score, 3),
            'experience_match': round(exp_score, 3),
            'text_similarity': round(text_similarity, 3),
            'is_recommended': total_score >= 0.6
        }
    
    def rank_candidates(self, 
                       candidates: List[Dict],
                       job_data: Dict,
                       top_n: int = 10) -> List[Tuple[Dict, Dict]]:
        """Rank candidates for a job"""
        scored_candidates = []
        
        for candidate in candidates:
            score_data = self.calculate_match_score(candidate, job_data)
            scored_candidates.append((candidate, score_data))
        
        # Sort by total score descending
        scored_candidates.sort(key=lambda x: x[1]['total_score'], reverse=True)
        
        return scored_candidates[:top_n]
    
    def recommend_jobs(self,
                      candidate_data: Dict,
                      jobs: List[Dict],
                      top_n: int = 10) -> List[Tuple[Dict, Dict]]:
        """Recommend jobs for a candidate"""
        scored_jobs = []
        
        for job in jobs:
            score_data = self.calculate_match_score(candidate_data, job)
            scored_jobs.append((job, score_data))
        
        # Sort by total score descending
        scored_jobs.sort(key=lambda x: x[1]['total_score'], reverse=True)
        
        return scored_jobs[:top_n]
