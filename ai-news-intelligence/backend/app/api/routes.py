"""REST API routes"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models import Article, SearchQuery
from app.schemas.schemas import (
    ArticleResponse, QueryRequest, RAGResponse, SummarizeRequest, SentimentAnalysisResponse,
    TrendingTopicsResponse, HeadlinesResponse, ErrorResponse
)
from app.rag.pipeline import retriever
from app.rag.llm import rag_engine
from app.nlp.processors import SentimentAnalyzer, TrendAnalyzer
from app.core.logging import logger
from app.core.exceptions import NoRelevantDocumentsFound
import uuid

router = APIRouter(prefix="/api", tags=["news"])


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


@router.get("/news/headlines", response_model=HeadlinesResponse)
async def get_headlines(
    category: str = Query("general", description="News category"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top headlines by category"""
    try:
        skip = (page - 1) * page_size
        
        query = db.query(Article)
        if category and category != "all":
            query = query.filter(Article.category == category)
        
        total_count = query.count()
        articles = query.order_by(desc(Article.published_at)).offset(skip).limit(page_size).all()
        
        return HeadlinesResponse(
            articles=[ArticleResponse.from_orm(a) for a in articles],
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Failed to fetch headlines: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch headlines")


@router.get("/news/category/{category}", response_model=HeadlinesResponse)
async def get_news_by_category(
    category: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get news articles by category"""
    try:
        skip = (page - 1) * page_size
        
        query = db.query(Article).filter(Article.category == category)
        total_count = query.count()
        articles = query.order_by(desc(Article.published_at)).offset(skip).limit(page_size).all()
        
        return HeadlinesResponse(
            articles=[ArticleResponse.from_orm(a) for a in articles],
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Failed to fetch category news: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch news")


@router.post("/ai/query", response_model=RAGResponse)
async def query_with_rag(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """Answer question using RAG"""
    try:
        if not rag_engine or not retriever:
            raise HTTPException(status_code=500, detail="RAG engine not initialized")
        
        start_time = datetime.utcnow()
        
        # Retrieve relevant documents
        try:
            retrieved_docs, scores = retriever.retrieve(
                request.query,
                top_k=5,
                similarity_threshold=0.3
            )
        except NoRelevantDocumentsFound:
            return RAGResponse(
                answer="No relevant information found in the available news sources.",
                sources=[],
                confidence_score=0.0,
                status="no_results"
            )
        
        # Fetch full articles
        articles = db.query(Article).filter(Article.id.in_(retrieved_docs)).all()
        
        # Format context for LLM
        context = "\n\n".join([
            f"Source: {a.source}\nTitle: {a.title}\nContent: {a.content[:500]}"
            for a in articles
        ])
        
        # Generate answer using LLM
        result = rag_engine.answer_query(request.query, context)
        
        # Log search query
        query_record = SearchQuery(
            id=str(uuid.uuid4()),
            query=request.query,
            result_count=len(articles),
            response_time_ms=(datetime.utcnow() - start_time).total_seconds() * 1000,
            cached=0
        )
        db.add(query_record)
        db.commit()
        
        return RAGResponse(
            answer=result["answer"],
            sources=[ArticleResponse.from_orm(a) for a in articles],
            confidence_score=result.get("confidence", 0.8),
            status=result["status"]
        )
    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        raise HTTPException(status_code=500, detail="Query processing failed")


@router.get("/news/search")
async def search_articles(
    q: str = Query(..., min_length=1, max_length=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search articles by keyword"""
    try:
        skip = (page - 1) * page_size
        
        # Simple full-text search
        query = db.query(Article).filter(
            (Article.title.ilike(f"%{q}%")) |
            (Article.content.ilike(f"%{q}%"))
        )
        
        total_count = query.count()
        articles = query.order_by(desc(Article.published_at)).offset(skip).limit(page_size).all()
        
        return HeadlinesResponse(
            articles=[ArticleResponse.from_orm(a) for a in articles],
            total_count=total_count,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/trending/topics", response_model=list[TrendingTopicsResponse])
async def get_trending_topics(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Get trending topics"""
    try:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        articles = db.query(Article).filter(
            Article.published_at >= cutoff_time
        ).all()
        
        trends = TrendAnalyzer.detect_trending_topics(
            [ArticleResponse.from_orm(a).model_dump() for a in articles],
            time_window_hours=hours
        )
        
        return trends
    except Exception as e:
        logger.error(f"Failed to fetch trending topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch trends")


@router.post("/ai/summarize", response_model=dict)
async def summarize_article(
    request: SummarizeRequest,
    db: Session = Depends(get_db)
):
    """Summarize an article"""
    try:
        if not rag_engine:
            raise HTTPException(status_code=500, detail="LLM engine not initialized")
        
        article = db.query(Article).filter(Article.id == request.article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Use cached summary if available
        if article.summary:
            return {
                "article_id": article.id,
                "summary": article.summary,
                "cached": True
            }
        
        # Generate summary
        summary = rag_engine.summarize_article(
            article.content,
            max_length=request.max_length or 300
        )
        
        # Cache summary
        article.summary = summary
        db.commit()
        
        return {
            "article_id": article.id,
            "summary": summary,
            "cached": False
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise HTTPException(status_code=500, detail="Summarization failed")


@router.get("/ai/sentiment/{article_id}", response_model=SentimentAnalysisResponse)
async def get_sentiment(
    article_id: str,
    db: Session = Depends(get_db)
):
    """Get sentiment analysis for article"""
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return SentimentAnalysisResponse(
            article_id=article.id,
            sentiment_score=article.sentiment_score or 0.0,
            sentiment_label=article.sentiment_label or "neutral",
            confidence=0.8
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Sentiment analysis failed")
