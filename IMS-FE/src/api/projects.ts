import { api } from '../lib/apiClient'
export const projects = {
  list: (q:{prog_id?:string|number; page?:number; limit?:number}) => api.get('/projects', q),
  create: (payload:any) => api.post('/projects', payload),
  remove: (id:number) => api.del(`/projects/${id}`)
}
