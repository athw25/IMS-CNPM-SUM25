import { api } from '../lib/apiClient'
export const profiles = {
  list: (q:{user_id?:number; status?:string; page?:number; limit?:number}) => api.get('/intern-profiles', q),
  create: (payload:any) => api.post('/intern-profiles', payload),
  get: (id:number) => api.get(`/intern-profiles/${id}`),
  patch: (id:number, payload:any) => api.patch(`/intern-profiles/${id}`, payload),
}
