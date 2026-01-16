# QUICK REFERENCE GUIDE

## File Locations

### Backend Core
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/api/routes.py` - All REST API endpoints
- `backend/app/rag/pipeline.py` - RAG components (embedding, retrieval)
- `backend/app/rag/llm.py` - LLM integration (OpenAI, local)
- `backend/app/ingestion/pipeline.py` - News ingestion system
- `backend/app/nlp/processors.py` - NLP tools (sentiment, NER, topics)
- `backend/app/db/models.py` - Database schema
- `backend/requirements.txt` - Python dependencies

### Frontend Core
- `frontend/src/App.tsx` - Navigation and routing
- `frontend/src/screens/HomeScreen.tsx` - Top headlines
- `frontend/src/screens/SearchScreen.tsx` - Ask AI & search
- `frontend/src/services/apiService.ts` - API client
- `frontend/src/store/index.ts` - Redux configuration
- `frontend/package.json` - Dependencies

### Configuration
- `backend/.env.example` - Backend environment template
- `frontend/.env.example` - Frontend environment template
- `deployment/docker/docker-compose.yml` - Local dev stack
- `deployment/k8s/backend-deployment.yaml` - Production deployment

### Documentation
- `README.md` - Setup and usage guide
- `ARCHITECTURE.md` - System design
- `SECURITY.md` - Security best practices
- `TESTING.md` - Testing strategy
- `PROMPTS.md` - LLM prompts

---

## Common Commands

### Start Development Environment
```bash
# Using Docker (easiest)
cd deployment/docker && docker-compose up -d

# Local Python backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# React Native frontend
cd frontend
npm install && npm start
```

### Database Operations
```bash
# Enter PostgreSQL
docker exec -it news_db psql -U postgres

# Create tables
docker exec news_backend python -c "from app.db.database import init_db; init_db()"

# View logs
docker logs -f news_backend
```

### Testing
```bash
# Backend tests
cd backend && pytest tests/ --cov=app -v

# Frontend tests
cd frontend && npm test -- --coverage
```

### API Testing
```bash
# Health check
curl http://localhost:8000/api/health

# Get headlines
curl http://localhost:8000/api/news/headlines?category=general

# Ask AI
curl -X POST http://localhost:8000/api/ai/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What is AI?"}'
```

---

## Key Configuration Variables

### Backend (.env)
```
OPENAI_API_KEY=sk-...
NEWSAPI_KEY=...
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379
DEBUG=true
SECRET_KEY=your-secret-key
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_VERSION=1.0.0
```

---

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/news/headlines` | Top headlines |
| GET | `/api/news/category/{cat}` | News by category |
| GET | `/api/news/search` | Search articles |
| POST | `/api/ai/query` | Ask AI (RAG) |
| POST | `/api/ai/summarize` | Summarize article |
| GET | `/api/ai/sentiment/{id}` | Sentiment analysis |
| GET | `/api/trending/topics` | Trending topics |

---

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker exec news_db pg_isready

# Reset database
docker-compose down -v && docker-compose up -d
```

### FAISS Index Issue
```bash
# Rebuild vector index
rm -rf backend/data/faiss_index
# Re-ingest articles through API
```

### API Not Responding
```bash
# Check backend logs
docker logs news_backend

# Check health
curl http://localhost:8000/api/health
```

---

## Performance Metrics

### Target Numbers
- API Response Time: < 500ms (p95)
- Ray Query Latency: < 1 second
- Concurrent Users: 1000+
- Cache Hit Rate: > 60%
- Database Query Time: < 50ms

### Monitor Performance
```bash
# Backend metrics
curl http://localhost:8000/metrics

# Database slow queries
docker exec news_db psql -U postgres \
  -c "SELECT query, calls, mean_time FROM pg_stat_statements ORDER BY mean_time DESC;"
```

---

## Security Checklist Before Production

- [ ] Set unique SECRET_KEY
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set strong database password
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Set up monitoring/alerts
- [ ] Enable audit logging
- [ ] Backup database regularly
- [ ] Rotate API keys

---

## Scaling Checklist

- [ ] Add PostgreSQL read replicas
- [ ] Enable Redis cluster
- [ ] Deploy behind load balancer
- [ ] Configure Kubernetes HPA
- [ ] Set up database sharding (if needed)
- [ ] Enable CDN for static assets
- [ ] Configure monitoring dashboard
- [ ] Set up auto-scaling policies

---

## Important Links

- **OpenAI API**: https://platform.openai.com/api-keys
- **NewsAPI**: https://newsapi.org
- **FastAPI Docs**: http://localhost:8000/docs (when running)
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Docker Docs**: https://docs.docker.com/
- **React Native Docs**: https://reactnative.dev/

---

## Development Tips

1. **Hot Reload**: Backend changes auto-reload with `--reload`
2. **API Testing**: Use Swagger UI at `/docs`
3. **Database Inspection**: Use PgAdmin at `http://localhost:5050`
4. **Logging**: Check app logs in `backend/logs/app.log`
5. **Redux DevTools**: Install browser extension for state debugging
6. **Type Safety**: Always use TypeScript in frontend
7. **Tests First**: Write tests before implementing features
8. **Environment Variables**: Never commit `.env` files

---

## Next Steps After Setup

1. **Configure News Sources**
   - Get API key from NewsAPI
   - Set in `.env`
   - Run ingestion pipeline

2. **Set Up LLM**
   - Use OpenAI (add API key) OR
   - Use local LLaMA (download model)
   - Test with `/api/ai/query`

3. **Monitor & Scale**
   - Set up Prometheus monitoring
   - Configure Grafana dashboards
   - Set up alerting

4. **Deploy**
   - Push to AWS/GCP/Azure
   - Configure DNS & SSL
   - Enable CDN
   - Set up CI/CD pipeline

---

*For detailed information, see README.md, ARCHITECTURE.md, or SECURITY.md*
