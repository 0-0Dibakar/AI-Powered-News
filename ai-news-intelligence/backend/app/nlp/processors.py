"""NLP processing utilities"""

from typing import List, Dict, Any, Tuple
import json
from app.core.logging import logger


class SentimentAnalyzer:
    """Sentiment analysis using VADER and TextBlob"""
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        try:
            from textblob import TextBlob
            import nltk
            nltk.download('vader_lexicon', quiet=True)
            from nltk.sentiment import SentimentIntensityAnalyzer
            
            self.textblob = TextBlob
            self.vader = SentimentIntensityAnalyzer()
            logger.info("Sentiment analyzer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analyzer: {e}")
            raise
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text
        
        Returns:
            Dict with sentiment_score (-1 to 1), sentiment_label, confidence
        """
        try:
            # Use VADER for quick analysis
            scores = self.vader.polarity_scores(text)
            compound = scores['compound']
            
            # Map compound score to label
            if compound >= 0.05:
                label = "positive"
            elif compound <= -0.05:
                label = "negative"
            else:
                label = "neutral"
            
            return {
                "sentiment_score": compound,
                "sentiment_label": label,
                "confidence": max(scores['pos'], scores['neg'], scores['neu'])
            }
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral",
                "confidence": 0.0
            }


class NamedEntityRecognizer:
    """Named Entity Recognition using spaCy"""
    
    def __init__(self, model: str = "en_core_web_sm"):
        """Initialize NER"""
        try:
            import spacy
            self.nlp = spacy.load(model)
            logger.info(f"NER initialized with model: {model}")
        except Exception as e:
            logger.warning(f"Failed to load spaCy model: {e}. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Returns:
            Dict with entity types as keys and lists of entities as values
        """
        if not self.nlp:
            return {}
        
        try:
            doc = self.nlp(text[:1000])  # Limit text length
            
            entities = {
                "PERSON": [],
                "ORG": [],
                "GPE": [],  # Geopolitical entities
                "DATE": [],
                "EVENT": []
            }
            
            for ent in doc.ents:
                ent_type = ent.label_
                if ent_type in entities:
                    if ent.text not in entities[ent_type]:
                        entities[ent_type].append(ent.text)
            
            # Remove empty categories
            return {k: v for k, v in entities.items() if v}
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return {}


class TopicExtractor:
    """Topic extraction"""
    
    @staticmethod
    def extract_topics_simple(text: str, n_topics: int = 3) -> List[str]:
        """
        Simple topic extraction using TF-IDF-like approach
        Returns list of important noun phrases
        """
        try:
            import nltk
            from nltk import word_tokenize, pos_tag
            from nltk.corpus import stopwords
            
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            # Tokenize and tag
            tokens = word_tokenize(text.lower())
            tagged = pos_tag(tokens)
            
            # Extract nouns
            stop_words = set(stopwords.words('english'))
            nouns = [
                word for word, pos in tagged
                if pos.startswith('NN') and word not in stop_words
            ]
            
            # Return most common
            from collections import Counter
            noun_freq = Counter(nouns)
            return [word for word, _ in noun_freq.most_common(n_topics)]
        except Exception as e:
            logger.error(f"Topic extraction failed: {e}")
            return []


class TextCleaner:
    """Text cleaning and preprocessing"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        try:
            import re
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Remove URLs
            text = re.sub(r'http\S+|www\S+', '', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s.,!?-]', '', text)
            
            return text
        except Exception as e:
            logger.error(f"Text cleaning failed: {e}")
            return text
    
    @staticmethod
    def extract_summary_sentences(text: str, n_sentences: int = 3) -> str:
        """Extract top sentences as summary"""
        try:
            import nltk
            from nltk.tokenize import sent_tokenize
            from nltk.corpus import stopwords
            
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            
            sentences = sent_tokenize(text)
            
            if len(sentences) <= n_sentences:
                return text
            
            # Simple scoring: favor sentences with important words
            stop_words = set(stopwords.words('english'))
            
            def score_sentence(sent: str) -> float:
                words = [w.lower() for w in sent.split() if w.lower() not in stop_words]
                return len(words) / len(sent.split()) if sent.split() else 0
            
            scored_sentences = [(i, score_sentence(s), s) for i, s in enumerate(sentences)]
            top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:n_sentences]
            top_sentences = sorted(top_sentences, key=lambda x: x[0])  # Restore order
            
            return " ".join([s[2] for s in top_sentences])
        except Exception as e:
            logger.error(f"Summary extraction failed: {e}")
            return text[:500]


class TrendAnalyzer:
    """Trend detection over time"""
    
    @staticmethod
    def detect_trending_topics(articles: List[Dict[str, Any]], time_window_hours: int = 24) -> List[Dict[str, Any]]:
        """
        Detect trending topics in articles
        
        Args:
            articles: List of article dicts with 'main_topic' and 'published_at'
            time_window_hours: Time window for trend detection
        
        Returns:
            List of trending topics with frequency and sentiment
        """
        from datetime import datetime, timedelta
        from collections import defaultdict
        
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        recent_articles = [
            a for a in articles
            if a.get('published_at') and a['published_at'] > cutoff_time
        ]
        
        topic_stats = defaultdict(lambda: {"count": 0, "sentiment_sum": 0})
        
        for article in recent_articles:
            topic = article.get('main_topic', 'General')
            topic_stats[topic]["count"] += 1
            topic_stats[topic]["sentiment_sum"] += article.get('sentiment_score', 0)
        
        # Format results
        trends = []
        for topic, stats in sorted(
            topic_stats.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        ):
            trends.append({
                "topic": topic,
                "frequency": stats["count"],
                "sentiment_avg": stats["sentiment_sum"] / stats["count"] if stats["count"] > 0 else 0,
                "articles_count": stats["count"],
                "period": f"{time_window_hours}h"
            })
        
        return trends[:20]  # Return top 20 trends
