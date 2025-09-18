import { api } from '../lib/apiClient'

export const auth = {
  login: (email:string, password:string) => api.post('/auth/login', { email, password }),
  register: (payload: any) => api.post('/auth/register', payload),
  me: () => api.get('/me'),
  refresh: () => api.post('/auth/refresh')
}
