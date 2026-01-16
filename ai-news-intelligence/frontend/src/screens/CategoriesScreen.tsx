/**
 * Categories Screen
 */

import React, { useState } from "react";
import {
  View,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Text,
} from "react-native";
import { useAppDispatch } from "@store/index";
import { setCategory, fetchNewsByCategory } from "@store/slices/newsSlice";

const CATEGORIES = [
  "business",
  "technology",
  "politics",
  "sports",
  "health",
  "science",
  "entertainment",
  "world",
];

const CategoriesScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const dispatch = useAppDispatch();
  const [selectedCategory, setSelectedCategory] = useState("general");

  const handleCategoryPress = async (category: string) => {
    setSelectedCategory(category);
    dispatch(setCategory(category));
    await dispatch(fetchNewsByCategory({ category, page: 1 }));
    navigation.navigate("Home");
  };

  return (
    <ScrollView style={styles.container}>
      <TouchableOpacity
        style={[
          styles.categoryButton,
          selectedCategory === "general" && styles.selectedButton,
        ]}
        onPress={() => handleCategoryPress("general")}
      >
        <Text
          style={[
            styles.categoryText,
            selectedCategory === "general" && styles.selectedText,
          ]}
        >
          Top Headlines
        </Text>
      </TouchableOpacity>

      {CATEGORIES.map((category) => (
        <TouchableOpacity
          key={category}
          style={[
            styles.categoryButton,
            selectedCategory === category && styles.selectedButton,
          ]}
          onPress={() => handleCategoryPress(category)}
        >
          <Text
            style={[
              styles.categoryText,
              selectedCategory === category && styles.selectedText,
            ]}
          >
            {category.charAt(0).toUpperCase() + category.slice(1)}
          </Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f5f5f5",
    padding: 16,
  },
  categoryButton: {
    backgroundColor: "#fff",
    paddingVertical: 16,
    paddingHorizontal: 12,
    marginBottom: 8,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: "#ddd",
  },
  selectedButton: {
    borderColor: "#0066cc",
    backgroundColor: "#e3f2fd",
  },
  categoryText: {
    fontSize: 16,
    fontWeight: "500",
    color: "#333",
  },
  selectedText: {
    color: "#0066cc",
    fontWeight: "600",
  },
});

export default CategoriesScreen;
