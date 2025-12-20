/**
 * Axios API Client for Django Backend
 * Handles authentication, token refresh, and error handling
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

// API Base URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for cookies
});

// Store for access token (in-memory, not localStorage)
let accessToken: string | null = null;

// Flag to prevent multiple refresh attempts
let isRefreshing = false;

export const setAccessToken = (token: string | null) => {
  accessToken = token;
};

export const getAccessToken = () => accessToken;

export const clearAccessToken = () => {
  accessToken = null;
};

// Request interceptor - add access token to requests
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (accessToken && config.headers) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { 
      _retry?: boolean;
      _isRefreshRequest?: boolean;
    };

    // Don't retry refresh requests to avoid infinite loop
    if (originalRequest._isRefreshRequest) {
      return Promise.reject(error);
    }

    // If 401 and we haven't retried yet and not currently refreshing
    if (error.response?.status === 401 && !originalRequest._retry && !isRefreshing) {
      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Try to refresh the token using raw axios (not the api instance)
        const refreshResponse = await axios.post(
          `${API_URL}/api/admin/auth/refresh/`,
          {},
          { withCredentials: true }
        );

        isRefreshing = false;

        if (refreshResponse.data.success && refreshResponse.data.access) {
          // Store new access token
          setAccessToken(refreshResponse.data.access);

          // Update the original request with new token
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
          }

          // Retry the original request
          return api(originalRequest);
        }
      } catch (refreshError) {
        isRefreshing = false;
        // Refresh failed, clear token
        clearAccessToken();
        
        // Only redirect if we're on a protected page (not login)
        if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
          window.location.href = '/admin/login';
        }
        
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// Auth-specific API functions
export const authApi = {
  /**
   * Login admin user
   */
  login: async (email: string, password: string) => {
    const response = await api.post('/api/admin/auth/login/', {
      email,
      password,
    });
    
    if (response.data.success && response.data.access) {
      setAccessToken(response.data.access);
    }
    
    return response.data;
  },

  /**
   * Logout admin user
   */
  logout: async () => {
    try {
      await api.post('/api/admin/auth/logout/');
    } finally {
      clearAccessToken();
    }
  },

  /**
   * Refresh access token - uses raw axios to avoid interceptor loop
   */
  refresh: async () => {
    try {
      // Use raw axios to avoid the interceptor trying to refresh on 401
      const response = await axios.post(
        `${API_URL}/api/admin/auth/refresh/`,
        {},
        { withCredentials: true }
      );
      
      if (response.data.success && response.data.access) {
        setAccessToken(response.data.access);
      }
      
      return response.data;
    } catch (error: any) {
      // Return a failed response object instead of throwing
      return { 
        success: false, 
        message: error.response?.data?.message || 'Token refresh failed' 
      };
    }
  },

  /**
   * Get current user
   */
  getMe: async () => {
    const response = await api.get('/api/admin/auth/me/');
    return response.data;
  },

  /**
   * Verify token
   */
  verify: async () => {
    const response = await api.post('/api/admin/auth/verify/');
    return response.data;
  },
};
