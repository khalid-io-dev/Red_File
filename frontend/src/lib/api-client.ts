import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 1800000, // 30 minutes
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('token');
        console.log('[API Client] Request to:', config.url);
        console.log('[API Client] Token exists:', !!token);
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
          console.log('[API Client] Authorization header set');
        } else {
          console.warn('[API Client] No token found in localStorage!');
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor - handle errors
    this.client.interceptors.response.use(
      (response) => {
        console.log('[API Client] Response success:', response.config.url, response.status);
        return response;
      },
      (error: AxiosError) => {
        console.error('[API Client] Response error:', error.response?.status, error.response?.data);
        if (error.response?.status === 401) {
          console.error('[API Client] 401 Unauthorized - redirecting to login');
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        if (error.response?.status === 403) {
          console.error('[API Client] 403 Forbidden - auth issue');
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await this.client.post('/login/access-token', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async register(data: { email: string; password: string; full_name: string }) {
    const response = await this.client.post('/users/', data);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.client.get('/users/me');
    return response.data;
  }

  async logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // Generic CRUD methods
  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.client.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any, config?: any): Promise<T> {
    const response = await this.client.post(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.client.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response = await this.client.delete(url);
    return response.data;
  }

  async download(url: string, params?: any): Promise<Blob> {
    const response = await this.client.get(url, { params, responseType: 'blob' });
    return response.data;
  }

  async upload<T>(
    url: string,
    fileOrFormData: File | FormData,
    onProgress?: (progress: number) => void
  ): Promise<T> {
    const formData = fileOrFormData instanceof FormData
      ? fileOrFormData
      : (() => {
          const fd = new FormData();
          fd.append('file', fileOrFormData);
          return fd;
        })();

    const response = await this.client.post(url, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
