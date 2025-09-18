export type StoredAuth = {
  accessToken: string | null
  refreshToken: string | null
  user: any | null
}
const K = {
  access: 'ims.access_token',
  refresh: 'ims.refresh_token',
  user: 'ims.user'
} as const

export const storage = {
  load(): StoredAuth {
    return {
      accessToken: localStorage.getItem(K.access),
      refreshToken: localStorage.getItem(K.refresh),
      user: (() => {
        const s = localStorage.getItem(K.user)
        if (!s) return null
        try { return JSON.parse(s) } catch { return null }
      })()
    }
  },
  save(accessToken: string, refreshToken: string, user: any) {
    localStorage.setItem(K.access, accessToken)
    localStorage.setItem(K.refresh, refreshToken)
    localStorage.setItem(K.user, JSON.stringify(user))
  },
  setAccess(access: string) { localStorage.setItem(K.access, access) },
  clear() {
    localStorage.removeItem(K.access)
    localStorage.removeItem(K.refresh)
    localStorage.removeItem(K.user)
  },
  keys: K
}
