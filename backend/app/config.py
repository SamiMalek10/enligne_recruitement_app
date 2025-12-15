from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Recruitment Application"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "recruitment_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # ML Settings
    ML_MODEL_PATH: str = "./models"
    MATCHING_THRESHOLD: float = 0.5
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".txt"}
    
    # Analytics
    ANALYTICS_BATCH_SIZE: int = 1000
    
    class Config:
        env_file = ".env"


settings = Settings()
