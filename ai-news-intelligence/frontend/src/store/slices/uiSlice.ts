/**
 * UI slice for Redux
 */

import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface UIState {
  theme: "light" | "dark";
  selectedArticleId: string | null;
  showSummary: boolean;
  showSentiment: boolean;
}

const initialState: UIState = {
  theme: "light",
  selectedArticleId: null,
  showSummary: false,
  showSentiment: false,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    toggleTheme: (state) => {
      state.theme = state.theme === "light" ? "dark" : "light";
    },
    selectArticle: (state, action: PayloadAction<string>) => {
      state.selectedArticleId = action.payload;
    },
    clearSelection: (state) => {
      state.selectedArticleId = null;
      state.showSummary = false;
      state.showSentiment = false;
    },
    toggleSummary: (state) => {
      state.showSummary = !state.showSummary;
    },
    toggleSentiment: (state) => {
      state.showSentiment = !state.showSentiment;
    },
  },
});

export const {
  toggleTheme,
  selectArticle,
  clearSelection,
  toggleSummary,
  toggleSentiment,
} = uiSlice.actions;
export default uiSlice.reducer;
