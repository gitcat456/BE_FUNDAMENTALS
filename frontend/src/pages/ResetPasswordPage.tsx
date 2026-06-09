import { useState } from 'react'
import { Link, Navigate, useNavigate, useSearchParams } from 'react-router-dom'
import { resetPassword } from '../api/authApi'
import { useAuth } from '../auth/AuthContext'
import {
  AuthPageShell,
  authInputClass,
  authLabelClass,
  authLinkClass,
  authSubmitClass,
} from '../components/auth/AuthPageShell'
import { useSnackbar } from '../components/snackbar/SnackbarProvider'

export function ResetPasswordPage() {
  const { profile, loading } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token') ?? ''
  const { showSuccess, showError } = useSnackbar()
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [pending, setPending] = useState(false)

  if (!loading && profile) {
    return <Navigate to={`/workspace/${profile.role}`} replace />
  }

  if (!token) {
    return (
      <AuthPageShell
        title="Invalid reset link"
        subtitle="This password reset link is missing a token or has expired. Request a new one to continue."
        footer={
          <>
            <Link to="/forgot-password" className={authLinkClass}>
              Request a new link
            </Link>
            {' · '}
            <Link to="/login" className={authLinkClass}>
              Sign in
            </Link>
          </>
        }
      >
        <p className="text-sm text-muted">
          Reset links expire after 15 minutes and can only be used once.
        </p>
      </AuthPageShell>
    )
  }

  return (
    <AuthPageShell
      title="Set new password"
      subtitle="Choose a strong password for your library account."
      footer={
        <>
          <Link to="/login" className={authLinkClass}>
            Back to sign in
          </Link>
        </>
      }
    >
      <form
        onSubmit={async (e) => {
          e.preventDefault()
          if (password !== confirmPassword) {
            showError('Passwords do not match.', 'Check your entries')
            return
          }
          setPending(true)
          try {
            const data = await resetPassword(token, password)
            showSuccess(data.message, 'Password updated')
            navigate('/login', { replace: true })
          } catch (err) {
            showError(
              err instanceof Error ? err.message : 'Could not reset password',
              'Reset failed',
            )
          } finally {
            setPending(false)
          }
        }}
        className="space-y-5"
      >
        <label className={authLabelClass}>
          New password
          <input
            type="password"
            className={authInputClass}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="new-password"
            required
            minLength={8}
          />
        </label>
        <label className={authLabelClass}>
          Confirm new password
          <input
            type="password"
            className={authInputClass}
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            autoComplete="new-password"
            required
            minLength={8}
          />
        </label>
        <p className="text-xs leading-relaxed text-muted">
          At least 8 characters with uppercase, lowercase, a number, and a special character.
        </p>
        <button type="submit" disabled={pending} className={authSubmitClass}>
          {pending ? 'Updating…' : 'Update password'}
        </button>
      </form>
    </AuthPageShell>
  )
}
