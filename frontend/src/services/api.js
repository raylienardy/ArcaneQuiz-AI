import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "https://arcane-quiz-ai.vercel.app",
  timeout: 30000,
  headers: { "Content-Type": "application/json" },
});

export default api;
