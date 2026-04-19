import { API_BASE, STORAGE_ACCESS, STORAGE_REFRESH } from './config'

function getAccess(): string | null {
  return localStorage.getItem(STORAGE_ACCESS)
}

function getRefresh(): string | null {
  return localStorage.getItem(STORAGE_REFRESH)
}

export function setTokens(access: string, refresh: string) {
  localStorage.setItem(STORAGE_ACCESS, access)
  localStorage.setItem(STORAGE_REFRESH, refresh)
}

export function clearTokens() {
  localStorage.removeItem(STORAGE_ACCESS)
  localStorage.removeItem(STORAGE_REFRESH)
}

async function rotateRefresh(): Promise<string | null> {
  const refresh = getRefresh()
  if (!refresh) return null
  const res = await fetch(`${API_BASE}/auth/jwt-refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })
  if (!res.ok) {
    clearTokens()
    return null
  }
  const data: { access: string; refresh: string } = await res.json()
  setTokens(data.access, data.refresh)
  return data.access
}

/**
 * Authenticated JSON fetch. Retries once after refresh on 401.
 */
export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const url = path.startsWith('http') ? path : `${API_BASE}${path.startsWith('/') ? '' : '/'}${path}`
  const headers = new Headers(init.headers)
  const access = getAccess()
  if (access && !headers.has('Authorization')) {
    headers.set('Authorization', `Bearer ${access}`)
  }
  let res = await fetch(url, { ...init, headers })
  if (res.status === 401 && !path.includes('jwt-refresh')) {
    const newAccess = await rotateRefresh()
    if (newAccess) {
      headers.set('Authorization', `Bearer ${newAccess}`)
      res = await fetch(url, { ...init, headers })
    }
  }
  return res
}

export async function apiJson<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await apiFetch(path, init)
  if (!res.ok) {
    const text = await res.text()
    let detail = text
    try {
      const j = JSON.parse(text) as { error?: string; message?: string; detail?: string }
      detail = j.error ?? j.message ?? j.detail ?? text
    } catch {
      /* ignore */
    }
    throw new Error(detail || `HTTP ${res.status}`)
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}
