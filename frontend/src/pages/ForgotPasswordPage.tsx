import { useState } from 'react'
import { Link, Navigate } from 'react-router-dom'
import { forgotPassword } from '../api/authApi'
import { useAuth } from '../auth/AuthContext'
import {
  AuthPageShell,
  authInputClass,
  authLabelClass,
  authLinkClass,
  authSubmitClass,
} from '../components/auth/AuthPageShell'
import { useSnackbar } from '../components/snackbar/SnackbarProvider'

export function ForgotPasswordPage() {
  const { profile, loading } = useAuth()
  const { showSuccess, showError } = useSnackbar()
  const [email, setEmail] = useState('')
  const [pending, setPending] = useState(false)
  const [sent, setSent] = useState(false)

  if (!loading && profile) {
    return <Navigate to={`/workspace/${profile.role}`} replace />
  }

  return (
    <AuthPageShell
      title="Forgot password"
      subtitle="Enter the email on your account. If it exists, we'll send a reset link that expires in 15 minutes."
      footer={
        <>
          Remember your password?{' '}
          <Link to="/login" className={authLinkClass}>
            Back to sign in
          </Link>
        </>
      }
    >
      <form
        onSubmit={async (e) => {
          e.preventDefault()
          setPending(true)
          try {
            const data = await forgotPassword(email.trim())
            setSent(true)
            showSuccess(
              data.message,
              'Reset link sent',
            )
          } catch (err) {
            showError(
              err instanceof Error ? err.message : 'Could not send reset link',
              'Request failed',
            )
          } finally {
            setPending(false)
          }
        }}
        className="space-y-5"
      >
        <label className={authLabelClass}>
          Email
          <input
            type="email"
            className={authInputClass}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            required
          />
        </label>
        {sent ? (
          <p className="text-sm leading-relaxed text-muted">
            Check your inbox for the reset link. You can close this page or try again with a
            different email.
          </p>
        ) : null}
        <button type="submit" disabled={pending} className={authSubmitClass}>
          {pending ? 'Sending…' : sent ? 'Send again' : 'Send reset link'}
        </button>
      </form>
    </AuthPageShell>
  )
}
