import type { UserRole } from '../api/types'

const ROLES: UserRole[] = ['admin', 'librarian', 'member', 'customer']

/** Normalize API role strings so nav/routing switches stay reliable. */
export function normalizeUserRole(role: string | undefined | null): UserRole | null {
  const value = (role ?? '').trim().toLowerCase()
  return ROLES.includes(value as UserRole) ? (value as UserRole) : null
}

export function canUsePayments(role: UserRole | null): boolean {
  return role === 'admin' || role === 'member' || role === 'customer'
}
