import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { setAuthToken, getAuthToken, setRefreshToken, getRefreshToken, clearAuthData } from '@/lib/auth'

interface User {
  id: number
  email: string
  username: string
  full_name: string
  is_admin: boolean
  is_active: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  setToken: (token: string) => void
  setRefreshToken: (token: string) => void
  updateUser: (user: Partial<User>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: getAuthToken(),
      refreshToken: getRefreshToken(),
      isAuthenticated: !!getAuthToken(),
      login: async (email: string, password: string) => {
        // Will be implemented with API call
        console.log('Login:', email, password)
      },
      logout: () => {
        clearAuthData()
        set({ user: null, token: null, refreshToken: null, isAuthenticated: false })
      },
      setUser: (user: User) => {
        set({ user, isAuthenticated: true })
      },
      setToken: (token: string) => {
        setAuthToken(token)
        set({ token, isAuthenticated: true })
      },
      setRefreshToken: (token: string) => {
        setRefreshToken(token)
        set({ refreshToken: token })
      },
      updateUser: (user: Partial<User>) => {
        set((state) => ({
          user: state.user ? { ...state.user, ...user } : null,
        }))
      },
    }),
    {
      name: 'auth-store',
    }
  )
)
