import type { LoanRow } from '../api/types'

type Props = {
  loans: LoanRow[]
  showBorrower?: boolean
}

export function LoansTable({ loans, showBorrower = true }: Props) {
  return (
    <div className="overflow-x-auto rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]">
      <table className="w-full min-w-[640px] text-left text-sm">
        <thead>
          <tr className="border-b border-[var(--color-border)] text-[var(--color-muted)]">
            <th className="px-4 py-3 font-medium">ID</th>
            {showBorrower ? <th className="px-4 py-3 font-medium">Borrower</th> : null}
            <th className="px-4 py-3 font-medium">Borrowed</th>
            <th className="px-4 py-3 font-medium">Due</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Books</th>
          </tr>
        </thead>
        <tbody>
          {loans.length === 0 ? (
            <tr>
              <td
                colSpan={showBorrower ? 6 : 5}
                className="px-4 py-8 text-center text-[var(--color-muted)]"
              >
                No loans to show.
              </td>
            </tr>
          ) : (
            loans.map((L) => (
              <tr
                key={L.id}
                className="border-b border-[var(--color-border)]/60 last:border-0 hover:bg-[var(--color-surface-2)]/80"
              >
                <td className="px-4 py-3 font-mono text-xs text-[var(--color-muted)]">{L.id}</td>
                {showBorrower ? (
                  <td className="px-4 py-3 text-[var(--color-ink)]">{L.borrower_name}</td>
                ) : null}
                <td className="px-4 py-3 text-[var(--color-muted)]">
                  {new Date(L.borrowed_date).toLocaleString()}
                </td>
                <td className="px-4 py-3 text-[var(--color-muted)]">{L.due_date}</td>
                <td className="px-4 py-3 capitalize">{L.status}</td>
                <td className="px-4 py-3">{L.total_books}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
