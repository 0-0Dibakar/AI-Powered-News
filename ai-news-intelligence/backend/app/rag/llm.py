"""LLM integration and inference"""

from typing import Optional, Dict, Any
import os
from app.core.config import settings
from app.core.logging import logger
from app.rag.pipeline import PromptTemplate


class LLMProvider:
    """LLM provider interface"""
    
    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
        """Generate response from LLM"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI provider"""
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key or settings.OPENAI_API_KEY)
            self.model = settings.LLM_MODEL
            logger.info(f"Initialized OpenAI provider with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI provider: {e}")
            raise
    
    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
        """Generate response using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise


class LocalLLMProvider(LLMProvider):
    """Local LLM provider (e.g., LLaMA)"""
    
    def __init__(self, model_name: str = "llama-2-13b"):
        """Initialize local LLM provider"""
        try:
            # For this example, we'll use a simple mock
            # In production, integrate with LLaMA, Mistral, or similar
            self.model_name = model_name
            logger.info(f"Initialized local LLM provider with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize local LLM provider: {e}")
            raise
    
    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
        """Generate response using local LLM"""
        # This is a placeholder. In production, integrate with actual local LLM
        logger.warning("Using mock local LLM provider. Integration required for production.")
        
        # Return a placeholder response structure
        return f"[Local LLM Response] {prompt[:100]}... (not implemented)"


class RAGEngine:
    """Main RAG inference engine"""
    
    def __init__(self, llm_provider: LLMProvider):
        """Initialize RAG engine"""
        self.llm = llm_provider
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS
    
    def answer_query(self, query: str, context: str) -> Dict[str, Any]:
        """
        Answer query using RAG
        
        Args:
            query: User query
            context: Retrieved context from vector DB
        
        Returns:
            Dict with answer and metadata
        """
        try:
            prompt = PromptTemplate.create_rag_prompt(query, context)
            
            answer = self.llm.generate(
                prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Check if LLM explicitly stated no relevant information
            if "no relevant information" in answer.lower():
                return {
                    "answer": "No relevant information found in the available news sources.",
                    "status": "no_results",
                    "confidence": 0.0
                }
            
            return {
                "answer": answer,
                "status": "success",
                "confidence": 0.8  # Estimated confidence
            }
        except Exception as e:
            logger.error(f"Query answering failed: {e}")
            raise
    
    def summarize_article(self, article_text: str, max_length: int = 300) -> str:
        """Summarize article using LLM"""
        try:
            prompt = PromptTemplate.create_summarization_prompt(article_text, max_length)
            summary = self.llm.generate(prompt, temperature=0.2, max_tokens=max_length)
            return summary
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            raise
    
    def analyze_sentiment(self, article_text: str) -> Dict[str, Any]:
        """Analyze sentiment using LLM"""
        try:
            prompt = PromptTemplate.create_sentiment_analysis_prompt(article_text)
            response = self.llm.generate(prompt, temperature=0.1, max_tokens=100)
            
            # Parse JSON response
            import json
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse sentiment response as JSON: {response}")
                return {"sentiment": "neutral", "confidence": 0.5, "reason": "Parse error"}
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise


# Global instance
rag_engine: Optional[RAGEngine] = None


def init_rag_engine():
    """Initialize RAG engine with LLM provider"""
    global rag_engine
    
    try:
        if settings.OPENAI_API_KEY:
            llm_provider = OpenAIProvider(settings.OPENAI_API_KEY)
        else:
            llm_provider = LocalLLMProvider(settings.LLM_MODEL)
        
        rag_engine = RAGEngine(llm_provider)
        logger.info("RAG engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG engine: {e}")
        raise
