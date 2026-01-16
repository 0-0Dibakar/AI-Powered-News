"""News ingestion pipeline"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import asyncio
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import IngestionException
from app.nlp.processors import SentimentAnalyzer, NamedEntityRecognizer, TopicExtractor, TextCleaner
from app.rag.pipeline import embedding_model, vector_db, TextChunker


class NewsDataLoader:
    """Load news from various sources"""
    
    @staticmethod
    async def load_from_newsapi(api_key: str, category: str = "general", limit: int = 50) -> List[Dict[str, Any]]:
        """Load news from NewsAPI"""
        try:
            import httpx
            
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "country": "us",
                "category": category,
                "pageSize": limit,
                "apiKey": api_key,
                "sortBy": "publishedAt"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            articles = []
            for article in data.get("articles", []):
                articles.append({
                    "title": article.get("title"),
                    "content": article.get("content") or article.get("description"),
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name", "NewsAPI"),
                    "published_at": article.get("publishedAt"),
                    "category": category
                })
            
            logger.info(f"Loaded {len(articles)} articles from NewsAPI")
            return articles
        except Exception as e:
            logger.error(f"Failed to load from NewsAPI: {e}")
            return []
    
    @staticmethod
    async def load_from_rss(rss_url: str) -> List[Dict[str, Any]]:
        """Load news from RSS feed"""
        try:
            import feedparser
            
            feed = feedparser.parse(rss_url)
            articles = []
            
            for entry in feed.entries[:50]:
                articles.append({
                    "title": entry.get("title"),
                    "content": entry.get("summary"),
                    "url": entry.get("link"),
                    "source": feed.feed.get("title", "RSS Feed"),
                    "published_at": entry.get("published"),
                    "category": "general"
                })
            
            logger.info(f"Loaded {len(articles)} articles from RSS: {rss_url}")
            return articles
        except Exception as e:
            logger.error(f"Failed to load from RSS {rss_url}: {e}")
            return []


class NewsDataProcessor:
    """Process and enrich news articles"""
    
    def __init__(self):
        """Initialize processor"""
        self.cleaner = TextCleaner()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.ner = NamedEntityRecognizer()
        self.topic_extractor = TopicExtractor()
    
    def process_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Process single article"""
        try:
            # Clean content
            content = article.get("content", "")
            cleaned_content = self.cleaner.clean_text(content)
            
            # Generate summary
            summary = self.cleaner.extract_summary_sentences(cleaned_content, n_sentences=3)
            
            # Sentiment analysis
            sentiment = self.sentiment_analyzer.analyze(cleaned_content)
            
            # NER
            entities = self.ner.extract_entities(cleaned_content)
            
            # Topic extraction
            topics = self.topic_extractor.extract_topics_simple(cleaned_content, n_topics=3)
            main_topic = topics[0] if topics else "General"
            
            # Add processed data
            article.update({
                "content": cleaned_content,
                "summary": summary,
                "sentiment_score": sentiment["sentiment_score"],
                "sentiment_label": sentiment["sentiment_label"],
                "entities": entities,
                "main_topic": main_topic
            })
            
            return article
        except Exception as e:
            logger.error(f"Failed to process article: {e}")
            return article
    
    async def process_batch(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process batch of articles"""
        processed = []
        for article in articles:
            processed.append(self.process_article(article))
        return processed


class NewsIndexer:
    """Index articles into vector DB"""
    
    def __init__(self):
        """Initialize indexer"""
        self.chunker = TextChunker(
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP
        )
    
    async def index_articles(self, articles: List[Dict[str, Any]]) -> None:
        """Index articles into vector DB"""
        try:
            if not embedding_model or not vector_db:
                logger.warning("RAG components not initialized, skipping indexing")
                return
            
            chunk_texts = []
            chunk_ids = []
            article_ids = []
            
            for article in articles:
                article_id = article.get("id") or str(uuid.uuid4())
                article["id"] = article_id
                
                content = article.get("content", "")
                if not content:
                    continue
                
                # Chunk the content
                chunks = self.chunker.chunk_text(content, chunk_id_prefix=article_id)
                
                for chunk_id, chunk_text in chunks:
                    chunk_texts.append(chunk_text)
                    chunk_ids.append(chunk_id)
                    article_ids.append(article_id)
            
            if not chunk_texts:
                logger.warning("No chunks to index")
                return
            
            # Generate embeddings
            embeddings = embedding_model.encode(chunk_texts)
            
            # Add to vector DB
            vector_db.add(embeddings, chunk_ids)
            
            logger.info(f"Indexed {len(chunk_texts)} chunks from {len(articles)} articles")
        except Exception as e:
            logger.error(f"Failed to index articles: {e}")
            raise IngestionException(f"Indexing failed: {e}")


class IngestionPipeline:
    """Complete news ingestion pipeline"""
    
    def __init__(self):
        """Initialize pipeline"""
        self.loader = NewsDataLoader()
        self.processor = NewsDataProcessor()
        self.indexer = NewsIndexer()
    
    async def ingest(self, source: str = "newsapi") -> List[Dict[str, Any]]:
        """
        Run complete ingestion pipeline
        
        Returns:
            List of processed and indexed articles
        """
        try:
            logger.info(f"Starting ingestion from {source}")
            
            # Load articles
            if source == "newsapi" and settings.NEWSAPI_KEY:
                articles = await self.loader.load_from_newsapi(
                    settings.NEWSAPI_KEY,
                    limit=settings.INGESTION_BATCH_SIZE
                )
            else:
                articles = []
            
            if not articles:
                logger.warning(f"No articles loaded from {source}")
                return []
            
            # Process articles
            processed_articles = await self.processor.process_batch(articles)
            
            # Index articles
            await self.indexer.index_articles(processed_articles)
            
            logger.info(f"Ingestion complete: {len(processed_articles)} articles processed")
            return processed_articles
        except Exception as e:
            logger.error(f"Ingestion pipeline failed: {e}")
            raise IngestionException(f"Ingestion failed: {e}")
