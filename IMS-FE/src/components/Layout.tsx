import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Role } from '../lib/auth'
import { clsx } from 'clsx'

const MenuByRole: Record<Role, {label:string, to:string}[]> = {
  Admin: [
    { label: 'Bảng điều khiển', to: '/dashboard/admin' },
    { label: 'Người dùng', to: '/entities/users' },
    { label: 'Health', to: '/dashboard/admin/health' },
    { label: "Cấu hình & bảo trì", to: "/dashboard/admin/settings" }, 

  ],
  HR: [
    { label: 'Bảng điều khiển', to: '/dashboard/hr' },
    { label: 'Chiến dịch', to: '/entities/campaigns' },
    { label: 'Đơn ứng tuyển', to: '/entities/applications' },
    { label: 'Hồ sơ Thực tập sinh', to: '/entities/profiles' },
    { label: 'Thông báo', to: '/entities/notifications' },
  ],
  Coordinator: [
    { label: 'Bảng điều khiển', to: '/dashboard/coord' },
    { label: 'Chương trình', to: '/entities/programs' },
    { label: 'Dự án', to: '/entities/projects' },
    { label: 'Nhiệm vụ', to: '/entities/assignments' },
    { label: 'KPI', to: '/entities/kpi' },
    { label: 'Lịch', to: '/entities/schedule' },
  ],
  Mentor: [
    { label: 'Bảng điều khiển', to: '/dashboard/mentor' },
    { label: 'Dự án', to: '/entities/projects' },
    { label: 'Nhiệm vụ', to: '/entities/assignments' },
    { label: 'Đánh giá', to: '/entities/evaluations' },
    { label: 'Chat', to: '/entities/chat' },
  ],
  Intern: [
    { label: 'Bảng điều khiển', to: '/dashboard/intern' },
    { label: 'Nhiệm vụ', to: '/entities/assignments' },
    { label: 'Lịch', to: '/entities/schedule' },
    { label: 'KPI', to: '/entities/kpi' },
    { label: 'Thông báo', to: '/entities/notifications' },
    { label: 'Chat', to: '/entities/chat' },
  ]
}

export default function Layout() {
  const { user, logout } = useAuth()
  const nav = useNavigate()

  return (
    <div className="min-h-dvh text-gray-900 dark:text-gray-100 bg-gray-50 dark:bg-gray-950">
      <header className="sticky top-0 z-40 border-b border-gray-200 dark:border-gray-800 bg-blue-400 dark:bg-blue-900 text-white">
        <div className="container flex items-center justify-between py-2">
          <div className="font-bold">Intern Management System</div>
          <div className="text-sm">
            {user ? (
              <div className="flex items-center gap-3">
                <span>{user.name} • {user.role}</span>
                <button className="btn" onClick={() => logout()}>Đăng xuất</button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <button className="btn" onClick={() => nav('/login')}>Đăng nhập</button>
                <button className="btn" onClick={() => nav('/register')}>Đăng ký</button>
              </div>
            )}
          </div>
        </div>
      </header>

      <div className="container grid grid-cols-12 gap-4 py-6">
        <aside className="col-span-12 md:col-span-3 lg:col-span-2">
          <nav className="card p-3">
            {user ? (
              <ul className="space-y-1">
                {MenuByRole[user.role].map(m => (
                  <li key={m.to}>
                    <NavLink to={m.to} className={({isActive}) => clsx('sidebar-link', isActive && 'sidebar-active')}>{m.label}</NavLink>
                  </li>
                ))}
                <li className="mt-2 border-t border-gray-200 dark:border-gray-800 pt-2 text-xs text-gray-500">
                  API: {import.meta.env.VITE_API_BASE}
                </li>
              </ul>
            ) : (
              <p className="text-sm text-gray-500">Vui lòng đăng nhập để xem menu.</p>
            )}
          </nav>
        </aside>
        <main className="col-span-12 md:col-span-9 lg:col-span-10">
          <Outlet />
        </main>
      </div>
      <footer className="py-6 text-center text-xs text-gray-500">{new Date().getFullYear()} © IMS</footer>
    </div>
  )
}
