"""Logging configuration"""

import logging
import logging.handlers
import os
from app.core.config import settings


def setup_logging():
    """Configure application logging"""
    
    # Create logs directory if not exists
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
    
    # Get logger
    logger = logging.getLogger("ai_news_intelligence")
    logger.setLevel(settings.LOG_LEVEL)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logging()
