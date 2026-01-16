/**
 * Search slice for Redux
 */

import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { Article, RAGResponse, HeadlinesResponse } from "@types/api";
import apiService from "@services/apiService";

interface SearchState {
  query: string;
  results: Article[];
  ragResults: RAGResponse | null;
  loading: boolean;
  error: string | null;
  lastSearchType: "keyword" | "rag" | null;
}

const initialState: SearchState = {
  query: "",
  results: [],
  ragResults: null,
  loading: false,
  error: null,
  lastSearchType: null,
};

// Async thunks
export const searchArticles = createAsyncThunk(
  "search/searchArticles",
  async ({ q, page }: { q: string; page: number }) => {
    const response = await apiService.searchArticles(q, page);
    return response;
  }
);

export const queryWithRAG = createAsyncThunk(
  "search/queryWithRAG",
  async ({ query, category }: { query: string; category?: string }) => {
    const response = await apiService.queryWithRAG(query, category);
    return response;
  }
);

const searchSlice = createSlice({
  name: "search",
  initialState,
  reducers: {
    setQuery: (state, action: PayloadAction<string>) => {
      state.query = action.payload;
    },
    clearSearch: (state) => {
      state.query = "";
      state.results = [];
      state.ragResults = null;
      state.lastSearchType = null;
    },
  },
  extraReducers: (builder) => {
    // Search Articles
    builder
      .addCase(searchArticles.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.lastSearchType = "keyword";
      })
      .addCase(
        searchArticles.fulfilled,
        (state, action: PayloadAction<HeadlinesResponse>) => {
          state.loading = false;
          state.results = action.payload.articles;
        }
      )
      .addCase(searchArticles.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Search failed";
      });

    // Query with RAG
    builder
      .addCase(queryWithRAG.pending, (state) => {
        state.loading = true;
        state.error = null;
        state.lastSearchType = "rag";
      })
      .addCase(
        queryWithRAG.fulfilled,
        (state, action: PayloadAction<RAGResponse>) => {
          state.loading = false;
          state.ragResults = action.payload;
          state.results = action.payload.sources;
        }
      )
      .addCase(queryWithRAG.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Query failed";
      });
  },
});

export const { setQuery, clearSearch } = searchSlice.actions;
export default searchSlice.reducer;
