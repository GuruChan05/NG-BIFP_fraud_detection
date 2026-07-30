import { useQuery } from '@tanstack/react-query'
import { dashboardAPI } from '@/lib/api'

export function useDashboardOverview() {
  return useQuery({
    queryKey: ['dashboard', 'overview'],
    queryFn: async () => {
      const response = await dashboardAPI.getOverview()
      return response.data
    },
    staleTime: 1000 * 60 * 2,
    gcTime: 1000 * 60 * 5,
  })
}

export function useRiskDistribution() {
  return useQuery({
    queryKey: ['dashboard', 'risk-distribution'],
    queryFn: async () => {
      const response = await dashboardAPI.getRiskDistribution()
      return response.data
    },
    staleTime: 1000 * 60 * 5,
    gcTime: 1000 * 60 * 10,
  })
}

export function useMonthlyStatistics() {
  return useQuery({
    queryKey: ['dashboard', 'monthly-statistics'],
    queryFn: async () => {
      const response = await dashboardAPI.getMonthlyStatistics()
      return response.data
    },
    staleTime: 1000 * 60 * 10,
    gcTime: 1000 * 60 * 30,
  })
}

export function useWeeklyStatistics() {
  return useQuery({
    queryKey: ['dashboard', 'weekly-statistics'],
    queryFn: async () => {
      const response = await dashboardAPI.getWeeklyStatistics()
      return response.data
    },
    staleTime: 1000 * 60 * 10,
    gcTime: 1000 * 60 * 30,
  })
}

export function useRecentActivity(limit?: number) {
  return useQuery({
    queryKey: ['dashboard', 'recent-activity', limit],
    queryFn: async () => {
      const response = await dashboardAPI.getRecentActivity(limit)
      return response.data
    },
    staleTime: 1000 * 60,
    gcTime: 1000 * 60 * 5,
  })
}

export function useDashboardSummary() {
  return useQuery({
    queryKey: ['dashboard', 'summary'],
    queryFn: async () => {
      const response = await dashboardAPI.getSummary()
      return response.data
    },
    staleTime: 1000 * 60 * 2,
    gcTime: 1000 * 60 * 10,
  })
}
