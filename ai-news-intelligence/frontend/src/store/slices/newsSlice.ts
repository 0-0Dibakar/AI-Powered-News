/**
 * News slice for Redux
 */

import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { Article, HeadlinesResponse } from "@types/api";
import apiService from "@services/apiService";

interface NewsState {
  headlines: Article[];
  currentCategory: string;
  loading: boolean;
  error: string | null;
  totalCount: number;
  currentPage: number;
}

const initialState: NewsState = {
  headlines: [],
  currentCategory: "general",
  loading: false,
  error: null,
  totalCount: 0,
  currentPage: 1,
};

// Async thunks
export const fetchHeadlines = createAsyncThunk(
  "news/fetchHeadlines",
  async ({ category, page }: { category: string; page: number }) => {
    const response = await apiService.getHeadlines(category, page);
    return response;
  }
);

export const fetchNewsByCategory = createAsyncThunk(
  "news/fetchByCategory",
  async ({ category, page }: { category: string; page: number }) => {
    const response = await apiService.getNewsByCategory(category, page);
    return response;
  }
);

const newsSlice = createSlice({
  name: "news",
  initialState,
  reducers: {
    setCategory: (state, action: PayloadAction<string>) => {
      state.currentCategory = action.payload;
      state.currentPage = 1;
    },
    setPage: (state, action: PayloadAction<number>) => {
      state.currentPage = action.payload;
    },
  },
  extraReducers: (builder) => {
    // Fetch Headlines
    builder
      .addCase(fetchHeadlines.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchHeadlines.fulfilled,
        (state, action: PayloadAction<HeadlinesResponse>) => {
          state.loading = false;
          state.headlines = action.payload.articles;
          state.totalCount = action.payload.total_count;
          state.currentPage = action.payload.page;
        }
      )
      .addCase(fetchHeadlines.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to fetch headlines";
      });

    // Fetch By Category
    builder
      .addCase(fetchNewsByCategory.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(
        fetchNewsByCategory.fulfilled,
        (state, action: PayloadAction<HeadlinesResponse>) => {
          state.loading = false;
          state.headlines = action.payload.articles;
          state.totalCount = action.payload.total_count;
          state.currentPage = action.payload.page;
        }
      )
      .addCase(fetchNewsByCategory.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to fetch news";
      });
  },
});

export const { setCategory, setPage } = newsSlice.actions;
export default newsSlice.reducer;
