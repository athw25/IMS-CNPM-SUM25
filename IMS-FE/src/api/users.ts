import { api } from '../lib/apiClient'
export const users = {
  list: (q:{role?:string; page?:number; limit?:number}) => api.get('/users', q),
  create: (payload:any) => api.post('/users', payload),
  get: (id:number) => api.get(`/users/${id}`)
}
