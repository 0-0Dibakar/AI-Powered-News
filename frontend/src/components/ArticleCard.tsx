/**
 * Article Card Component
 */

import React from "react";
import { View, TouchableOpacity, StyleSheet, Text, Image } from "react-native";
import { Article } from "@types/api";

interface ArticleCardProps {
  article: Article;
  onPress: () => void;
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, onPress }) => {
  const getSentimentColor = (label?: string) => {
    switch (label) {
      case "positive":
        return "#4CAF50";
      case "negative":
        return "#f44336";
      default:
        return "#FFC107";
    }
  };

  return (
    <TouchableOpacity style={styles.card} onPress={onPress}>
      <View style={styles.content}>
        <Text style={styles.title} numberOfLines={2}>
          {article.title}
        </Text>

        <Text style={styles.source}>{article.source}</Text>

        {article.sentiment_label && (
          <View style={styles.badgeContainer}>
            <View
              style={[
                styles.sentimentBadge,
                { backgroundColor: getSentimentColor(article.sentiment_label) },
              ]}
            >
              <Text style={styles.badgeText}>
                {article.sentiment_label.substring(0, 1).toUpperCase()}
              </Text>
            </View>
            {article.main_topic && (
              <View style={styles.topicBadge}>
                <Text style={styles.topicText}>{article.main_topic}</Text>
              </View>
            )}
          </View>
        )}

        <Text style={styles.date}>
          {article.published_at
            ? new Date(article.published_at).toLocaleDateString()
            : ""}
        </Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: "#fff",
    marginBottom: 8,
    marginHorizontal: 8,
    borderRadius: 8,
    overflow: "hidden",
    elevation: 2,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 1.41,
  },
  content: {
    padding: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: "600",
    color: "#222",
    marginBottom: 8,
  },
  source: {
    fontSize: 12,
    color: "#666",
    marginBottom: 8,
  },
  badgeContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
    gap: 8,
  },
  sentimentBadge: {
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 4,
  },
  badgeText: {
    color: "#fff",
    fontSize: 11,
    fontWeight: "600",
  },
  topicBadge: {
    backgroundColor: "#e0e0e0",
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 4,
  },
  topicText: {
    fontSize: 11,
    color: "#333",
  },
  date: {
    fontSize: 12,
    color: "#999",
  },
});

export default ArticleCard;
