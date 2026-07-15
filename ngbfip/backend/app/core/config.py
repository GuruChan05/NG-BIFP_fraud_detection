from pydantic_settings import BaseSettings
from typing import List
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Application
    APP_NAME: str = "NG-BIFP Fraud Detection"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://bifp_user:bifp_password@postgres:5432/ng_bifp"
    SQLALCHEMY_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    DATABASE_POOL_RECYCLE: int = 3600
    
    # Security
    SECRET_KEY: str = "change-this-to-a-random-32-character-string-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_LOG_ROUNDS: int = 12
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # ML Configuration
    ML_MODEL_PATH: str = "models/"
    FRAUD_DETECTION_CONTAMINATION: float = 0.1
    
    # Feature Flags
    ENABLE_AUDIT_LOGGING: bool = True
    ENABLE_ML_INFERENCE: bool = True
    ENABLE_NOTIFICATIONS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **data):
        super().__init__(**data)
        # Validate SECRET_KEY length
        if len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        # Create models directory if it doesn't exist
        os.makedirs(self.ML_MODEL_PATH, exist_ok=True)

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

settings = get_settings()
