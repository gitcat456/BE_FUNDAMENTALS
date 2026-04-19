import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../../auth/AuthContext'
import { fetchBooks, fetchLoans } from '../../api/libApi'
import { StatCard } from '../../components/StatCard'

export function DashboardHome() {
  const { profile } = useAuth()
  const [bookCount, setBookCount] = useState<number | null>(null)
  const [loanCount, setLoanCount] = useState<number | null>(null)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const [books, loans] = await Promise.all([fetchBooks(), fetchLoans()])
        if (!cancelled) {
          setBookCount(books.length)
          setLoanCount(loans.length)
        }
      } catch (e) {
        if (!cancelled) setErr(e instanceof Error ? e.message : 'Failed to load stats')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [])

  if (!profile) return null

  const base = `/workspace/${profile.role}`

  const hero = {
    admin: {
      title: 'Operations overview',
      body: 'Monitor the full collection and every active loan from one place.',
    },
    librarian: {
      title: 'Circulation desk',
      body: 'Add titles, retire copies, and register loans without touching the terminal.',
    },
    member: {
      title: 'Your member portal',
      body: 'Browse the catalog and track what you have checked out.',
    },
    customer: {
      title: 'Welcome',
      body: 'Explore what is on the shelves and see your borrowing activity.',
    },
  }[profile.role]

  return (
    <div className="max-w-4xl">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-[var(--color-accent-dim)]">
        Dashboard
      </p>
      <h1 className="mt-2 font-display text-3xl font-semibold text-[var(--color-ink)]">
        {hero.title}
      </h1>
      <p className="mt-3 max-w-2xl text-sm leading-relaxed text-[var(--color-muted)]">{hero.body}</p>

      {err ? (
        <p className="mt-6 rounded-lg border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-200">
          {err}
        </p>
      ) : null}

      <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          label="Titles in catalog"
          value={bookCount ?? '—'}
          hint="From GET /api/list/"
        />
        <StatCard
          label={profile.role === 'member' || profile.role === 'customer' ? 'Your loan rows' : 'Loan records'}
          value={loanCount ?? '—'}
          hint={
            profile.role === 'member' || profile.role === 'customer'
              ? 'Filtered for your account on the server'
              : 'Includes all active loans'
          }
        />
        <StatCard
          label="Account role"
          value={profile.role}
          hint="Loaded from GET /api/auth/profile/"
        />
      </div>

      <div className="mt-10 flex flex-wrap gap-3">
        {(profile.role === 'admin' || profile.role === 'librarian') && (
          <>
            <Link
              to={`${base}/books`}
              className="rounded-xl border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-ink)] transition hover:border-[var(--color-accent-dim)]"
            >
              Manage books
            </Link>
            <Link
              to={`${base}/loans`}
              className="rounded-xl bg-[var(--color-accent)] px-4 py-2 text-sm font-semibold text-[var(--color-canvas)] transition hover:brightness-110"
            >
              Open loans
            </Link>
          </>
        )}
        {(profile.role === 'member' || profile.role === 'customer') && (
          <>
            <Link
              to={`${base}/browse`}
              className="rounded-xl bg-[var(--color-accent)] px-4 py-2 text-sm font-semibold text-[var(--color-canvas)] transition hover:brightness-110"
            >
              Browse catalog
            </Link>
            <Link
              to={`${base}/loans`}
              className="rounded-xl border border-[var(--color-border)] px-4 py-2 text-sm font-medium text-[var(--color-ink)] transition hover:border-[var(--color-accent-dim)]"
            >
              View loans
            </Link>
          </>
        )}
      </div>
    </div>
  )
}
