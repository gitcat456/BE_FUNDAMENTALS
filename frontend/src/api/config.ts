export const API_BASE = (
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'
).replace(/\/$/, '')

export const STORAGE_ACCESS = 'be_lib_access'
export const STORAGE_REFRESH = 'be_lib_refresh'
