import { api } from '../lib/apiClient'
export const chat = {
  start: (user_id:number) => api.post('/threads/start', { user_id }),
  listThreads: (q:{page?:number; limit?:number}) => api.get('/threads', q),
  listMessages: (tid:number, q:{page?:number; limit?:number}) => api.get(`/threads/${tid}/messages`, q),
  postMessage: (tid:number, payload:any) => api.post(`/threads/${tid}/messages`, payload),
}
