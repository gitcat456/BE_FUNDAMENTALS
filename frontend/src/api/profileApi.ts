import type {
  GeocodeResult,
  NearbyUsersResponse,
  UserProfileDetail,
} from './types'
import { apiFetch, apiJson } from './client'

export type UserProfileUpdatePayload = {
  bio?: string
  location?: string
  country?: string
}

function profileUpdateErrorMessage(text: string): string {
  try {
    const j = JSON.parse(text) as Record<string, string | string[]>
    for (const key of ['location', 'bio', 'error', 'detail']) {
      const val = j[key]
      if (typeof val === 'string') return val
      if (Array.isArray(val) && val[0]) return String(val[0])
    }
  } catch {
    /* ignore */
  }
  return text
}

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

export async function updateUserProfile(
  payload: UserProfileUpdatePayload,
): Promise<UserProfileDetail> {
  const res = await apiFetch('/users/profile/update/', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(profileUpdateErrorMessage(text) || `HTTP ${res.status}`)
  }
  return res.json() as Promise<UserProfileDetail>
}

export async function geocodeAddress(
  address: string,
  country = 'KE',
): Promise<GeocodeResult> {
  const params = new URLSearchParams({ address, country })
  return apiJson<GeocodeResult>(`/maps/geocode/?${params}`)
}

export async function reverseGeocodeAddress(lat: number, lng: number): Promise<string> {
  const params = new URLSearchParams({ lat: String(lat), lng: String(lng) })
  const data = await apiJson<{ address: string }>(`/maps/reverse-geocode/?${params}`)
  return data.address
}

export async function fetchNearbyUsers(
  lat: number,
  lng: number,
  radiusKm = 10,
): Promise<NearbyUsersResponse> {
  const params = new URLSearchParams({
    lat: String(lat),
    lng: String(lng),
    radius: String(radiusKm),
  })
  return apiJson<NearbyUsersResponse>(`/maps/nearby-users/?${params}`)
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
