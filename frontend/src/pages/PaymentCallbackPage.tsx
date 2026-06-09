import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { verifyLoanPayment } from '../api/paymentsApi'
import { useAuth } from '../auth/AuthContext'
import { useSnackbar } from '../components/snackbar/SnackbarProvider'

export function PaymentCallbackPage() {
  const [searchParams] = useSearchParams()
  const reference = searchParams.get('reference') ?? searchParams.get('trxref') ?? ''
  const { profile } = useAuth()
  const navigate = useNavigate()
  const { showSuccess, showError } = useSnackbar()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')
  const [dueDate, setDueDate] = useState<string | null>(null)
  const verified = useRef(false)

  useEffect(() => {
    if (!reference) {
      setStatus('error')
      setMessage('No payment reference in the URL. Return from Paystack should include ?reference=…')
      return
    }
    if (verified.current) return
    verified.current = true

    void (async () => {
      try {
        const result = await verifyLoanPayment(reference)
        setStatus('success')
        setMessage(result.message)
        if (result.due_date) setDueDate(result.due_date)
        showSuccess(result.message, 'Payment confirmed')
      } catch (e) {
        const msg = e instanceof Error ? e.message : 'Payment verification failed'
        setStatus('error')
        setMessage(msg)
        showError(msg, 'Verification failed')
      }
    })()
  }, [reference, showError, showSuccess])

  const loansPath = profile ? `/workspace/${profile.role}/loans` : '/login'

  return (
    <div className="flex min-h-screen items-center justify-center px-6 py-16">
      <div className="w-full max-w-md rounded-2xl border border-border bg-surface p-8 text-center">
        {status === 'loading' ? (
          <>
            <p className="font-display text-xl font-semibold text-ink">
              Confirming payment…
            </p>
            <p className="mt-3 text-sm text-muted">
              Verifying <span className="font-mono text-accent">{reference}</span>{' '}
              with the library.
            </p>
          </>
        ) : null}

        {status === 'success' ? (
          <>
            <p className="font-display text-xl font-semibold text-ok">
              You&apos;re all set
            </p>
            <p className="mt-3 text-sm text-muted">{message}</p>
            {dueDate ? (
              <p className="mt-2 text-sm text-ink">
                Return books by <strong>{dueDate}</strong>.
              </p>
            ) : null}
          </>
        ) : null}

        {status === 'error' ? (
          <>
            <p className="font-display text-xl font-semibold text-red-300">Payment issue</p>
            <p className="mt-3 text-sm text-muted">{message}</p>
          </>
        ) : null}

        {status !== 'loading' ? (
          <div className="mt-8 flex flex-col gap-3">
            <button
              type="button"
              onClick={() => navigate(loansPath, { replace: true })}
              className="rounded-xl bg-accent px-4 py-2.5 text-sm font-semibold text-canvas hover:brightness-110"
            >
              View my loans
            </button>
            <Link
              to={profile ? `/workspace/${profile.role}/browse` : '/login'}
              className="text-sm text-muted hover:text-accent"
            >
              Back to browse
            </Link>
          </div>
        ) : null}
      </div>
    </div>
  )
}
