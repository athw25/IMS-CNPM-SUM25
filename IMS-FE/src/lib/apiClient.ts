import { storage } from './storage'

const API_BASE = import.meta.env.VITE_API_BASE || (globalThis as any).__API_BASE__ || 'http://localhost:5000'

type Opts = {
  method?: string
  body?: any
  headers?: Record<string,string>
  retry?: boolean
}

async function raw(path: string, opts: Opts = {}) {
  const url = path.startsWith('http') ? path : `${API_BASE}${path}`
  const headers: Record<string,string> = { 'Content-Type': 'application/json', ...(opts.headers||{}) }
  const { accessToken } = storage.load()
  if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`
  const res = await fetch(url, { method: opts.method || 'GET', headers, body: opts.body ? JSON.stringify(opts.body) : undefined })
  if (res.status === 204) return null
  let data: any = null
  try { data = await res.json() } catch { data = null }
  if (!res.ok) {
    // 401 → thử refresh 1 lần
    if (res.status === 401 && opts.retry !== false) {
      const refreshed = await refreshAccessToken()
      if (refreshed) {
        return raw(path, { ...opts, retry: false })
      }
    }
    const msg = data?.error?.message || `HTTP ${res.status}`
    const err: any = new Error(msg)
    err.code = data?.error?.code || res.status
    err.payload = data
    throw err
  }
  return data
}

async function refreshAccessToken(): Promise<boolean> {
  const { refreshToken } = storage.load()
  if (!refreshToken) return false
  try {
    const res = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${refreshToken}` }
    })
    const data = await res.json()
    if (!res.ok) return false
    if (data?.access_token) {
      storage.setAccess(data.access_token)
      return true
    }
    if (data?.accessToken) { // phòng trường hợp khác casing
      storage.setAccess(data.accessToken)
      return true
    }
    return false
  } catch {
    return false
  }
}

export const api = {
  get: (p: string, q?: Record<string, any>) => {
    const qs = q ? '?' + new URLSearchParams(Object.entries(q).filter(([_,v]) => v!==undefined && v!==null).map(([k,v]) => [k, String(v)])) : ''
    return raw(p + qs, { method: 'GET' })
  },
  post: (p: string, body?: any) => raw(p, { method: 'POST', body }),
  patch: (p: string, body?: any) => raw(p, { method: 'PATCH', body }),
  del: (p: string) => raw(p, { method: 'DELETE' }),
  base: API_BASE
}
