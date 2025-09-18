import { api } from '../lib/apiClient'
export const assignments = {
  list: (q:{proj_id?:string|number; intern_id?:string|number; status?:string; page?:number; limit?:number}) => api.get('/assignments', q),
  create: (payload:any) => api.post('/assignments', payload),
  updateStatus: (id:number, status:'Doing'|'Done') => api.patch(`/assignments/${id}/status`, { status }),
  remove: (id:number) => api.del(`/assignments/${id}`)
}
