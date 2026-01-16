"""Pydantic schemas for request/response validation"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any


class ArticleBase(BaseModel):
    """Base article schema"""
    title: str
    content: Optional[str] = None
    source: str
    category: Optional[str] = None
    url: str
    published_at: Optional[datetime] = None


class ArticleCreate(ArticleBase):
    """Schema for creating articles"""
    pass


class ArticleResponse(ArticleBase):
    """Schema for article responses"""
    id: str
    summary: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    main_topic: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class QueryRequest(BaseModel):
    """Schema for user queries"""
    query: str = Field(..., min_length=3, max_length=1000)
    category: Optional[str] = None


class RAGResponse(BaseModel):
    """Schema for RAG query responses"""
    answer: str
    sources: List[ArticleResponse]
    confidence_score: Optional[float] = None
    status: str = "success"


class SummarizeRequest(BaseModel):
    """Schema for summarization requests"""
    article_id: str
    max_length: Optional[int] = 300


class SummarizeResponse(BaseModel):
    """Schema for summarization responses"""
    article_id: str
    summary: str
    original_length: int
    summary_length: int


class SentimentAnalysisResponse(BaseModel):
    """Schema for sentiment analysis response"""
    article_id: str
    sentiment_score: float
    sentiment_label: str
    confidence: float


class TrendingTopicsResponse(BaseModel):
    """Schema for trending topics"""
    topic: str
    frequency: int
    sentiment_avg: float
    articles_count: int
    period: str = "24h"


class HeadlinesResponse(BaseModel):
    """Schema for headlines response"""
    articles: List[ArticleResponse]
    total_count: int
    page: int
    page_size: int


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    status: str = "error"
    detail: str
    error_code: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Schema for health check"""
    status: str
    version: str
    timestamp: datetime
