"""Main FastAPI application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.db.database import init_db
from app.api.routes import router as api_router
from app.rag.pipeline import init_rag_components
from app.rag.llm import init_rag_engine
from app.core.middleware import RateLimitMiddleware, RequestLoggingMiddleware


# Setup logging
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    # Startup
    logger.info("Starting AI News Intelligence Application")
    try:
        init_db()
        logger.info("Database initialized")
        
        init_rag_components()
        logger.info("RAG components initialized")
        
        init_rag_engine()
        logger.info("RAG engine initialized")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered News Intelligence Platform with RAG",
    lifespan=lifespan
)


# Add middleware
app.add_middleware(CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, redis_url=settings.REDIS_URL)


# Include routes
app.include_router(api_router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
