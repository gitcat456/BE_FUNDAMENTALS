import { API_BASE } from './config'

type ApiErrorBody = {
  error?: string
  message?: string
  detail?: string
  password?: string[]
}

async function parseError(res: Response): Promise<string> {
  const text = await res.text()
  try {
    const body = JSON.parse(text) as ApiErrorBody
    if (body.password?.length) return body.password.join(' ')
    return body.error ?? body.message ?? body.detail ?? text
  } catch {
    return text || `Request failed (${res.status})`
  }
}

export type RegisterPayload = {
  username: string
  email: string
  password: string
}

export type RegisterResponse = {
  id: number
  username: string
  email: string
}

export async function register(payload: RegisterPayload): Promise<RegisterResponse> {
  const res = await fetch(`${API_BASE}/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json() as Promise<RegisterResponse>
}

export async function forgotPassword(email: string): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/auth/forgot-password/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json() as Promise<{ message: string }>
}

export async function resetPassword(token: string, password: string): Promise<{ message: string }> {
  const res = await fetch(`${API_BASE}/auth/reset-password/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token, password }),
  })
  if (!res.ok) throw new Error(await parseError(res))
  return res.json() as Promise<{ message: string }>
}

export type GoogleLoginResponse = {
  accessToken: string
  refreshToken: string
  username: string
  email: string
  photo_url: string | null
  is_new_user: boolean
}

export async function googleLogin(idToken: string): Promise<GoogleLoginResponse> {
  const res = await fetch(`${API_BASE}/auth/google/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: idToken }),
  })
  if (!res.ok) throw new Error(await parseError(res))

  const data = (await res.json()) as {
    accessToken?: string
    access_token?: string
    refreshToken?: string
    refresh_token?: string
    username: string
    email: string
    photo_url?: string | null
    is_new_user?: boolean
  }

  const accessToken = data.accessToken ?? data.access_token
  const refreshToken = data.refreshToken ?? data.refresh_token

  if (!accessToken || !refreshToken) {
    throw new Error('Invalid response from server')
  }

  return {
    accessToken,
    refreshToken,
    username: data.username,
    email: data.email,
    photo_url: data.photo_url ?? null,
    is_new_user: Boolean(data.is_new_user),
  }
}
