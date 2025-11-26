import axios from "axios";

const apiInstance = axios.create({
  baseURL: `${import.meta.env.VITE_DEV_API_BASE_URL}/api/`,
  timeout: 1000,
  headers: { "Content-Type": "application/json" },
});

export default apiInstance;
