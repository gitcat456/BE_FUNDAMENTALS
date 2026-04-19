import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import type { Profile } from '../api/types'
import { API_BASE, STORAGE_ACCESS } from '../api/config'
import { apiFetch, apiJson, clearTokens, setTokens } from '../api/client'

type AuthState = {
  profile: Profile | null
  loading: boolean
  error: string | null
  login: (username: string, password: string) => Promise<Profile>
  logout: () => Promise<void>
  refreshProfile: () => Promise<void>
}

const AuthContext = createContext<AuthState | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [profile, setProfile] = useState<Profile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshProfile = useCallback(async () => {
    const hasToken = localStorage.getItem(STORAGE_ACCESS)
    if (!hasToken) {
      setProfile(null)
      setLoading(false)
      return
    }
    try {
      const p = await apiJson<Profile>('/auth/profile/')
      setProfile(p)
      setError(null)
    } catch {
      setProfile(null)
      clearTokens()
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void refreshProfile()
  }, [refreshProfile])

  const login = useCallback(async (username: string, password: string) => {
    setError(null)
    const res = await fetch(`${API_BASE}/auth/jwt-login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    const data = (await res.json()) as {
      accessToken?: string
      refreshToken?: string
      message?: string
      error?: string
    }
    if (!res.ok) {
      throw new Error(data.message ?? data.error ?? 'Login failed')
    }
    if (!data.accessToken || !data.refreshToken) {
      throw new Error('Invalid response from server')
    }
    setTokens(data.accessToken, data.refreshToken)
    const p = await apiJson<Profile>('/auth/profile/')
    setProfile(p)
    return p
  }, [])

  const logout = useCallback(async () => {
    try {
      await apiFetch('/auth/jwt-logout/', { method: 'POST' })
    } catch {
      /* still clear locally */
    }
    clearTokens()
    setProfile(null)
  }, [])

  const value = useMemo(
    () => ({
      profile,
      loading,
      error,
      login,
      logout,
      refreshProfile,
    }),
    [profile, loading, error, login, logout, refreshProfile],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
