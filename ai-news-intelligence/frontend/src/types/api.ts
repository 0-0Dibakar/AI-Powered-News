/**
 * Types for API responses and data models
 */

export interface Article {
  id: string;
  url: string;
  title: string;
  content?: string;
  summary?: string;
  source: string;
  category?: string;
  published_at?: string;
  sentiment_score?: number;
  sentiment_label?: "positive" | "negative" | "neutral";
  main_topic?: string;
  created_at: string;
}

export interface QueryRequest {
  query: string;
  category?: string;
}

export interface RAGResponse {
  answer: string;
  sources: Article[];
  confidence_score?: number;
  status: "success" | "no_results" | "error";
}

export interface SummarizeRequest {
  article_id: string;
  max_length?: number;
}

export interface SummarizeResponse {
  article_id: string;
  summary: string;
  original_length: number;
  summary_length: number;
}

export interface SentimentAnalysis {
  article_id: string;
  sentiment_score: number;
  sentiment_label: "positive" | "negative" | "neutral";
  confidence: number;
}

export interface TrendingTopic {
  topic: string;
  frequency: number;
  sentiment_avg: number;
  articles_count: number;
  period: string;
}

export interface HeadlinesResponse {
  articles: Article[];
  total_count: number;
  page: number;
  page_size: number;
}

export interface ApiError {
  status: string;
  detail: string;
  error_code?: string;
}
