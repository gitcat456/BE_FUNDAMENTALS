import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import type { UserRole } from '../api/types'
import { useAuth } from '../auth/AuthContext'

const roleLabel: Record<UserRole, string> = {
  admin: 'Administrator',
  librarian: 'Librarian',
  member: 'Member',
  customer: 'Customer',
}

const navForRole = (role: UserRole): { to: string; label: string }[] => {
  const base = `/workspace/${role}`
  switch (role) {
    case 'admin':
      return [
        { to: base, label: 'Overview' },
        { to: `${base}/books`, label: 'Books' },
        { to: `${base}/loans`, label: 'Loans' },
      ]
    case 'librarian':
      return [
        { to: base, label: 'Desk' },
        { to: `${base}/books`, label: 'Catalog' },
        { to: `${base}/loans`, label: 'Loans' },
      ]
    case 'member':
      return [
        { to: base, label: 'Home' },
        { to: `${base}/browse`, label: 'Browse' },
        { to: `${base}/loans`, label: 'My loans' },
      ]
    case 'customer':
      return [
        { to: base, label: 'Home' },
        { to: `${base}/browse`, label: 'Catalog' },
        { to: `${base}/loans`, label: 'Activity' },
      ]
    default:
      return [{ to: base, label: 'Home' }]
  }
}

export function WorkspaceShell() {
  const { profile, logout } = useAuth()
  const navigate = useNavigate()

  if (!profile) return null

  const items = navForRole(profile.role)

  return (
    <div className="flex min-h-screen">
      <aside className="flex w-64 flex-col border-r border-[var(--color-border)] bg-[var(--color-surface)]/95 backdrop-blur">
        <div className="border-b border-[var(--color-border)] px-5 py-6">
          <p className="font-display text-lg font-semibold tracking-tight text-[var(--color-ink)]">
            Lib Desk
          </p>
          <p className="mt-1 text-xs text-[var(--color-muted)]">Library control room</p>
        </div>
        <nav className="flex flex-1 flex-col gap-0.5 p-3">
          {items.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === `/workspace/${profile.role}`}
              className={({ isActive }) =>
                [
                  'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-[var(--color-surface-2)] text-[var(--color-accent)]'
                    : 'text-[var(--color-muted)] hover:bg-[var(--color-surface-2)]/60 hover:text-[var(--color-ink)]',
                ].join(' ')
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-[var(--color-border)] p-4">
          <div className="rounded-xl bg-[var(--color-canvas)]/80 p-3">
            <p className="text-sm font-medium text-[var(--color-ink)]">{profile.username}</p>
            <p className="mt-0.5 text-xs text-[var(--color-accent-dim)]">{roleLabel[profile.role]}</p>
            <p className="mt-2 truncate text-xs text-[var(--color-muted)]">{profile.email}</p>
          </div>
          <button
            type="button"
            onClick={async () => {
              await logout()
              navigate('/login', { replace: true })
            }}
            className="mt-3 w-full rounded-lg border border-[var(--color-border)] py-2 text-sm text-[var(--color-muted)] transition hover:border-[var(--color-accent-dim)] hover:text-[var(--color-ink)]"
          >
            Sign out
          </button>
        </div>
      </aside>
      <main className="min-w-0 flex-1 p-8 lg:p-10">
        <Outlet />
      </main>
    </div>
  )
}
