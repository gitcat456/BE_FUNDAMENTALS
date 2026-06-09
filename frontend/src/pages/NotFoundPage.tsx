import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const NOT_FOUND_ICON =
  'https://cdn.prod.website-files.com/69b15b68fb5a0ea0e6ef48b2/69d772b6e341c1183f525617_Icon%20-%20Navigation.png'

export function NotFoundPage() {
  const { profile, loading } = useAuth()

  const homeTo = !loading && profile ? `/workspace/${profile.role}` : '/login'
  const homeLabel = !loading && profile ? 'Back to workspace' : 'Back to sign in'

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center px-4 py-16">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c9a227' fill-opacity='0.07'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />

      <div className="relative w-full max-w-lg text-center">
        <div className="mx-auto mb-8 flex h-28 w-28 items-center justify-center rounded-3xl border border-border bg-surface shadow-[0_0_48px_rgba(56,189,248,0.15)]">
          <img
            src={NOT_FOUND_ICON}
            alt=""
            width={72}
            height={72}
            className="h-[4.5rem] w-[4.5rem] object-contain"
            decoding="async"
          />
        </div>

        <p className="font-display text-7xl font-semibold tracking-tight text-ink">404</p>
        <h1 className="mt-3 font-display text-2xl font-medium text-ink">Page not found</h1>
        <p className="mx-auto mt-4 max-w-sm text-sm leading-relaxed text-muted">
          This route does not exist or may have moved. Check the URL, or head back to a known part of Lib Desk.
        </p>

        <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Link
            to={homeTo}
            className="inline-flex min-w-[10rem] items-center justify-center rounded-xl bg-accent px-6 py-3 text-sm font-semibold text-canvas transition hover:brightness-110"
          >
            {homeLabel}
          </Link>
          <Link
            to="/"
            className="inline-flex min-w-[10rem] items-center justify-center rounded-xl border border-border bg-surface/90 px-6 py-3 text-sm font-medium text-ink transition hover:border-accent-dim"
          >
            Home
          </Link>
        </div>
      </div>
    </div>
  )
}
