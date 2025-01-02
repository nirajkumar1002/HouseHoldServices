import axios from 'axios';

// Create an Axios instance
const instance = axios.create({
  baseURL: 'http://localhost:5000/api', // Set your base URL here
});

// Add a request interceptor
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers['Authorization'] = token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default instance;