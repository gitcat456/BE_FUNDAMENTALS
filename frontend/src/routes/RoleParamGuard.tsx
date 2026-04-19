import { Navigate, useParams } from 'react-router-dom'
import type { ReactNode } from 'react'
import type { UserRole } from '../api/types'
import { useAuth } from '../auth/AuthContext'

/**
 * Ensures the URL segment `/workspace/:role` matches the role returned by the API.
 * Never trust client-side role selection — the backend is the source of truth.
 */
export function RoleParamGuard({ children }: { children: ReactNode }) {
  const { role } = useParams()
  const { profile, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-[var(--color-muted)]">
        Loading…
      </div>
    )
  }

  if (!profile) {
    return <Navigate to="/login" replace />
  }

  const roles: UserRole[] = ['admin', 'librarian', 'member', 'customer']
  if (!role || !roles.includes(role as UserRole) || role !== profile.role) {
    return <Navigate to={`/workspace/${profile.role}`} replace />
  }

  return <>{children}</>
}
