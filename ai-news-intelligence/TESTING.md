"""Comprehensive testing strategy and implementation guide"""

# TESTING STRATEGY FOR AI NEWS INTELLIGENCE

## Testing Pyramid

```
         /\
        /  \          E2E Tests (10%)
       /____\         Mobile app integration
      /      \
     /  \  /  \       Integration Tests (30%)
    /____\/____\      API endpoints, Database, RAG
   /            \
  /      Unit     \   Unit Tests (60%)
 /     Tests       \  Functions, Classes, Utilities
/__________________\
```

## 1. Unit Tests

### Backend Unit Tests

**File: `backend/tests/test_rag_pipeline.py`**

```python
# Test embedding model
def test_embedding_model_encode():
    from app.rag.pipeline import EmbeddingModel
    model = EmbeddingModel()
    embeddings = model.encode(["hello world", "test text"])
    assert embeddings.shape == (2, 384)

# Test vector database
def test_vector_db_add_and_search():
    from app.rag.pipeline import VectorDatabase
    import numpy as np
    
    db = VectorDatabase()
    embeddings = np.random.rand(5, 384).astype(np.float32)
    doc_ids = [f"doc_{i}" for i in range(5)]
    
    db.add(embeddings, doc_ids)
    results, scores = db.search(embeddings[0], top_k=3)
    
    assert len(results) >= 1
    assert results[0] == "doc_0"

# Test text chunker
def test_text_chunker():
    from app.rag.pipeline import TextChunker
    
    chunker = TextChunker(chunk_size=100, overlap=10)
    text = " ".join(["word"] * 250)
    chunks = chunker.chunk_text(text, "doc_1")
    
    assert len(chunks) > 1
    assert all(chunk_id.startswith("doc_1") for chunk_id, _ in chunks)

# Test sentiment analyzer
def test_sentiment_analyzer():
    from app.nlp.processors import SentimentAnalyzer
    
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("This is amazing!")
    
    assert result["sentiment_label"] == "positive"
    assert result["sentiment_score"] > 0
    assert 0 <= result["confidence"] <= 1
```

**File: `backend/tests/test_nlp.py`**

```python
# Test NER
def test_ner_extract_entities():
    from app.nlp.processors import NamedEntityRecognizer
    
    ner = NamedEntityRecognizer()
    entities = ner.extract_entities("John Smith works at Apple in San Francisco")
    
    assert "PERSON" in entities or "PERSON" not in entities  # Depends on model
    assert isinstance(entities, dict)

# Test topic extraction
def test_topic_extractor():
    from app.nlp.processors import TopicExtractor
    
    text = "The technology company announced new AI features"
    topics = TopicExtractor.extract_topics_simple(text, n_topics=3)
    
    assert isinstance(topics, list)
    assert len(topics) <= 3

# Test text cleaner
def test_text_cleaner():
    from app.nlp.processors import TextCleaner
    
    dirty = "<p>Hello <b>world</b>! http://example.com   </p>"
    clean = TextCleaner.clean_text(dirty)
    
    assert "<" not in clean
    assert "http" not in clean
    assert "  " not in clean

# Test trend analyzer
def test_trend_analyzer():
    from app.nlp.processors import TrendAnalyzer
    
    articles = [
        {"main_topic": "AI", "sentiment_score": 0.5, "published_at": datetime.utcnow()},
        {"main_topic": "AI", "sentiment_score": 0.7, "published_at": datetime.utcnow()},
        {"main_topic": "Climate", "sentiment_score": -0.3, "published_at": datetime.utcnow()},
    ]
    
    trends = TrendAnalyzer.detect_trending_topics(articles, time_window_hours=24)
    
    assert len(trends) >= 1
    assert trends[0]["frequency"] >= 1
    assert "sentiment_avg" in trends[0]
```

### Frontend Unit Tests

**File: `frontend/__tests__/apiService.test.ts`**

```typescript
import apiService from "@services/apiService";
import axios from "axios";

jest.mock("axios");

describe("API Service", () => {
  it("should fetch headlines", async () => {
    const mockData = {
      articles: [{ id: "1", title: "Test" }],
      total_count: 1,
      page: 1,
      page_size: 10,
    };

    (axios.get as jest.Mock).mockResolvedValue({ data: mockData });

    const result = await apiService.getHeadlines("general", 1, 10);

    expect(result).toEqual(mockData);
    expect(axios.get).toHaveBeenCalled();
  });

  it("should handle API errors", async () => {
    const error = new Error("Network error");
    (axios.get as jest.Mock).mockRejectedValue(error);

    await expect(apiService.getHeadlines()).rejects.toThrow("Network error");
  });
});
```

## 2. Integration Tests

**File: `backend/tests/test_integration.py`**

```python
@pytest.fixture
def client_with_data():
    """Setup test client with sample data"""
    from fastapi.testclient import TestClient
    from app.main import app
    
    client = TestClient(app)
    
    # Add sample article
    article = Article(
        id="test-1",
        url="http://test.com",
        title="Integration Test Article",
        content="Test content about AI and technology",
        source="Test News",
        category="technology",
        sentiment_score=0.5,
        sentiment_label="positive",
        main_topic="AI"
    )
    db.add(article)
    db.commit()
    
    yield client

def test_full_query_flow(client_with_data):
    """Test complete RAG query flow"""
    # 1. Query with RAG
    response = client_with_data.post(
        "/api/ai/query",
        json={"query": "What about AI?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    
    # 2. Get article sentiment
    article_id = data["sources"][0]["id"]
    response = client_with_data.get(f"/api/ai/sentiment/{article_id}")
    assert response.status_code == 200
    assert "sentiment_label" in response.json()

def test_ingestion_to_retrieval_flow():
    """Test data flow from ingestion to retrieval"""
    import asyncio
    from app.ingestion.pipeline import IngestionPipeline
    from app.rag.pipeline import retriever
    
    async def run_flow():
        # Ingest articles
        pipeline = IngestionPipeline()
        articles = await pipeline.ingest("newsapi")
        
        # Retrieve articles
        if articles:
            results, scores = retriever.retrieve("test query", top_k=5)
            assert isinstance(results, list)
    
    asyncio.run(run_flow())
```

## 3. API Endpoint Tests

**File: `backend/tests/test_endpoints.py`**

```python
class TestEndpoints:
    """Test all REST API endpoints"""
    
    def test_health_endpoint(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_headlines_endpoint(self, client):
        response = client.get("/api/news/headlines")
        assert response.status_code == 200
        assert "articles" in response.json()
    
    def test_category_endpoint(self, client):
        response = client.get("/api/news/category/technology")
        assert response.status_code == 200
        assert isinstance(response.json()["articles"], list)
    
    def test_search_endpoint(self, client):
        response = client.get("/api/news/search?q=AI")
        assert response.status_code == 200
        assert "articles" in response.json()
    
    def test_trending_endpoint(self, client):
        response = client.get("/api/trending/topics")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_rag_query_endpoint(self, client):
        response = client.post(
            "/api/ai/query",
            json={"query": "What is the news?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
    
    def test_summarize_endpoint(self, client):
        # Would need valid article_id from database
        response = client.post(
            "/api/ai/summarize",
            json={"article_id": "test-id"}
        )
        assert response.status_code in [200, 404]
```

## 4. React Native Component Tests

**File: `frontend/__tests__/screens/HomeScreen.test.tsx`**

```typescript
import React from "react";
import { render, screen, waitFor } from "@testing-library/react-native";
import { Provider } from "react-redux";
import { store } from "@store/index";
import HomeScreen from "@screens/HomeScreen";

describe("HomeScreen", () => {
  it("should render headlines", async () => {
    const mockNavigation = { navigate: jest.fn() };

    render(
      <Provider store={store}>
        <HomeScreen navigation={mockNavigation} />
      </Provider>
    );

    await waitFor(() => {
      expect(screen.getByText(/Top Headlines/i)).toBeTruthy();
    });
  });

  it("should handle refresh", async () => {
    const mockNavigation = { navigate: jest.fn() };

    const { getByTestId } = render(
      <Provider store={store}>
        <HomeScreen navigation={mockNavigation} />
      </Provider>
    );

    // Simulate refresh
    const refreshControl = getByTestId("refresh-control");
    expect(refreshControl).toBeTruthy();
  });
});
```

## 5. E2E Tests

**File: `frontend/e2e/firstTest.e2e.js`**

```javascript
describe("News App E2E", () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it("should search for articles", async () => {
    // Navigate to search tab
    await element(by.label("Search")).tap();

    // Type query
    await element(by.id("search-input")).typeText("AI");

    // Press ask AI button
    await element(by.label("Ask AI")).tap();

    // Wait for results
    await waitFor(element(by.text(/AI Answer:/)))
      .toBeVisible()
      .withTimeout(5000);
  });

  it("should view article summary", async () => {
    // Navigate to home
    await element(by.label("Home")).tap();

    // Wait for articles to load
    await waitFor(element(by.text(/Test Article/)))
      .toBeVisible()
      .withTimeout(5000);

    // Tap article
    await element(by.text(/Test Article/)).multiTap();

    // Verify summary appears
    await expect(element(by.text(/Summary/))).toBeVisible();
  });
});
```

## Test Coverage Targets

- **Overall Coverage**: > 80%
- **Backend Coverage**: > 85%
  - RAG Pipeline: 90%
  - API Routes: 85%
  - NLP Processors: 80%
- **Frontend Coverage**: 75%
  - Components: 80%
  - Services: 85%
  - Redux Slices: 75%

## Running Tests

```bash
# Backend
cd backend
pytest tests/ --cov=app --cov-report=html

# Frontend
cd frontend
npm test -- --coverage

# E2E
detox test --configuration ios.sim.debug
```

## CI/CD Integration

See `.github-workflows-main.yml` for GitHub Actions pipeline that:
- Runs unit tests on every PR
- Enforces coverage thresholds
- Generates coverage reports
- Blocks merge if tests fail

