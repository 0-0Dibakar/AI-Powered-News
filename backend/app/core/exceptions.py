"""Custom exception classes"""

from fastapi import HTTPException, status


class NewsIntelligenceException(Exception):
    """Base exception for the application"""
    pass


class RAGException(NewsIntelligenceException):
    """RAG pipeline related exception"""
    pass


class NoRelevantDocumentsFound(RAGException):
    """Raised when no relevant documents are found during retrieval"""
    message = "No relevant information found in the available news sources."


class EmbeddingException(RAGException):
    """Raised when embedding generation fails"""
    pass


class VectorDBException(RAGException):
    """Raised when vector database operations fail"""
    pass


class IngestionException(NewsIntelligenceException):
    """News ingestion pipeline exception"""
    pass


class DatabaseException(NewsIntelligenceException):
    """Database operation exception"""
    pass


class ExternalAPIException(NewsIntelligenceException):
    """External API call exception"""
    pass


# HTTP Exception mappers
def rag_exception_handler(exc: RAGException):
    """Handle RAG exceptions"""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )


def database_exception_handler(exc: DatabaseException):
    """Handle database exceptions"""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error occurred"
    )


def external_api_exception_handler(exc: ExternalAPIException):
    """Handle external API exceptions"""
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="External service unavailable"
    )
