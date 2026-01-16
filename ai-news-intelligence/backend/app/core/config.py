"""Application configuration management"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "AI News Intelligence"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/news_db"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hour
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    NEWSAPI_KEY: Optional[str] = None
    GUARDIAN_API_KEY: Optional[str] = None
    
    # LLM Configuration
    LLM_MODEL: str = "gpt-3.5-turbo"  # or "llama-2-13b" for local
    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 500
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DEVICE: str = "cpu"  # or "cuda" for GPU
    
    # Vector DB
    VECTOR_DB_PATH: str = "./data/faiss_index"
    VECTOR_SIMILARITY_THRESHOLD: float = 0.5
    
    # RAG Configuration
    RAG_TOP_K: int = 5
    CHUNK_SIZE: int = 400
    CHUNK_OVERLAP: int = 50
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    
    # News Ingestion
    INGESTION_BATCH_SIZE: int = 100
    INGESTION_INTERVAL_MINUTES: int = 60
    NEWS_SOURCES: str = "newsapi,guardian,bbc"
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
