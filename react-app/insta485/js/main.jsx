import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./post";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
// <Post url="/api/v1/posts/1/> commented out
root.render(
  <StrictMode>
    <App url="/api/v1/posts/" />
  </StrictMode>,
);
