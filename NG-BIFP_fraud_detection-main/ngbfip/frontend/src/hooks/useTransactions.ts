import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { transactionAPI } from '@/lib/api'

export function useTransactions(page = 1, pageSize = 20, filters?: any) {
  return useQuery({
    queryKey: ['transactions', page, pageSize, filters],
    queryFn: async () => {
      const response = await transactionAPI.list(page, pageSize, filters)
      return response.data
    },
    staleTime: 1000 * 60 * 2,
    gcTime: 1000 * 60 * 5,
  })
}

export function useTransaction(id: number) {
  return useQuery({
    queryKey: ['transaction', id],
    queryFn: async () => {
      const response = await transactionAPI.get(id)
      return response.data
    },
  })
}

export function useCreateTransaction() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: any) => transactionAPI.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
    },
  })
}

export function useUpdateTransaction() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) =>
      transactionAPI.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
    },
  })
}

export function useDeleteTransaction() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => transactionAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
    },
  })
}

export function useSearchTransactions(query: string) {
  return useQuery({
    queryKey: ['transactions', 'search', query],
    queryFn: async () => {
      const response = await transactionAPI.search(query)
      return response.data
    },
    enabled: query.length > 0,
  })
}

export function useTransactionHistory(userId: number) {
  return useQuery({
    queryKey: ['transactions', 'history', userId],
    queryFn: async () => {
      const response = await transactionAPI.getHistory(userId)
      return response.data
    },
  })
}

export function useTransactionStats() {
  return useQuery({
    queryKey: ['transactions', 'stats'],
    queryFn: async () => {
      const response = await transactionAPI.getStats()
      return response.data
    },
    staleTime: 1000 * 60 * 5,
  })
}
