import { api } from '../lib/apiClient'
export const applications = {
  list: (q:{camp_id?:number; status?:string; page?:number; limit?:number}) => api.get('/applications', q),
  create: (payload:any) => api.post('/applications', payload),
  patch: (id:number, payload:any) => api.patch(`/applications/${id}`, payload),
}
