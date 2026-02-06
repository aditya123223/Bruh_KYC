import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // replace with your backend
});

export default api;
