# INSTALLATION & DEPENDENCIES

## System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB
- OS: Windows, macOS, or Linux

### Recommended (Production)
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 100GB+
- OS: Linux (Ubuntu 20.04+)

---

## Prerequisites to Install

### Required
1. **Docker & Docker Compose** (for easiest setup)
   - Download: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version && docker-compose --version`

2. **Python 3.11+** (for local backend development)
   - Download: https://www.python.org/downloads/
   - Verify: `python --version`

3. **Node.js 18+** (for frontend development)
   - Download: https://nodejs.org/
   - Verify: `node --version && npm --version`

4. **Git** (for version control)
   - Download: https://git-scm.com/
   - Verify: `git --version`

### Optional (for local database)
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

---

## Installation Methods

### METHOD 1: Docker (Recommended - Fastest)

**1. Install Docker**
- Visit: https://www.docker.com/products/docker-desktop
- Download and install for your OS
- Verify: `docker --version`

**2. Clone or Download Project**
```bash
cd ai-news-intelligence
```

**3. Start Stack**
```bash
cd deployment/docker
docker-compose up -d
```

**4. Verify Services**
```bash
# Check containers
docker ps

# Check backend
curl http://localhost:8000/api/health

# Check logs
docker logs news_backend
```

**Duration**: ~5 minutes (includes downloads)

---

### METHOD 2: Local Python Backend

**1. Install Python 3.11+**
```bash
python --version  # Should be 3.11 or higher
```

**2. Navigate to Backend**
```bash
cd backend
```

**3. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**4. Install Dependencies**
```bash
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

**5. Setup Environment**
```bash
cp .env.example .env
# Edit .env and add your settings
```

**6. Setup Database** (Use Docker or local PostgreSQL)
```bash
# If using Docker for just database
docker run -d \
  --name news_db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=news_db \
  -p 5432:5432 \
  postgres:15-alpine
```

**7. Initialize Database**
```bash
python -c "from app.db.database import init_db; init_db()"
```

**8. Run Backend**
```bash
uvicorn app.main:app --reload
```

**Duration**: ~10 minutes

---

### METHOD 3: Local React Native Frontend

**1. Install Node.js 18+**
```bash
node --version  # Should be 18 or higher
npm --version
```

**2. Navigate to Frontend**
```bash
cd frontend
```

**3. Install Dependencies**
```bash
npm install
```

**4. Setup Environment**
```bash
cp .env.example .env
# Edit .env - make sure API_URL points to backend
```

**5. Run Development Server**
```bash
npm start
```

**Duration**: ~5 minutes

---

## Full Local Development Setup

### All Components Locally (Advanced)

**1. PostgreSQL Setup**
```bash
# Option A: Docker
docker run -d \
  --name news_postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15-alpine

# Option B: Local installation
# Download from: https://www.postgresql.org/download/
```

**2. Redis Setup**
```bash
# Docker
docker run -d \
  --name news_redis \
  -p 6379:6379 \
  redis:7-alpine

# Local installation
# Download from: https://redis.io/
```

**3. Backend Setup** (see METHOD 2 above)

**4. Frontend Setup** (see METHOD 3 above)

**5. Verify All Services**
```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend running
# Visit http://localhost:19000 (Expo)

# Database
psql -h localhost -U postgres

# Redis
redis-cli ping
```

---

## Dependency Details

### Backend Dependencies (Python)

**Core Framework**
- fastapi==0.104.1 - Web framework
- uvicorn==0.24.0 - ASGI server
- pydantic==2.5.0 - Data validation

**Database**
- sqlalchemy==2.0.23 - ORM
- psycopg2-binary==2.9.9 - PostgreSQL driver
- alembic==1.12.1 - Database migrations

**Authentication**
- python-jose==3.3.0 - JWT tokens
- passlib==1.7.4 - Password hashing
- bcrypt==4.1.1 - Encryption

**AI/ML**
- sentence-transformers==2.2.2 - Embeddings (384 dims)
- faiss-cpu==1.7.4 - Vector search
- transformers==4.35.2 - HuggingFace models
- openai==1.3.8 - OpenAI API

**NLP**
- nltk==3.8.1 - Natural language processing
- spacy==3.7.2 - Named entity recognition
- textblob==0.17.1 - Sentiment analysis
- scikit-learn==1.3.2 - Machine learning

**Data Processing**
- pandas==2.1.3 - DataFrames
- numpy==1.24.3 - Numerical computing

**Caching & Async**
- redis==5.0.1 - Redis client
- celery==5.3.4 - Task queue

**Web Scraping**
- beautifulsoup4==4.12.2 - HTML parsing
- feedparser==6.0.10 - RSS parsing
- requests==2.31.0 - HTTP requests

**Testing**
- pytest==7.4.3 - Test framework
- pytest-asyncio==0.21.1 - Async test support
- pytest-cov==4.1.0 - Coverage reporting

---

### Frontend Dependencies (Node.js)

**Core Framework**
- react==18.2.0 - React library
- react-native==0.73.0 - Mobile framework
- typescript==5.3.0 - Type safety

**Navigation**
- @react-navigation/native - Navigation
- @react-navigation/bottom-tabs - Tab navigation
- @react-navigation/stack - Stack navigation
- react-native-screens==3.27.0 - Native screens

**State Management**
- @reduxjs/toolkit==1.9.7 - Redux state
- react-redux==8.1.3 - React-Redux bindings
- react-query==3.39.3 - Data fetching

**HTTP & Storage**
- axios==1.6.0 - HTTP client
- @react-native-async-storage/async-storage==1.21.0 - Local storage

**Testing & Development**
- jest==29.7.0 - Test framework
- @testing-library/react-native==12.2.0 - Component testing
- @types/react==18.2.0 - Type definitions
- @types/react-native==0.73.0 - Type definitions

---

## Troubleshooting Installation

### Python Issues

**Issue**: `python: command not found`
```bash
# Solution: Use python3 on macOS/Linux
python3 --version
python3 -m venv venv
source venv/bin/activate
```

**Issue**: `ModuleNotFoundError: No module named 'spacy'`
```bash
# Solution: Download spaCy model
python -m spacy download en_core_web_sm
```

**Issue**: Database connection error
```bash
# Solution: Check PostgreSQL is running
# If using Docker:
docker ps | grep postgres
docker start news_db

# If local:
psql -h localhost -U postgres
```

### Node.js Issues

**Issue**: `npm: command not found`
```bash
# Solution: Install Node.js
# https://nodejs.org/

# Verify
node --version
npm --version
```

**Issue**: `EACCES: permission denied`
```bash
# Solution on Linux/Mac
sudo npm install -g npm
```

### Docker Issues

**Issue**: `Docker daemon not running`
```bash
# Solution: Start Docker Desktop application
# Windows/Mac: Open Docker Desktop app
# Linux: sudo systemctl start docker
```

**Issue**: Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

---

## Verification Checklist

After installation, verify everything works:

### Docker Setup
- [ ] `docker --version` works
- [ ] `docker ps` shows containers
- [ ] Backend API responds to `curl http://localhost:8000/api/health`

### Python Setup
- [ ] `python --version` shows 3.11+
- [ ] Virtual environment activated
- [ ] `pytest --version` works
- [ ] `python -c "import fastapi"` succeeds

### Node.js Setup
- [ ] `node --version` shows 18+
- [ ] `npm --version` shows 9+
- [ ] `npm list react` works
- [ ] `npm start` runs without errors

### Database
- [ ] PostgreSQL accessible
- [ ] Database tables created
- [ ] Can connect with psql

### Redis
- [ ] Redis running
- [ ] `redis-cli ping` returns PONG
- [ ] Cache operations work

---

## Next Steps After Installation

1. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Add API keys (OpenAI, NewsAPI, etc.)

2. **Test the Setup**
   - Run health check: `curl http://localhost:8000/api/health`
   - Access Swagger UI: http://localhost:8000/docs

3. **Ingest Sample News**
   - Use API to fetch headlines
   - Test RAG query functionality

4. **Explore the Code**
   - Check backend routes
   - Review frontend screens
   - Read RAG pipeline code

5. **Run Tests**
   - Backend: `pytest backend/tests/`
   - Frontend: `npm test`

---

## Getting Help

If installation fails:

1. Check [README.md](README.md#troubleshooting)
2. Review this file for your specific issue
3. Check Docker logs: `docker logs news_backend`
4. Verify prerequisites are installed
5. See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Total Installation Time**:
- Docker method: ~5 minutes
- Local method: ~20 minutes
- Full local method: ~30 minutes

Good luck! 🚀
