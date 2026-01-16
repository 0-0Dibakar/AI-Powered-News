"""RAG pipeline components"""

import os
import pickle
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from app.core.config import settings
from app.core.exceptions import (
    EmbeddingException, VectorDBException, NoRelevantDocumentsFound
)
from app.core.logging import logger


class EmbeddingModel:
    """Sentence embedding model wrapper"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise EmbeddingException(f"Failed to load embedding model: {e}")
    
    def encode(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode texts to embeddings"""
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            return embeddings
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            raise EmbeddingException(f"Embedding failed: {e}")


class VectorDatabase:
    """FAISS vector database wrapper"""
    
    def __init__(self, embedding_dim: int = 384, index_path: str = None):
        """Initialize vector database"""
        try:
            import faiss
            self.faiss = faiss
            self.index_path = index_path or settings.VECTOR_DB_PATH
            self.embedding_dim = embedding_dim
            self.doc_id_map = {}  # Map from index position to doc ID
            
            os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
            
            if os.path.exists(self.index_path):
                self.index = faiss.read_index(self.index_path)
                logger.info(f"Loaded vector index from {self.index_path}")
            else:
                self.index = faiss.IndexFlatL2(embedding_dim)
                logger.info("Created new FAISS index")
        except Exception as e:
            logger.error(f"Vector DB initialization failed: {e}")
            raise VectorDBException(f"Vector DB initialization failed: {e}")
    
    def add(self, embeddings: np.ndarray, doc_ids: List[str]) -> List[int]:
        """Add embeddings to index"""
        try:
            embeddings = np.array(embeddings, dtype=np.float32)
            start_idx = self.index.ntotal
            self.index.add(embeddings)
            
            for i, doc_id in enumerate(doc_ids):
                self.doc_id_map[start_idx + i] = doc_id
            
            self.save()
            logger.info(f"Added {len(doc_ids)} embeddings to vector DB")
            return list(range(start_idx, start_idx + len(doc_ids)))
        except Exception as e:
            logger.error(f"Failed to add embeddings: {e}")
            raise VectorDBException(f"Failed to add embeddings: {e}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> Tuple[List[str], List[float]]:
        """Search for similar embeddings"""
        try:
            query_embedding = np.array([query_embedding], dtype=np.float32)
            distances, indices = self.index.search(query_embedding, top_k)
            
            doc_ids = []
            scores = []
            
            for idx, distance in zip(indices[0], distances[0]):
                if idx in self.doc_id_map:
                    doc_ids.append(self.doc_id_map[idx])
                    # Convert L2 distance to similarity score (0-1)
                    similarity = 1 / (1 + distance)
                    scores.append(float(similarity))
            
            return doc_ids, scores
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise VectorDBException(f"Search failed: {e}")
    
    def save(self):
        """Save index to disk"""
        try:
            self.faiss.write_index(self.index, self.index_path)
            logger.info(f"Saved vector index to {self.index_path}")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise VectorDBException(f"Failed to save index: {e}")


class TextChunker:
    """Split documents into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        """Initialize chunker"""
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, chunk_id_prefix: str = "") -> List[Tuple[str, str]]:
        """
        Chunk text into overlapping segments
        
        Returns:
            List of (chunk_id, chunk_text) tuples
        """
        words = text.split()
        chunks = []
        
        i = 0
        chunk_idx = 0
        
        while i < len(words):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunk_id = f"{chunk_id_prefix}_chunk_{chunk_idx}"
            chunks.append((chunk_id, chunk_text))
            
            i += self.chunk_size - self.overlap
            chunk_idx += 1
        
        return chunks


class Retriever:
    """RAG retriever component"""
    
    def __init__(self, embedding_model: EmbeddingModel, vector_db: VectorDatabase):
        """Initialize retriever"""
        self.embedding_model = embedding_model
        self.vector_db = vector_db
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = settings.VECTOR_SIMILARITY_THRESHOLD
    ) -> Tuple[List[str], List[float]]:
        """
        Retrieve relevant documents for query
        
        Returns:
            List of (doc_id, similarity_score) tuples
        """
        try:
            # Encode query
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Search vector DB
            doc_ids, scores = self.vector_db.search(query_embedding, top_k=top_k * 2)
            
            # Filter by threshold
            results = [
                (doc_id, score)
                for doc_id, score in zip(doc_ids, scores)
                if score >= similarity_threshold
            ]
            
            if not results:
                raise NoRelevantDocumentsFound()
            
            # Return top-k
            return results[:top_k]
        except NoRelevantDocumentsFound:
            raise
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            raise VectorDBException(f"Retrieval failed: {e}")


class PromptTemplate:
    """Prompt template manager for LLM"""
    
    SYSTEM_PROMPT = """You are an AI News Intelligence Assistant.

You must answer strictly based on retrieved news documents provided below.
If the answer is not present in the retrieved documents, clearly say:
"No relevant information found in the available news sources."

Rules:
- Be concise, factual, and neutral
- Avoid speculation or personal opinions
- Always cite sources
- Output must be JSON-friendly text suitable for a mobile app
- No emojis or special formatting
- Use simple, globally understandable English"""
    
    @staticmethod
    def create_rag_prompt(query: str, context: str) -> str:
        """Create RAG prompt with query and context"""
        return f"""{PromptTemplate.SYSTEM_PROMPT}

RETRIEVED NEWS CONTEXT:
{context}

USER QUERY:
{query}

ANSWER:"""
    
    @staticmethod
    def create_summarization_prompt(article_text: str, max_length: int = 300) -> str:
        """Create summarization prompt"""
        return f"""Summarize the following news article in {max_length} words or less.
Be concise and capture the key points.

ARTICLE:
{article_text}

SUMMARY:"""
    
    @staticmethod
    def create_sentiment_analysis_prompt(article_text: str) -> str:
        """Create sentiment analysis prompt"""
        return f"""Analyze the sentiment of the following news article.
Respond in JSON format with: {{"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0, "reason": "brief explanation"}}

ARTICLE:
{article_text}

ANALYSIS:"""


# Global instances (will be initialized on startup)
embedding_model: Optional[EmbeddingModel] = None
vector_db: Optional[VectorDatabase] = None
retriever: Optional[Retriever] = None


def init_rag_components():
    """Initialize RAG components"""
    global embedding_model, vector_db, retriever
    
    try:
        embedding_model = EmbeddingModel(settings.EMBEDDING_MODEL)
        vector_db = VectorDatabase(embedding_dim=384)
        retriever = Retriever(embedding_model, vector_db)
        logger.info("RAG components initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG components: {e}")
        raise
