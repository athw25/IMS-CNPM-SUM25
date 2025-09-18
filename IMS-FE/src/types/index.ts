export type Role = 'Admin'|'HR'|'Coordinator'|'Mentor'|'Intern'

export type User = {
  id: number
  email: string
  name: string
  role: Role
  department?: string
  location?: string
  headline?: string
  avatar_url?: string
  created_at?: string
}

export type Pagination<T> = { items: T[]; page: number; limit: number; total: number }

export type Campaign = { id:number; title:string; status:'Open'|'Closed'; description?:string; created_by:number; created_at:string }
export type Application = { id:number; camp_id:number; user_id:number; status:'Pending'|'Approved'|'Rejected'; note?:string; created_at:string }
export type TrainingProgram = { id:number; title:string; goal?:string; created_by:number }
export type Project = { id:number; prog_id:number; title:string; description?:string; owner_id:number }
export type Assignment = { id:number; proj_id:number; intern_id:number; status:'Pending'|'Doing'|'Done'; due_date?:string|null }
export type Evaluation = { id:number; intern_id:number; evaluator_id:number; score:number; comment?:string; created_at:string }
export type ScheduleItem = { id:number; intern_id:number; title:string; type:'Interview'|'Onboarding'|'Training'|'Work'; start_time:string; end_time:string; location?:string }
export type KPIRecord = { id:number; intern_id:number; kpi_key:string; value:number; period:string; note?:string }
export type Notification = { id:number; user_id:number; type:string; payload:any; is_read:boolean; created_at:string }
export type Thread = { id:number; user_a_id:number; user_b_id:number; created_at:string }
export type Message = { id:number; thread_id:number; sender_id:number; content:string; created_at:string }
