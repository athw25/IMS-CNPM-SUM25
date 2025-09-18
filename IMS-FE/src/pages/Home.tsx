import { useAuth } from '../contexts/AuthContext'
import { Link } from 'react-router-dom'

export default function Home() {
  const { user } = useAuth()
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Chào mừng đến IMS</h1>
      <p className="text-gray-600 dark:text-gray-400">Hệ thống quản lý Thực tập sinh cho Doanh nghiệp.</p>
      {user ? (
        <p>Chào <b>{user.name}</b> • Vai trò: <b>{user.role}</b></p>
      ) : (
        <div className="flex gap-2">
          <Link to="/login" className="btn btn-primary">Đăng nhập</Link>
          <Link to="/register" className="btn">Đăng ký</Link>
        </div>
      )}
    </div>
  )
}
