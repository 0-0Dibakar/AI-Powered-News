/**
 * Search/Ask AI Screen
 */

import React, { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Text,
} from "react-native";
import { useAppDispatch, useAppSelector } from "@store/index";
import { queryWithRAG, searchArticles, setQuery, clearSearch } from "@store/slices/searchSlice";
import ArticleCard from "@components/ArticleCard";

const SearchScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const dispatch = useAppDispatch();
  const { query, results, ragResults, loading, lastSearchType } = useAppSelector(
    (state) => state.search
  );
  const [inputValue, setInputValue] = useState("");

  const handleRAGQuery = async () => {
    if (inputValue.trim()) {
      dispatch(setQuery(inputValue));
      await dispatch(queryWithRAG({ query: inputValue }));
    }
  };

  const handleKeywordSearch = async () => {
    if (inputValue.trim()) {
      dispatch(setQuery(inputValue));
      await dispatch(searchArticles({ q: inputValue, page: 1 }));
    }
  };

  const handleClear = () => {
    setInputValue("");
    dispatch(clearSearch());
  };

  const renderRAGResults = () => {
    if (!ragResults) return null;

    return (
      <View style={styles.ragResultContainer}>
        <Text style={styles.answerLabel}>AI Answer:</Text>
        <Text style={styles.answerText}>{ragResults.answer}</Text>
        <Text style={styles.confidenceText}>
          Confidence: {(ragResults.confidence_score || 0).toFixed(2)}
        </Text>
        <Text style={styles.sourcesLabel}>Sources:</Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <TextInput
          style={styles.input}
          placeholder="Ask a question or search..."
          placeholderTextColor="#999"
          value={inputValue}
          onChangeText={setInputValue}
        />
        {inputValue ? (
          <TouchableOpacity style={styles.clearButton} onPress={handleClear}>
            <Text style={styles.clearButtonText}>✕</Text>
          </TouchableOpacity>
        ) : null}
      </View>

      <View style={styles.buttonContainer}>
        <TouchableOpacity
          style={[styles.button, styles.ragButton]}
          onPress={handleRAGQuery}
          disabled={loading}
        >
          {loading && lastSearchType === "rag" ? (
            <ActivityIndicator size="small" color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Ask AI</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.searchButton]}
          onPress={handleKeywordSearch}
          disabled={loading}
        >
          {loading && lastSearchType === "keyword" ? (
            <ActivityIndicator size="small" color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Search</Text>
          )}
        </TouchableOpacity>
      </View>

      {ragResults && renderRAGResults()}

      <FlatList
        data={results}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <ArticleCard
            article={item}
            onPress={() => navigation.navigate("Summary", { articleId: item.id })}
          />
        )}
        contentContainerStyle={styles.listContent}
        ListEmptyComponent={
          !loading ? (
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>
                {query ? "No results found" : "Search or ask a question"}
              </Text>
            </View>
          ) : null
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
    paddingTop: 16,
  },
  searchContainer: {
    flexDirection: "row",
    paddingHorizontal: 16,
    marginBottom: 12,
    alignItems: "center",
  },
  input: {
    flex: 1,
    backgroundColor: "#fff",
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    borderColor: "#ddd",
    borderWidth: 1,
  },
  clearButton: {
    marginLeft: 8,
    padding: 8,
  },
  clearButtonText: {
    fontSize: 20,
    color: "#999",
  },
  buttonContainer: {
    flexDirection: "row",
    paddingHorizontal: 16,
    marginBottom: 16,
    gap: 12,
  },
  button: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: "center",
    justifyContent: "center",
  },
  ragButton: {
    backgroundColor: "#0066cc",
  },
  searchButton: {
    backgroundColor: "#4CAF50",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  ragResultContainer: {
    marginHorizontal: 16,
    marginBottom: 16,
    backgroundColor: "#fff",
    padding: 12,
    borderRadius: 8,
  },
  answerLabel: {
    fontSize: 14,
    fontWeight: "600",
    marginBottom: 8,
  },
  answerText: {
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 8,
    color: "#333",
  },
  confidenceText: {
    fontSize: 12,
    color: "#666",
    marginBottom: 12,
  },
  sourcesLabel: {
    fontSize: 14,
    fontWeight: "600",
    marginTop: 8,
  },
  listContent: {
    paddingHorizontal: 16,
  },
  emptyContainer: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 40,
  },
  emptyText: {
    fontSize: 16,
    color: "#999",
  },
});

export default SearchScreen;
