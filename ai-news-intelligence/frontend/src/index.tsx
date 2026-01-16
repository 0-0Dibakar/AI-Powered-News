/**
 * App Entry Point
 */

import React from "react";
import { Provider } from "react-redux";
import { store } from "@store/index";
import App from "./App";

export default function Root() {
  return (
    <Provider store={store}>
      <App />
    </Provider>
  );
}
