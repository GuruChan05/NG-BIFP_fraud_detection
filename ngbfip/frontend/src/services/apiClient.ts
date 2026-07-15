import api from './api';
import { AxiosPromise } from 'axios';

interface LoginRequest {
  email: string;
  password: string;
}

interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name: string;
}

interface TokenResponse {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
}

export const authService = {
  login: (data: LoginRequest): AxiosPromise<TokenResponse> =>
    api.post('/api/v1/auth/login', data),
  
  register: (data: RegisterRequest): AxiosPromise<any> =>
    api.post('/api/v1/auth/register', data),
  
  logout: (): AxiosPromise<any> =>
    api.post('/api/v1/auth/logout'),
  
  refreshToken: (): AxiosPromise<TokenResponse> =>
    api.post('/api/v1/auth/refresh'),
  
  forgotPassword: (email: string): AxiosPromise<any> =>
    api.post('/api/v1/auth/forgot-password', { email }),
};

export const userService = {
  getCurrentUser: (): AxiosPromise<any> =>
    api.get('/api/v1/users/me'),
  
  getUser: (userId: string): AxiosPromise<any> =>
    api.get(`/api/v1/users/${userId}`),
  
  updateUser: (userId: string, data: any): AxiosPromise<any> =>
    api.put(`/api/v1/users/${userId}`, data),
};

export const transactionService = {
  getTransactions: (skip: number = 0, limit: number = 50): AxiosPromise<any> =>
    api.get('/api/v1/transactions/', { params: { skip, limit } }),
  
  getTransaction: (transactionId: string): AxiosPromise<any> =>
    api.get(`/api/v1/transactions/${transactionId}`),
  
  createTransaction: (data: any): AxiosPromise<any> =>
    api.post('/api/v1/transactions/', data),
  
  getUserTransactions: (userId: string, skip: number = 0, limit: number = 50): AxiosPromise<any> =>
    api.get(`/api/v1/transactions/user/${userId}`, { params: { skip, limit } }),
};

export const riskService = {
  analyzeRisk: (transactionId: string): AxiosPromise<any> =>
    api.post('/api/v1/risk/analyze', { transaction_id: transactionId }),
  
  getRiskTrends: (): AxiosPromise<any> =>
    api.get('/api/v1/risk/trends'),
};

export const alertService = {
  getAlerts: (skip: number = 0, limit: number = 50): AxiosPromise<any> =>
    api.get('/api/v1/alerts/', { params: { skip, limit } }),
  
  getAlert: (alertId: string): AxiosPromise<any> =>
    api.get(`/api/v1/alerts/${alertId}`),
  
  resolveAlert: (alertId: string, status: string, notes?: string): AxiosPromise<any> =>
    api.put(`/api/v1/alerts/${alertId}/resolve`, { status, resolution_notes: notes }),
};

export const deviceService = {
  getDevices: (): AxiosPromise<any> =>
    api.get('/api/v1/devices/'),
  
  getDevice: (deviceId: string): AxiosPromise<any> =>
    api.get(`/api/v1/devices/${deviceId}`),
  
  registerDevice: (data: any): AxiosPromise<any> =>
    api.post('/api/v1/devices/', data),
  
  updateDeviceTrust: (deviceId: string, data: any): AxiosPromise<any> =>
    api.put(`/api/v1/devices/${deviceId}/trust`, data),
};

export const dashboardService = {
  getOverview: (): AxiosPromise<any> =>
    api.get('/api/v1/dashboard/overview'),
  
  getStatistics: (): AxiosPromise<any> =>
    api.get('/api/v1/dashboard/statistics'),
};
