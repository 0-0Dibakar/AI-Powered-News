# AI News Intelligence Platform - Complete Setup Guide

## Project Overview

AI News Intelligence is a production-ready mobile application that aggregates news from multiple sources and uses Retrieval-Augmented Generation (RAG) with Large Language Models to provide intelligent news analysis, Q&A, summarization, and trend detection.

**Key Features:**
- Real-time news aggregation from multiple sources
- RAG-powered intelligent Q&A
- Sentiment analysis and trend detection
- Article summarization
- Category-based news organization
- Mobile-first design (Android & iOS)

---

## Architecture

### System Components

1. **Frontend (React Native + TypeScript)**
   - Mobile app for iOS and Android
   - 4 main screens: Home, Categories, Search/Ask AI, Summary
   - Redux for state management
   - Responsive UI optimized for mobile

2. **Backend (FastAPI + Python)**
   - REST API for all frontend requests
   - RAG pipeline with embedding and retrieval
   - News ingestion system
   - NLP processing (sentiment, entities, topics)
   - Rate limiting and authentication

3. **AI/ML Components**
   - Embedding Model: `all-MiniLM-L6-v2` (384 dimensions)
   - Vector Database: FAISS for similarity search
   - LLM: OpenAI GPT-3.5-turbo or local LLaMA
   - NLP Tools: spaCy, NLTK, TextBlob

4. **Data Storage**
   - PostgreSQL: Article metadata and chunks
   - Redis: Caching and rate limiting
   - FAISS: Vector embeddings index

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)
- API Keys: OpenAI, NewsAPI, Guardian

### Quick Start with Docker

**1. Clone and Setup**

```bash
cd ai-news-intelligence
```

**2. Configure Environment**

```bash
# Backend
cd backend
cp .env.example .env
# Edit .env with your API keys and settings

# Frontend
cd ../frontend
cp .env.example .env
```

**3. Start Services**

```bash
cd deployment/docker
docker-compose up -d
```

Services will be available at:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PgAdmin: http://localhost:5050 (admin@example.com / admin)
- Redis: localhost:6379

**4. Initialize Database**

```bash
docker exec news_backend python -c "from app.db.database import init_db; init_db()"
```

**5. Ingest Sample News**

```bash
docker exec news_backend python -c "
import asyncio
from app.ingestion.pipeline import IngestionPipeline

pipeline = IngestionPipeline()
asyncio.run(pipeline.ingest('newsapi'))
"
```

---

## Local Development Setup

### Backend Setup

**1. Create Virtual Environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**3. Set Up PostgreSQL Locally**

```bash
# Create database
createdb news_db

# Set connection string in .env
DATABASE_URL=postgresql://user:password@localhost:5432/news_db
```

**4. Run Backend**

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

**1. Install Dependencies**

```bash
cd frontend
npm install
```

**2. Configure API URL**

Create `.env` file:

```
REACT_APP_API_URL=http://localhost:8000/api
```

**3. Run Development Server**

```bash
# For Expo
expo start

# For React Native CLI
npm start
```

---

## API Documentation

### Key Endpoints

#### Health Check
```
GET /api/health
```
Returns: `{status, version, timestamp}`

#### Get Headlines
```
GET /api/news/headlines?category=general&page=1&page_size=10
```

#### News by Category
```
GET /api/news/category/{category}
```
Categories: business, technology, politics, sports, health, science, entertainment, world

#### RAG Query (Ask AI)
```
POST /api/ai/query
{
  "query": "What are the latest developments in AI?",
  "category": "technology"
}
```
Returns: `{answer, sources, confidence_score, status}`

#### Search Articles
```
GET /api/news/search?q=keyword&page=1&page_size=10
```

#### Get Trending Topics
```
GET /api/trending/topics?hours=24
```

#### Article Summarization
```
POST /api/ai/summarize
{
  "article_id": "article-123",
  "max_length": 300
}
```

#### Sentiment Analysis
```
GET /api/ai/sentiment/{article_id}
```

Full API docs available at `http://localhost:8000/docs`

---

## Configuration

### Environment Variables

**Critical Production Settings:**

```env
# Security
SECRET_KEY=generate-strong-random-key-here
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@host:5432/news_db

# API Keys
OPENAI_API_KEY=sk-...
NEWSAPI_KEY=your-key
GUARDIAN_API_KEY=your-key

# RAG Settings
RAG_TOP_K=5
CHUNK_SIZE=400
CHUNK_OVERLAP=50
LLM_TEMPERATURE=0.2

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60
```

---

## Security Best Practices

### 1. Authentication & Authorization

- JWT tokens for user sessions
- API key validation for mobile clients
- CORS properly configured
- HTTPS enforced in production

```python
# Verify token middleware
@app.get("/protected")
async def protected_endpoint(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401)
    return payload
```

### 2. Database Security

- Use environment variables for credentials
- Connection pooling enabled
- SQL injection prevention with parameterized queries
- Database backups automated

### 3. Input Validation

- Pydantic models validate all requests
- Query sanitization
- Rate limiting prevents abuse
- Token limits enforced

### 4. Data Protection

- Sensitive data never logged
- Credentials encrypted in environment
- HTTPS for all communications
- GDPR compliance for user data

### 5. API Security

- Rate limiting per user/IP
- Request signing support
- Error responses don't leak internals
- Health check endpoints public

---

## Performance Optimization

### Caching Strategy

**Redis Caching Layers:**
- Query results (TTL: 1 hour)
- Article embeddings (TTL: 24 hours)
- Rate limit counters (TTL: per window)
- Session data (TTL: per token expiry)

```python
# Cache implementation
cache_key = f"query:{query_hash}"
cached = redis_client.get(cache_key)
if cached:
    return json.loads(cached)

# If miss, compute and cache
result = compute_rag_result(query)
redis_client.setex(cache_key, 3600, json.dumps(result))
return result
```

### Database Optimization

- Indexed searches on: source, category, published_at, created_at
- Connection pooling (20 connections + 40 overflow)
- Read replicas for scaling
- Batch inserts for news ingestion

### Vector Database

- FAISS indexing for O(log n) similarity search
- Batch embedding generation (32 documents at once)
- Periodic index optimization
- Sharding for large datasets (>10M documents)

### Frontend Optimization

- Image lazy loading
- Infinite scroll pagination
- Local caching with AsyncStorage
- Debounced search input

---

## Scalability Recommendations

### Horizontal Scaling

1. **Load Balancer**: Nginx/HAProxy
   ```
   User → Load Balancer → Multiple FastAPI instances
   ```

2. **Database**: PostgreSQL replication
   - Primary (write)
   - Read replicas (queries)
   - Connection pooling

3. **Vector DB**: FAISS index sharding
   - Shard by category or time range
   - Distributed retrieval

4. **Cache**: Redis Cluster
   - 6+ nodes for redundancy
   - Sentinel for failover

### Vertical Scaling

- GPU support for embedding generation
- Increased memory for larger FAISS indices
- Faster CPU for LLM inference

### Auto-Scaling with Kubernetes

```yaml
HorizontalPodAutoscaler:
  minReplicas: 2
  maxReplicas: 10
  targetCPU: 70%
  targetMemory: 80%
```

---

## Testing

### Backend Testing

**Run tests:**
```bash
cd backend
pytest tests/ --cov=app
```

**Test coverage:**
- Unit tests for RAG components
- Integration tests for API endpoints
- Database transaction tests

### Frontend Testing

**Run tests:**
```bash
cd frontend
npm test
```

### E2E Testing

```bash
# Mobile E2E with Detox
npm install -D detox-cli
detox build-framework-cache
detox build-app
detox test
```

---

## Monitoring & Observability

### Logging

- Centralized logging with ELK stack
- Log levels: DEBUG, INFO, WARNING, ERROR
- Structured JSON logs for easy parsing

### Metrics

- Prometheus: Response times, error rates, cache hits
- Grafana: Dashboards for monitoring
- Custom metrics:
  - RAG query latency
  - Embedding generation time
  - Cache hit rate
  - API request counts

### Alerting

```yaml
# Example Prometheus alert
- alert: HighLatency
  expr: histogram_quantile(0.95, api_response_time_ms) > 5000
  for: 5m
  action: notify-slack
```

---

## Troubleshooting

### Common Issues

**1. FAISS Index Corruption**
```bash
# Rebuild index
rm -rf data/faiss_index
# Reingest articles
python -c "import asyncio; from app.ingestion.pipeline import IngestionPipeline; asyncio.run(IngestionPipeline().ingest())"
```

**2. Database Connection Errors**
```bash
# Check PostgreSQL
psql -U postgres -h localhost -c "SELECT 1"

# Reset connections
docker-compose down && docker-compose up -d
```

**3. Memory Issues with Large Datasets**
- Reduce chunk size in .env
- Increase VM.max_map_count for FAISS
- Use FAISS GPU variant

**4. Slow RAG Queries**
- Check Redis connectivity
- Monitor embedding model performance
- Reduce RAG_TOP_K if slow
- Add database indexes

---

## Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Deploy with docker stack
docker stack deploy -c docker-compose.yml news-app
```

### Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f deployment/k8s/

# Monitor
kubectl get pods -l app=news-backend
kubectl logs deployment/news-backend

# Scale
kubectl scale deployment news-backend --replicas=5
```

### Cloud Platforms

**AWS:**
```bash
# Deploy to ECS Fargate
aws ecs create-service --cluster news --task-definition news-backend
```

**GCP:**
```bash
# Deploy to Cloud Run
gcloud run deploy news-backend --source ./backend
```

**Azure:**
```bash
# Deploy to App Service
az webapp up --name news-backend --runtime python:3.11
```

---

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Submit pull request

## License

MIT License - See LICENSE file

## Support

- Documentation: See ARCHITECTURE.md
- Issues: GitHub Issues
- Discussions: GitHub Discussions

