export type Role = 'Admin'|'HR'|'Coordinator'|'Mentor'|'Intern'

export const hasRole = (user: any, roles?: Role[]) => {
  if (!roles || roles.length === 0) return true
  const r = user?.role as Role | undefined
  return !!r && roles.includes(r)
}
