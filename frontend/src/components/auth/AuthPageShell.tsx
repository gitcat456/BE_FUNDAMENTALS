import { Link } from 'react-router-dom'
import type { ReactNode } from 'react'

type AuthPageShellProps = {
  title: string
  subtitle: ReactNode
  children: ReactNode
  footer?: ReactNode
}

export function AuthPageShell({ title, subtitle, children, footer }: AuthPageShellProps) {
  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center px-4 py-10">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.35]"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c9a227' fill-opacity='0.07'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
        }}
      />
      <div className="relative w-full max-w-md">
        <div className="mb-10 text-center">
          <Link
            to="/login"
            className="font-display text-4xl font-semibold tracking-tight text-[var(--color-ink)] transition hover:text-[var(--color-accent)]"
          >
            Lib Desk
          </Link>
          <h1 className="mt-4 font-display text-2xl font-medium text-[var(--color-ink)]">{title}</h1>
          <p className="mt-3 text-sm leading-relaxed text-[var(--color-muted)]">{subtitle}</p>
        </div>
        <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 p-8 shadow-xl backdrop-blur">
          {children}
        </div>
        {footer ? <div className="mt-6 text-center text-sm text-[var(--color-muted)]">{footer}</div> : null}
      </div>
    </div>
  )
}

export const authInputClass =
  'mt-2 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2.5 text-sm text-[var(--color-ink)] outline-none transition focus:border-[var(--color-accent-dim)]'

export const authLabelClass =
  'block text-xs font-medium uppercase tracking-wide text-[var(--color-muted)]'

export const authSubmitClass =
  'w-full rounded-xl bg-[var(--color-accent)] py-3 text-sm font-semibold text-[var(--color-canvas)] transition hover:brightness-110 disabled:opacity-50'

export const authLinkClass =
  'font-medium text-[var(--color-accent)] transition hover:brightness-125'
