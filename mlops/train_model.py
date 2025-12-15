"""
MLOps - Model Training Pipeline
Train and save the matching model
"""

import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime
import os


def train_model():
    """Train the TF-IDF vectorizer on sample data"""
    
    # Sample training data (in real scenario, this would be from database)
    sample_texts = [
        "Python Machine Learning Data Science TensorFlow PyTorch",
        "Java Spring Boot Microservices Docker Kubernetes",
        "JavaScript React Node.js TypeScript Express",
        "DevOps AWS Azure Docker Kubernetes Jenkins CI/CD",
        "Big Data Spark Hadoop Kafka Hive Data Engineering",
        "Data Analyst SQL Power BI Tableau Python",
        "Full Stack Developer React Django PostgreSQL",
        "Mobile Developer Swift Kotlin Android iOS",
        "Security Engineer Cybersecurity Penetration Testing",
        "Cloud Architect AWS Azure GCP Terraform"
    ]
    
    # Create and fit vectorizer
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        stop_words='english'
    )
    
    vectorizer.fit(sample_texts)
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Save model
    model_path = f"models/tfidf_vectorizer_{datetime.now().strftime('%Y%m%d')}.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    
    # Save as default
    with open("models/tfidf_vectorizer.pkl", 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print(f"✅ Model trained and saved to {model_path}")
    print(f"📊 Vocabulary size: {len(vectorizer.vocabulary_)}")
    
    return vectorizer


if __name__ == "__main__":
    print("🚀 Starting MLOps Training Pipeline...")
    train_model()
    print("✅ Training completed!")
