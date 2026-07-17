import { useQuery, useMutation } from '@tanstack/react-query'
import axios from 'axios'
import { getAuthToken } from './auth'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = getAuthToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface Transaction {
  id: number
  user_id: number
  amount: number
  transaction_type: string
  merchant: string
  merchant_category?: string
  location?: string
  device_id?: string
  risk_score: number
  is_fraudulent: string
  created_at: string
}

export interface TransactionListResponse {
  total: number
  page: number
  page_size: number
  total_pages: number
  data: Transaction[]
}

export interface TransactionStats {
  total_transactions: number
  total_amount: number
  average_amount: number
  fraud_count: number
  fraud_percentage: number
  legitimate_count: number
  unknown_count: number
}

export interface DashboardOverview {
  total_transactions: number
  fraud_cases: number
  active_users: number
  todays_activity: number
  average_risk_score: number
  trusted_devices: number
  high_risk_transactions: number
  resolved_alerts: number
}

export const transactionAPI = {
  list: (page = 1, pageSize = 20, filters?: any) =>
    api.get<TransactionListResponse>('/transactions/', {
      params: { page, page_size: pageSize, ...filters },
    }),
  create: (data: any) => api.post<Transaction>('/transactions/', data),
  get: (id: number) => api.get<Transaction>(`/transactions/${id}`),
  update: (id: number, data: any) => api.put<Transaction>(`/transactions/${id}`, data),
  delete: (id: number) => api.delete(`/transactions/${id}`),
  search: (query: string) => api.get<Transaction[]>('/transactions/search/query', { params: { q: query } }),
  getHistory: (userId: number) => api.get<Transaction[]>(`/transactions/user/${userId}/history`),
  getStats: () => api.get<TransactionStats>('/transactions/stats/summary'),
  importCSV: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/transactions/import/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  exportCSV: () => api.get('/transactions/export/csv'),
}

export const dashboardAPI = {
  getOverview: () => api.get<DashboardOverview>('/dashboard/overview'),
  getSummary: () => api.get<any>('/dashboard/summary'),
}

export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  register: (email: string, username: string, full_name: string, password: string, confirm_password: string) =>
    api.post('/auth/register', { email, username, full_name, password, confirm_password }),
  refresh: (refreshToken: string) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
  logout: () => api.post('/auth/logout'),
  changePassword: (old_password: string, new_password: string, confirm_password: string) =>
    api.post('/auth/change-password', { old_password, new_password, confirm_password }),
}

export const userAPI = {
  getCurrentUser: () => api.get('/users/me'),
  updateProfile: (data: any) => api.put('/users/me', data),
  getLoginHistory: (limit = 20) => api.get(`/users/me/login-history?limit=${limit}`),
  getUser: (id: number) => api.get(`/users/${id}`),
  createUser: (data: any) => api.post('/users/', data),
  updateUser: (id: number, data: any) => api.put(`/users/${id}`, data),
  deleteUser: (id: number) => api.delete(`/users/${id}`),
  activateUser: (id: number) => api.post(`/users/${id}/activate`),
  deactivateUser: (id: number) => api.post(`/users/${id}/deactivate`),
  listUsers: (skip = 0, limit = 100) => api.get('/users/', { params: { skip, limit } }),
}

export const notificationAPI = {
  list: () => api.get('/notifications/'),
  get: (id: number) => api.get(`/notifications/${id}`),
  create: (data: any) => api.post('/notifications/', data),
  markAsRead: (id: number) => api.put(`/notifications/${id}/read`),
  markAllAsRead: () => api.post('/notifications/mark-all-read'),
  delete: (id: number) => api.delete(`/notifications/${id}`),
  getUnreadCount: () => api.get('/notifications/unread/count'),
}

export default api
