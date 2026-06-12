import type { LoanStatus } from '../api/types'

const labels: Record<LoanStatus, string> = {
  pending_payment: 'Pending payment',
  borrowed: 'Borrowed',
  returned: 'Returned',
  cancelled: 'Cancelled',
}

const styles: Record<LoanStatus, string> = {
  pending_payment: 'border-warn/40 bg-warn/10 text-warn',
  borrowed: 'border-ok/40 bg-ok/10 text-ok',
  returned: 'border-border bg-surface-2 text-muted',
  cancelled: 'border-red-500/30 bg-red-500/10 text-red-300',
}

export function LoanStatusBadge({ status }: { status: string }) {
  const key = status as LoanStatus
  const label = labels[key] ?? status.replace(/_/g, ' ')
  const className = styles[key] ?? 'border-border text-muted'

  return (
    <span
      className={`inline-flex rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize ${className}`}
    >
      {label}
    </span>
  )
}
