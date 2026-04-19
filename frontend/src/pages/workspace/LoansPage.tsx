import { useCallback, useEffect, useState } from 'react'
import { useAuth } from '../../auth/AuthContext'
import { createLoan, fetchLoans } from '../../api/libApi'
import type { LoanRow } from '../../api/types'
import { LoansTable } from '../../components/LoansTable'

export function LoansPage() {
  const { profile } = useAuth()
  const [loans, setLoans] = useState<LoanRow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [loanForm, setLoanForm] = useState({
    borrower_email: '',
    due_date: '',
    book_isbns: '',
  })

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setLoans(await fetchLoans())
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load loans')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void load()
  }, [load])

  if (!profile) return null

  const showBorrower = profile.role === 'admin' || profile.role === 'librarian'
  const canCreateLoan = profile.role === 'admin' || profile.role === 'librarian'

  async function onCreateLoan(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    const isbns = loanForm.book_isbns
      .split(/[\s,]+/)
      .map((s) => s.trim())
      .filter(Boolean)
    try {
      await createLoan({
        borrower_email: loanForm.borrower_email.trim(),
        due_date: loanForm.due_date,
        book_isbns: isbns,
      })
      setLoanForm({ borrower_email: '', due_date: '', book_isbns: '' })
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not create loan')
    }
  }

  return (
    <div className="max-w-5xl">
      <h1 className="font-display text-2xl font-semibold text-[var(--color-ink)]">
        {profile.role === 'member' || profile.role === 'customer' ? 'Loans' : 'Loan register'}
      </h1>
      <p className="mt-2 text-sm text-[var(--color-muted)]">
        Data from <code className="text-[var(--color-accent)]">GET /api/loan-list/</code>
        {canCreateLoan ? (
          <>
            {' '}
            and new loans via <code className="text-[var(--color-accent)]">POST /api/loans/</code>
          </>
        ) : (
          <>
            . The API only returns loans for your user when you are not staff.
          </>
        )}
      </p>

      {canCreateLoan ? (
        <form
          onSubmit={onCreateLoan}
          className="mt-8 rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/80 p-6"
        >
          <p className="text-sm font-medium text-[var(--color-ink)]">Register a loan</p>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <label className="text-xs uppercase text-[var(--color-muted)] sm:col-span-2">
              Borrower email (must match a user in the database)
              <input
                required
                type="email"
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm"
                value={loanForm.borrower_email}
                onChange={(e) => setLoanForm((f) => ({ ...f, borrower_email: e.target.value }))}
              />
            </label>
            <label className="text-xs uppercase text-[var(--color-muted)]">
              Due date
              <input
                required
                type="date"
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm"
                value={loanForm.due_date}
                onChange={(e) => setLoanForm((f) => ({ ...f, due_date: e.target.value }))}
              />
            </label>
            <label className="text-xs uppercase text-[var(--color-muted)] sm:col-span-2">
              Book ISBNs (comma or space separated)
              <input
                required
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm font-mono"
                placeholder="9780000000000, 9781111111111"
                value={loanForm.book_isbns}
                onChange={(e) => setLoanForm((f) => ({ ...f, book_isbns: e.target.value }))}
              />
            </label>
          </div>
          <button
            type="submit"
            className="mt-4 rounded-xl bg-[var(--color-accent)] px-4 py-2 text-sm font-semibold text-[var(--color-canvas)] hover:brightness-110"
          >
            Create loan
          </button>
        </form>
      ) : null}

      {error ? (
        <p className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </p>
      ) : null}

      <div className="mt-8">
        {loading ? (
          <p className="text-sm text-[var(--color-muted)]">Loading loans…</p>
        ) : (
          <LoansTable loans={loans} showBorrower={showBorrower} />
        )}
      </div>
    </div>
  )
}
