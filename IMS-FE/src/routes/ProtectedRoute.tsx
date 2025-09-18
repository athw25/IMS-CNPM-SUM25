import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { hasRole } from '../lib/auth'
import type { Role } from '../lib/auth'

export default function ProtectedRoute({ children, roles }: { children: React.ReactNode; roles?: Role[] }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="p-6">Đang tải...</div>
  if (!user) return <Navigate to="/login" replace />
  if (!hasRole(user, roles)) return <div className="p-6">Bạn không có quyền truy cập.</div>
  return <>{children}</>
}
