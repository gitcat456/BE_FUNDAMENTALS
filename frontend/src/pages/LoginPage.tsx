import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export function LoginPage() {
  const { login, profile, loading } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [pending, setPending] = useState(false)

  if (!loading && profile) {
    return <Navigate to={`/workspace/${profile.role}`} replace />
  }

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center px-4">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c9a227' fill-opacity='0.07'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />
      <div className="relative w-full max-w-md">
        <div className="mb-10 text-center">
          <h1 className="font-display text-4xl font-semibold tracking-tight text-[var(--color-ink)]">
            Lib Desk
          </h1>
          <p className="mt-3 text-sm leading-relaxed text-[var(--color-muted)]">
            Sign in with your library account. Your dashboard is chosen automatically from your
            account role — not from this screen.
          </p>
        </div>
        <form
          onSubmit={async (e) => {
            e.preventDefault()
            setError(null)
            setPending(true)
            try {
              const p = await login(username.trim(), password)
              navigate(`/workspace/${p.role}`, { replace: true })
            } catch (err) {
              setError(err instanceof Error ? err.message : 'Login failed')
            } finally {
              setPending(false)
            }
          }}
          className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 p-8 shadow-xl backdrop-blur"
        >
          <label className="block text-xs font-medium uppercase tracking-wide text-[var(--color-muted)]">
            Username
            <input
              className="mt-2 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2.5 text-sm text-[var(--color-ink)] outline-none ring-0 transition focus:border-[var(--color-accent-dim)]"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              required
            />
          </label>
          <label className="mt-5 block text-xs font-medium uppercase tracking-wide text-[var(--color-muted)]">
            Password
            <input
              type="password"
              className="mt-2 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2.5 text-sm text-[var(--color-ink)] outline-none transition focus:border-[var(--color-accent-dim)]"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </label>
          {error ? (
            <p className="mt-4 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-300">
              {error}
            </p>
          ) : null}
          <button
            type="submit"
            disabled={pending}
            className="mt-6 w-full rounded-xl bg-[var(--color-accent)] py-3 text-sm font-semibold text-[var(--color-canvas)] transition hover:brightness-110 disabled:opacity-50"
          >
            {pending ? 'Signing in…' : 'Continue'}
          </button>
        </form>
      </div>
    </div>
  )
}
