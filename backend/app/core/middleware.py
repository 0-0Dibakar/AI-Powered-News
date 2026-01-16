"""Rate limiting middleware"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import time
from app.core.config import settings
from app.core.logging import logger


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using Redis"""
    
    def __init__(self, app, redis_url: str = None):
        """Initialize rate limiter"""
        super().__init__(app)
        try:
            self.redis_client = redis.from_url(redis_url or settings.REDIS_URL)
            self.enabled = settings.RATE_LIMIT_ENABLED
            logger.info("Rate limiting middleware initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize Redis: {e}. Rate limiting disabled.")
            self.redis_client = None
            self.enabled = False
    
    async def dispatch(self, request: Request, call_next):
        """Rate limit incoming requests"""
        if not self.enabled or not self.redis_client:
            return await call_next(request)
        
        try:
            # Get client identifier (IP or API key)
            client_id = request.headers.get("x-api-key") or request.client.host
            
            # Check rate limit
            key = f"rate_limit:{client_id}"
            current = self.redis_client.get(key)
            
            if current and int(current) >= settings.RATE_LIMIT_REQUESTS:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later."
                )
            
            # Increment counter
            if current:
                self.redis_client.incr(key)
            else:
                self.redis_client.setex(key, settings.RATE_LIMIT_WINDOW_SECONDS, 1)
            
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return await call_next(request)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        """Log request details"""
        import time
        
        start_time = time.time()
        
        # Log request
        logger.info(f"{request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Status: {response.status_code} | Time: {process_time:.2f}s")
        
        return response


class CORSMiddleware:
    """Custom CORS handling"""
    
    def __init__(self, app):
        """Initialize CORS"""
        from fastapi.middleware.cors import CORSMiddleware as FastAPICORS
        
        self.middleware = FastAPICORS(
            app,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS
        )
