import { api } from '../lib/apiClient'
export const programs = {
  list: (q:{page?:number; limit?:number}) => api.get('/training-programs', q),
  create: (payload:any) => api.post('/training-programs', payload),
  remove: (id:number) => api.del(`/training-programs/${id}`)
}
