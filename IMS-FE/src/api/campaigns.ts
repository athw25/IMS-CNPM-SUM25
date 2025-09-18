import { api } from '../lib/apiClient'
export const campaigns = {
  list: (q:{status?:string; page?:number; limit?:number}) => api.get('/campaigns', q),
  create: (payload:any) => api.post('/campaigns', payload),
  patch: (id:number, payload:any) => api.patch(`/campaigns/${id}`, payload),
  remove: (id:number) => api.del(`/campaigns/${id}`)
}
