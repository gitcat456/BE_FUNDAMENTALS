import { useCallback, useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { fetchAllPayments, fetchPaymentHistory } from '../../api/paymentsApi'
import type { PaymentRecord } from '../../api/types'
import { useAuth } from '../../auth/AuthContext'
import { PaymentsTable } from '../../components/PaymentsTable'
import { usePaymentRefund } from '../../hooks/usePaymentRefund'
import { canUsePayments, normalizeUserRole } from '../../utils/role'

export function PaymentsPage() {
  const { profile } = useAuth()
  const [payments, setPayments] = useState<PaymentRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const role = profile ? normalizeUserRole(profile.role) : null
  const isAdmin = role === 'admin'

  const load = useCallback(async () => {
    if (!profile || !role) return
    setLoading(true)
    try {
      setPayments(isAdmin ? await fetchAllPayments() : await fetchPaymentHistory())
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load payments')
    } finally {
      setLoading(false)
    }
  }, [profile, role, isAdmin])

  const { refund, refundingPaymentId } = usePaymentRefund(load)

  useEffect(() => {
    void load()
  }, [load])

  if (!profile || !role) return null

  if (!canUsePayments(role)) {
    return <Navigate to={`/workspace/${role}`} replace />
  }

  return (
    <div className="max-w-6xl">
      <h1 className="font-display text-2xl font-semibold text-ink">
        {isAdmin ? 'All payments' : 'Payments'}
      </h1>
      <p className="mt-2 text-sm text-muted">
        {isAdmin ? (
          <>
            Every Paystack loan payment in the system. Refund successful charges on behalf of
            members — the loan is cancelled and book copies are restored.
          </>
        ) : (
          <>
            Your Paystack loan payments. Successful charges can be refunded — the linked loan is
            cancelled and book copies are restored.
          </>
        )}
      </p>

      {error ? (
        <p className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </p>
      ) : null}

      <div className="mt-8">
        {loading ? (
          <p className="text-sm text-muted">Loading…</p>
        ) : (
          <PaymentsTable
            payments={payments}
            onRefund={refund}
            refundingPaymentId={refundingPaymentId}
            showPayer={isAdmin}
          />
        )}
      </div>
    </div>
  )
}
