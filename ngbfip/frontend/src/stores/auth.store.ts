import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: string
  email: string
  role: string
  name?: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  setUser: (user: User) => void
  setToken: (token: string) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: async (email: string, password: string) => {
        // Will be implemented with API call
        console.log('Login:', email, password)
      },
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false })
      },
      setUser: (user: User) => {
        set({ user, isAuthenticated: true })
      },
      setToken: (token: string) => {
        set({ token })
      },
    }),
    {
      name: 'auth-store',
    }
  )
)
