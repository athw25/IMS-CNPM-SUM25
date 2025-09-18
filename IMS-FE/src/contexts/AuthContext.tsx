import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../lib/apiClient'
import { storage } from '../lib/storage'
import { useNavigate } from 'react-router-dom'
import type { Role } from '../lib/auth'

type User = { id:number; email:string; name:string; role:Role; intern_profile?: any }

type AuthState = {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  loading: boolean
  login: (email:string, password:string) => Promise<void>
  register: (name:string, email:string, password:string, role?:Role) => Promise<void>
  logout: () => void
}

const Ctx = createContext<AuthState>(null as any)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [refreshToken, setRefreshToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const nav = useNavigate()

  useEffect(() => {
    const s = storage.load()
    setAccessToken(s.accessToken)
    setRefreshToken(s.refreshToken)
    setUser(s.user)
    setLoading(false)
  }, [])

  async function login(email:string, password:string) {
    const data = await api.post('/auth/login', { email, password })
    const { access_token, refresh_token, user } = data
    setAccessToken(access_token); setRefreshToken(refresh_token); setUser(user)
    storage.save(access_token, refresh_token, user)
    // điều hướng theo role
    gotoRoleHome(user.role)
  }

  async function register(name:string, email:string, password:string, role:Role='Intern') {
    await api.post('/auth/register', { name, email, password, role })
    // auto login
    await login(email, password)
  }

  function logout() {
    storage.clear()
    setUser(null); setAccessToken(null); setRefreshToken(null)
    nav('/login')
  }

  function gotoRoleHome(role: Role) {
    const map: Record<Role,string> = {
      Admin: '/dashboard/admin',
      HR: '/dashboard/hr',
      Coordinator: '/dashboard/coord',
      Mentor: '/dashboard/mentor',
      Intern: '/dashboard/intern',
    }
    nav(map[role] || '/')
  }

  const value = useMemo(() => ({ user, accessToken, refreshToken, loading, login, register, logout }), [user, accessToken, refreshToken, loading])

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}

export const useAuth = () => useContext(Ctx)
