/**
 * Article Summary Screen
 */

import React, { useEffect, useState } from "react";
import {
  View,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  Linking,
} from "react-native";
import apiService from "@services/apiService";
import { Article, SentimentAnalysis } from "@types/api";

interface SummaryScreenProps {
  route: any;
  navigation: any;
}

const SummaryScreen: React.FC<SummaryScreenProps> = ({
  route,
  navigation,
}) => {
  const { articleId } = route.params;
  const [article, setArticle] = useState<Article | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [sentiment, setSentiment] = useState<SentimentAnalysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadArticleDetails();
  }, [articleId]);

  const loadArticleDetails = async () => {
    try {
      setLoading(true);
      // Fetch summary and sentiment
      const [summaryRes, sentimentRes] = await Promise.all([
        apiService.summarizeArticle(articleId),
        apiService.getSentiment(articleId),
      ]);
      setSummary(summaryRes.summary);
      setSentiment(sentimentRes);
    } catch (error) {
      console.error("Error loading article details:", error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (label: string) => {
    switch (label) {
      case "positive":
        return "#4CAF50";
      case "negative":
        return "#f44336";
      default:
        return "#FFC107";
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0066cc" />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>{article?.title}</Text>
        <Text style={styles.source}>{article?.source}</Text>
        <Text style={styles.date}>
          {article?.published_at
            ? new Date(article.published_at).toLocaleDateString()
            : ""}
        </Text>

        {summary && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Summary</Text>
            <Text style={styles.summaryText}>{summary}</Text>
          </View>
        )}

        {sentiment && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Sentiment Analysis</Text>
            <View style={styles.sentimentContainer}>
              <View
                style={[
                  styles.sentimentBadge,
                  { backgroundColor: getSentimentColor(sentiment.sentiment_label) },
                ]}
              >
                <Text style={styles.sentimentLabel}>
                  {sentiment.sentiment_label.toUpperCase()}
                </Text>
              </View>
              <Text style={styles.sentimentScore}>
                Score: {(sentiment.sentiment_score * 100).toFixed(0)}%
              </Text>
            </View>
          </View>
        )}

        <TouchableOpacity
          style={styles.readMoreButton}
          onPress={() => article?.url && Linking.openURL(article.url)}
        >
          <Text style={styles.readMoreText}>Read Full Article</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
  },
  content: {
    padding: 16,
  },
  title: {
    fontSize: 20,
    fontWeight: "700",
    marginBottom: 8,
    color: "#222",
  },
  source: {
    fontSize: 14,
    color: "#666",
    fontWeight: "500",
  },
  date: {
    fontSize: 12,
    color: "#999",
    marginBottom: 16,
  },
  section: {
    backgroundColor: "#fff",
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 8,
    color: "#333",
  },
  summaryText: {
    fontSize: 14,
    lineHeight: 20,
    color: "#555",
  },
  sentimentContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  sentimentBadge: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 6,
  },
  sentimentLabel: {
    color: "#fff",
    fontSize: 12,
    fontWeight: "600",
  },
  sentimentScore: {
    fontSize: 14,
    color: "#555",
    fontWeight: "500",
  },
  readMoreButton: {
    backgroundColor: "#0066cc",
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: "center",
  },
  readMoreText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});

export default SummaryScreen;
