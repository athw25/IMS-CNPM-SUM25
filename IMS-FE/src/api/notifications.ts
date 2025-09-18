import { api } from '../lib/apiClient'
export const notifications = {
  list: (q:{page?:number; limit?:number}) => api.get('/notifications', q),
  create: (payload:any) => api.post('/notifications', payload),
  markRead: (id:number) => api.patch(`/notifications/${id}/read`)
}
