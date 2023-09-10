// apios.ts
import axios from "axios";
const BASEURL = "http://localhost:8888"; // replace with your API endpoint

const apios = axios.create({
    baseURL: BASEURL,
  });

  // Add a request interceptor
  apios.interceptors.request.use((config) => {
    // Get the JWT token from local storage
    const jwtToken = localStorage.getItem('jwt_token');

    // If the JWT token exists, set it in the request headers
    if (jwtToken) {
      config.headers['Authorization'] = `Bearer ${jwtToken}`;
    }

    return config;
  }, (error) => {
    // Do something with request error
    return Promise.reject(error);
  });



export default apios;