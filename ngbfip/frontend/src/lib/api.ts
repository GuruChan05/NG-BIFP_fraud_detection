import axios, { AxiosInstance, AxiosError } from 'axios'
import { useAuthStore } from '@/stores/auth.store'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add token
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// Auth API
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/users/me'),
}

// Users API
export const usersAPI = {
  getMe: () => api.get('/users/me'),
  getUser: (id: string) => api.get(`/users/${id}`),
  createUser: (data: any) => api.post('/users', data),
  updateUser: (id: string, data: any) => api.put(`/users/${id}`, data),
  deleteUser: (id: string) => api.delete(`/users/${id}`),
}

// Transactions API
export const transactionsAPI = {
  list: (params?: any) => api.get('/transactions', { params }),
  get: (id: string) => api.get(`/transactions/${id}`),
  create: (data: any) => api.post('/transactions', data),
  update: (id: string, data: any) => api.put(`/transactions/${id}`, data),
  getUserTransactions: (userId: string) =>
    api.get(`/transactions/user/${userId}`),
}

// Risk API
export const riskAPI = {
  analyze: (data: any) => api.post('/risk/analyze', data),
  getTrends: (params?: any) => api.get('/risk/trends', { params }),
}

// Alerts API
export const alertsAPI = {
  list: (params?: any) => api.get('/alerts', { params }),
  get: (id: string) => api.get(`/alerts/${id}`),
  create: (data: any) => api.post('/alerts', data),
  resolve: (id: string, data: any) =>
    api.put(`/alerts/${id}/resolve`, data),
}

// Devices API
export const devicesAPI = {
  list: (params?: any) => api.get('/devices', { params }),
  get: (id: string) => api.get(`/devices/${id}`),
  create: (data: any) => api.post('/devices', data),
  updateTrust: (id: string, data: any) =>
    api.put(`/devices/${id}/trust`, data),
}

// Dashboard API
export const dashboardAPI = {
  getOverview: () => api.get('/dashboard/overview'),
  getStatistics: (params?: any) =>
    api.get('/dashboard/statistics', { params }),
}

// Health API
export const healthAPI = {
  check: () => api.get('/health'),
}
