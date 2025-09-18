import { api } from '../lib/apiClient'
export const evaluations = {
  list: (q:{intern_id?:number; page?:number; limit?:number}) => api.get('/evaluations', q),
  create: (payload:any) => api.post('/evaluations', payload),
  avgScore: (internId:number) => api.get(`/interns/${internId}/avg-score`)
}
