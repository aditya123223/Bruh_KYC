import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// 🔐 attach API key automatically
api.interceptors.request.use((config) => {
  config.headers["x-api-key"] = "hackathon-demo-key";
  return config;
});

export default api;

