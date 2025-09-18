import { api } from '../lib/apiClient'
export const schedule = {
  list: (q:{intern_id?:number|string; from?:string; to?:string; page?:number; limit?:number}) => api.get('/schedule', q),
  create: (payload:any) => api.post('/schedule', payload),
  patch: (id:number, payload:any) => api.patch(`/schedule/${id}`, payload),
  remove: (id:number) => api.del(`/schedule/${id}`)
}
