import axios from "axios";

const API = axios.create({
  baseURL: "https://ai-resume-analyzer-backend-7nj5.onrender.com"
});

export default API;