import type { UserProfileDetail } from './types'
import { apiFetch, apiJson } from './client'

const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_PHOTO_BYTES = 5 * 1024 * 1024

export function validateProfilePhoto(file: File): string | null {
  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
    return 'Only JPEG, PNG, or WEBP images are allowed.'
  }
  if (file.size > MAX_PHOTO_BYTES) {
    return 'Image must be 5MB or smaller.'
  }
  return null
}

export async function fetchUserProfile(): Promise<UserProfileDetail> {
  return apiJson<UserProfileDetail>('/users/profile/')
}

export async function updateUserProfile(bio: string): Promise<UserProfileDetail> {
  return apiJson<UserProfileDetail>('/users/profile/update/', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bio }),
  })
}

export async function uploadProfilePhoto(file: File): Promise<{ photo_url: string }> {
  const validationError = validateProfilePhoto(file)
  if (validationError) throw new Error(validationError)

  const form = new FormData()
  form.append('photo', file)

  const res = await apiFetch('/users/profile/photo/', {
    method: 'POST',
    body: form,
  })
  if (!res.ok) {
    const text = await res.text()
    let detail = text
    try {
      const j = JSON.parse(text) as { error?: string }
      detail = j.error ?? text
    } catch {
      /* ignore */
    }
    throw new Error(detail || `HTTP ${res.status}`)
  }
  return res.json() as Promise<{ photo_url: string }>
}
