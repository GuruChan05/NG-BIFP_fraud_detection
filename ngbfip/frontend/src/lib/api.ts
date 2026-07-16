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

export default api
