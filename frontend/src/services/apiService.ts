/**
 * API service for backend communication
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {
  Article,
  QueryRequest,
  RAGResponse,
  SummarizeRequest,
  HeadlinesResponse,
  TrendingTopic,
} from "@types/api";

class ApiService {
  private axiosInstance: AxiosInstance;
  private baseURL: string;
  private apiKey: string = "mobile-app-key-123";

  constructor(baseURL: string = "http://localhost:8000/api") {
    this.baseURL = baseURL;
    this.axiosInstance = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "x-api-key": this.apiKey,
      },
    });

    // Add request interceptor
    this.axiosInstance.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem("auth_token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Handle 401 Unauthorized
        if (error.response?.status === 401) {
          AsyncStorage.removeItem("auth_token");
        }
        return Promise.reject(error);
      }
    );
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<any> {
    return this.axiosInstance.get("/health");
  }

  /**
   * Get top headlines
   */
  async getHeadlines(
    category: string = "general",
    page: number = 1,
    pageSize: number = 10
  ): Promise<HeadlinesResponse> {
    const response = await this.axiosInstance.get<HeadlinesResponse>(
      "/news/headlines",
      {
        params: { category, page, page_size: pageSize },
      }
    );
    return response.data;
  }

  /**
   * Get news by category
   */
  async getNewsByCategory(
    category: string,
    page: number = 1,
    pageSize: number = 10
  ): Promise<HeadlinesResponse> {
    const response = await this.axiosInstance.get<HeadlinesResponse>(
      `/news/category/${category}`,
      {
        params: { page, page_size: pageSize },
      }
    );
    return response.data;
  }

  /**
   * RAG-powered query
   */
  async queryWithRAG(query: string, category?: string): Promise<RAGResponse> {
    const request: QueryRequest = { query, category };
    const response = await this.axiosInstance.post<RAGResponse>(
      "/ai/query",
      request
    );
    return response.data;
  }

  /**
   * Search articles
   */
  async searchArticles(
    q: string,
    page: number = 1,
    pageSize: number = 10
  ): Promise<HeadlinesResponse> {
    const response = await this.axiosInstance.get<HeadlinesResponse>(
      "/news/search",
      {
        params: { q, page, page_size: pageSize },
      }
    );
    return response.data;
  }

  /**
   * Get trending topics
   */
  async getTrendingTopics(hours: number = 24): Promise<TrendingTopic[]> {
    const response = await this.axiosInstance.get<TrendingTopic[]>(
      "/trending/topics",
      {
        params: { hours },
      }
    );
    return response.data;
  }

  /**
   * Summarize article
   */
  async summarizeArticle(
    articleId: string,
    maxLength?: number
  ): Promise<{ article_id: string; summary: string; cached: boolean }> {
    const request: SummarizeRequest = { article_id: articleId, max_length: maxLength };
    const response = await this.axiosInstance.post(
      "/ai/summarize",
      request
    );
    return response.data;
  }

  /**
   * Get sentiment analysis
   */
  async getSentiment(articleId: string): Promise<any> {
    const response = await this.axiosInstance.get(
      `/ai/sentiment/${articleId}`
    );
    return response.data;
  }
}

// Create singleton instance
const apiService = new ApiService(
  process.env.REACT_APP_API_URL || "http://localhost:8000/api"
);

export default apiService;
