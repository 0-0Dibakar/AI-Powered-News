"""Database models for news articles and metadata"""

from sqlalchemy import Column, String, Text, DateTime, Float, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Article(Base):
    """News article model"""
    __tablename__ = "articles"
    
    id = Column(String(255), primary_key=True)
    url = Column(String(2048), unique=True, nullable=False)
    title = Column(String(1024), nullable=False)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    source = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # NLP extracted features
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    sentiment_label = Column(String(20), nullable=True)  # positive, negative, neutral
    main_topic = Column(String(100), nullable=True)
    entities = Column(Text, nullable=True)  # JSON: {person, location, org, ...}
    
    # Vector DB reference
    embedding_id = Column(String(255), nullable=True)
    
    __table_args__ = (
        Index("idx_source", "source"),
        Index("idx_category", "category"),
        Index("idx_published_at", "published_at"),
        Index("idx_created_at", "created_at"),
    )


class Chunk(Base):
    """Article chunks for RAG (300-500 tokens each)"""
    __tablename__ = "chunks"
    
    id = Column(String(255), primary_key=True)
    article_id = Column(String(255), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    embedding_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_article_id", "article_id"),
    )


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_email", "email"),
        Index("idx_username", "username"),
    )


class SearchQuery(Base):
    """Track user search queries for analytics and caching"""
    __tablename__ = "search_queries"
    
    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), nullable=True)
    query = Column(Text, nullable=False)
    result_count = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    cached = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_user_id", "user_id"),
        Index("idx_created_at", "created_at"),
    )
