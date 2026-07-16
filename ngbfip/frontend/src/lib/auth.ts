const TOKEN_KEY = 'auth_token'
const USER_KEY = 'user_info'

export function setAuthToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getAuthToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function removeAuthToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function isAuthenticated(): boolean {
  return getAuthToken() !== null
}

export function setUserInfo(user: any): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

export function getUserInfo(): any {
  const user = localStorage.getItem(USER_KEY)
  return user ? JSON.parse(user) : null
}

export function clearAuth(): void {
  removeAuthToken()
  localStorage.removeItem(USER_KEY)
}
