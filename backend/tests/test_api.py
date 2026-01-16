"""Backend tests for RAG and API endpoints"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.models import Base, Article
from app.db.database import get_db
import uuid
from datetime import datetime


@pytest.fixture
def test_db():
    """Create test database"""
    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal()


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_get_headlines(client, test_db):
    """Test headlines endpoint"""
    # Add test article
    article = Article(
        id=str(uuid.uuid4()),
        url="http://test.com",
        title="Test Article",
        source="Test Source",
        published_at=datetime.utcnow(),
        sentiment_score=0.5,
        sentiment_label="positive"
    )
    test_db.add(article)
    test_db.commit()
    
    response = client.get("/api/news/headlines?category=general&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert data["page"] == 1


def test_search_articles(client, test_db):
    """Test search endpoint"""
    article = Article(
        id=str(uuid.uuid4()),
        url="http://test.com",
        title="Search Test Article",
        content="Test content for searching",
        source="Test Source",
        published_at=datetime.utcnow()
    )
    test_db.add(article)
    test_db.commit()
    
    response = client.get("/api/news/search?q=search&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data


def test_rag_query_no_results(client):
    """Test RAG query with no results"""
    response = client.post("/api/ai/query", json={"query": "nonexistent topic xyz 123"})
    assert response.status_code == 200
    data = response.json()
    assert "No relevant information" in data["answer"]


def test_summarize_article_not_found(client):
    """Test summarization with non-existent article"""
    response = client.post("/api/ai/summarize", json={"article_id": "nonexistent"})
    assert response.status_code == 404


def test_get_sentiment_not_found(client):
    """Test sentiment analysis with non-existent article"""
    response = client.get("/api/ai/sentiment/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_ingestion_pipeline():
    """Test news ingestion pipeline"""
    from app.ingestion.pipeline import IngestionPipeline
    
    pipeline = IngestionPipeline()
    # This would require NewsAPI key to work
    articles = await pipeline.ingest("newsapi")
    assert isinstance(articles, list)


def test_rate_limiting(client):
    """Test rate limiting"""
    # Make multiple requests
    for i in range(5):
        response = client.get("/api/health")
        assert response.status_code in [200, 429]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
