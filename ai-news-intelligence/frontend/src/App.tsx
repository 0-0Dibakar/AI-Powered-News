/**
 * Main App Navigation
 */

import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Text, View } from "react-native";

import HomeScreen from "@screens/HomeScreen";
import SearchScreen from "@screens/SearchScreen";
import CategoriesScreen from "@screens/CategoriesScreen";
import SummaryScreen from "@screens/SummaryScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const HomeStack = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: "#0066cc" },
        headerTintColor: "#fff",
        headerTitleStyle: { fontWeight: "600" },
      }}
    >
      <Stack.Screen
        name="HomeTab"
        component={HomeScreen}
        options={{ title: "Top Headlines" }}
      />
      <Stack.Screen
        name="Summary"
        component={SummaryScreen}
        options={{ title: "Article Summary" }}
      />
    </Stack.Navigator>
  );
};

const CategoriesStack = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: "#0066cc" },
        headerTintColor: "#fff",
        headerTitleStyle: { fontWeight: "600" },
      }}
    >
      <Stack.Screen
        name="CategoriesTab"
        component={CategoriesScreen}
        options={{ title: "Categories" }}
      />
    </Stack.Navigator>
  );
};

const SearchStack = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: "#0066cc" },
        headerTintColor: "#fff",
        headerTitleStyle: { fontWeight: "600" },
      }}
    >
      <Stack.Screen
        name="SearchTab"
        component={SearchScreen}
        options={{ title: "Search & Ask AI" }}
      />
      <Stack.Screen
        name="Summary"
        component={SummaryScreen}
        options={{ title: "Article Summary" }}
      />
    </Stack.Navigator>
  );
};

const App = () => {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          headerShown: false,
          tabBarActiveTintColor: "#0066cc",
          tabBarInactiveTintColor: "#999",
          tabBarStyle: {
            borderTopColor: "#ddd",
            backgroundColor: "#fff",
          },
          tabBarLabel: ({ focused, color }) => {
            const label =
              route.name === "HomeStack"
                ? "Home"
                : route.name === "CategoriesStack"
                ? "Categories"
                : "Search";
            return (
              <Text style={{ color, fontSize: 11, fontWeight: "600" }}>
                {label}
              </Text>
            );
          },
        })}
      >
        <Tab.Screen
          name="HomeStack"
          component={HomeStack}
          options={{
            tabBarLabel: "Home",
          }}
        />
        <Tab.Screen
          name="CategoriesStack"
          component={CategoriesStack}
          options={{
            tabBarLabel: "Categories",
          }}
        />
        <Tab.Screen
          name="SearchStack"
          component={SearchStack}
          options={{
            tabBarLabel: "Search",
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
};

export default App;
