/**
 * Home Screen - Top Headlines
 */

import React, { useEffect, useState } from "react";
import {
  View,
  FlatList,
  StyleSheet,
  RefreshControl,
  ActivityIndicator,
} from "react-native";
import { useAppDispatch, useAppSelector } from "@store/index";
import { fetchHeadlines, setPage } from "@store/slices/newsSlice";
import ArticleCard from "@components/ArticleCard";

const HomeScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const dispatch = useAppDispatch();
  const { headlines, loading, error } = useAppSelector((state) => state.news);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadHeadlines();
  }, []);

  const loadHeadlines = async () => {
    await dispatch(fetchHeadlines({ category: "general", page: 1 }));
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadHeadlines();
    setRefreshing(false);
  };

  const handleArticlePress = (articleId: string) => {
    navigation.navigate("Summary", { articleId });
  };

  if (loading && !headlines.length) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0066cc" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={headlines}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <ArticleCard
            article={item}
            onPress={() => handleArticlePress(item.id)}
          />
        )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.listContent}
      />
      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  listContent: {
    paddingVertical: 8,
  },
  errorContainer: {
    backgroundColor: "#ffebee",
    padding: 12,
    margin: 8,
    borderRadius: 8,
  },
  errorText: {
    color: "#c62828",
    fontSize: 14,
  },
});

export default HomeScreen;
