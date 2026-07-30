export function setAuthToken(token: string): void {
  localStorage.setItem('auth_token', token)
}

export function getAuthToken(): string | null {
  return localStorage.getItem('auth_token')
}

export function setRefreshToken(token: string): void {
  localStorage.setItem('refresh_token', token)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem('refresh_token')
}

export function clearAuthTokens(): void {
  localStorage.removeItem('auth_token')
  localStorage.removeItem('refresh_token')
}

export function setUserData(userData: any): void {
  localStorage.setItem('user_data', JSON.stringify(userData))
}

export function getUserData(): any {
  const data = localStorage.getItem('user_data')
  return data ? JSON.parse(data) : null
}

export function clearAuthData(): void {
  clearAuthTokens()
  localStorage.removeItem('user_data')
}
