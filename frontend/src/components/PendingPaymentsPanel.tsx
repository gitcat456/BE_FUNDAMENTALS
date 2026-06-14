import type { PaymentRecord } from '../api/types'

type Props = {
  payments: PaymentRecord[]
  onVerify: (reference: string) => void
  verifyingReference: string | null
}

export function PendingPaymentsPanel({ payments, onVerify, verifyingReference }: Props) {
  const pending = payments.filter((p) => p.status === 'pending')
  if (pending.length === 0) return null

  return (
    <div className="mt-8 rounded-2xl border border-warn/30 bg-warn/5 p-5">
      <p className="text-sm font-medium text-ink">Checkout awaiting verification</p>
      <p className="mt-1 text-xs text-muted">
        Paid on Paystack but the loan is not active yet? Confirm each payment below.
      </p>
      <ul className="mt-4 space-y-3">
        {pending.map((p) => (
          <li
            key={p.id}
            className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-border bg-surface px-4 py-3"
          >
            <div className="min-w-0 text-sm">
              <span className="font-mono text-xs text-accent">{p.reference}</span>
              <span className="ml-2 text-muted">
                Loan #{p.loan_id} · KES {p.expected_amount}
              </span>
            </div>
            <button
              type="button"
              disabled={verifyingReference === p.reference}
              onClick={() => void onVerify(p.reference)}
              className="shrink-0 rounded-lg border border-accent-dim px-3 py-1.5 text-xs font-semibold text-accent transition hover:bg-accent/10 disabled:opacity-50"
            >
              {verifyingReference === p.reference ? 'Verifying…' : 'Retry verify'}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
