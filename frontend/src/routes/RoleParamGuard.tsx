import { Navigate, Outlet, useParams } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { normalizeUserRole } from '../utils/role'

/**
 * Ensures the URL segment `/workspace/:role` matches the role returned by the API.
 * Never trust client-side role selection — the backend is the source of truth.
 */
export function RoleParamGuard() {
  const { role: roleParam } = useParams()
  const { profile, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-muted">
        Loading…
      </div>
    )
  }

  if (!profile) {
    return <Navigate to="/login" replace />
  }

  const urlRole = normalizeUserRole(roleParam)
  const userRole = normalizeUserRole(profile.role)

  if (!urlRole || !userRole || urlRole !== userRole) {
    return <Navigate to={`/workspace/${userRole ?? 'member'}`} replace />
  }

  return <Outlet />
}
