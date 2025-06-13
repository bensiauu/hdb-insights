import "./index.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";

console.log("CSS should be loading");

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <div className="bg-gradient-to-tr from-blue-50 via-white to-green-100 font-inter text-gray-900 min-h-screen">
      <App />
    </div>
  </StrictMode>,
);
