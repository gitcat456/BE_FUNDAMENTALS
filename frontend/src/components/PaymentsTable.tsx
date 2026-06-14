import type { PaymentRecord } from '../api/types'

type Props = {
  payments: PaymentRecord[]
  onRefund?: (paymentId: number) => void
  refundingPaymentId?: number | null
  showPayer?: boolean
}

const statusStyles: Record<string, string> = {
  pending: 'text-warn',
  success: 'text-ok',
  failed: 'text-red-300',
  refunded: 'text-muted',
}

function payerLabel(p: PaymentRecord): string | null {
  if ('username' in p && typeof p.username === 'string') return p.username
  return null
}

export function PaymentsTable({
  payments,
  onRefund,
  refundingPaymentId = null,
  showPayer = false,
}: Props) {
  const showActions = Boolean(onRefund)
  const colCount = 6 + (showPayer ? 1 : 0) + (showActions ? 1 : 0)

  return (
    <div className="overflow-x-auto rounded-xl border border-border bg-surface">
      <table className="w-full min-w-[720px] text-left text-sm">
        <thead>
          <tr className="border-b border-border text-muted">
            {showPayer ? <th className="px-4 py-3 font-medium">Payer</th> : null}
            <th className="px-4 py-3 font-medium">Reference</th>
            <th className="px-4 py-3 font-medium">Expected</th>
            <th className="px-4 py-3 font-medium">Paid</th>
            <th className="px-4 py-3 font-medium">Status</th>
            <th className="px-4 py-3 font-medium">Loan</th>
            <th className="px-4 py-3 font-medium">Created</th>
            {showActions ? <th className="px-4 py-3 font-medium w-28" /> : null}
          </tr>
        </thead>
        <tbody>
          {payments.length === 0 ? (
            <tr>
              <td colSpan={colCount} className="px-4 py-8 text-center text-muted">
                No payments yet.
              </td>
            </tr>
          ) : (
            payments.map((p) => (
              <tr
                key={p.id}
                className="border-b border-border/60 last:border-0 hover:bg-surface-2/80"
              >
                {showPayer ? (
                  <td className="px-4 py-3 text-ink">{payerLabel(p) ?? '—'}</td>
                ) : null}
                <td className="px-4 py-3 font-mono text-xs text-ink">{p.reference}</td>
                <td className="px-4 py-3">KES {p.expected_amount}</td>
                <td className="px-4 py-3 text-muted">
                  {p.amount_paid != null ? `KES ${p.amount_paid}` : '—'}
                </td>
                <td className={`px-4 py-3 capitalize ${statusStyles[p.status] ?? ''}`}>
                  {p.status}
                </td>
                <td className="px-4 py-3 font-mono text-xs text-muted">#{p.loan_id}</td>
                <td className="px-4 py-3 text-muted">
                  {new Date(p.created_at).toLocaleString()}
                </td>
                {showActions ? (
                  <td className="px-4 py-3">
                    {p.status === 'success' ? (
                      <button
                        type="button"
                        disabled={refundingPaymentId === p.id}
                        onClick={() => onRefund?.(p.id)}
                        className="text-xs font-medium text-warn hover:underline disabled:opacity-50"
                      >
                        {refundingPaymentId === p.id ? 'Refunding…' : 'Refund'}
                      </button>
                    ) : (
                      <span className="text-xs text-muted">—</span>
                    )}
                  </td>
                ) : null}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
