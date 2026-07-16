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

export interface RiskDistribution {
  risk_level: string
  count: number
  percentage: number
}

export interface MonthlyStatistic {
  month: string
  transactions: number
  fraud_cases: number
  risk_score: number
}

export interface WeeklyStatistic {
  week: string
  transactions: number
  fraud_cases: number
  risk_score: number
}

export interface RecentActivity {
  id: number
  user_id: number
  amount: number
  transaction_type: string
  merchant: string
  risk_score: number
  is_fraudulent: string
  created_at: string
}

export interface DashboardSummary {
  overview: DashboardOverview
  risk_distribution: RiskDistribution[]
  monthly_statistics: MonthlyStatistic[]
  weekly_statistics: WeeklyStatistic[]
  recent_activity: RecentActivity[]
}

export const dashboardAPI = {
  getOverview: () => api.get<DashboardOverview>('/dashboard/overview'),
  getStatistics: () => api.get<any>('/dashboard/statistics'),
  getRiskDistribution: () => api.get<RiskDistribution[]>('/dashboard/risk-distribution'),
  getMonthlyStatistics: () => api.get<MonthlyStatistic[]>('/dashboard/monthly-statistics'),
  getWeeklyStatistics: () => api.get<WeeklyStatistic[]>('/dashboard/weekly-statistics'),
  getRecentActivity: (limit?: number) =>
    api.get<RecentActivity[]>('/dashboard/recent-activity', { params: { limit } }),
  getSummary: () => api.get<DashboardSummary>('/dashboard/summary'),
}

export default api
