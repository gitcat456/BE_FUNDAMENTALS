import { useState } from 'react'

import { Link, Navigate, useNavigate } from 'react-router-dom'

import { register } from '../api/authApi'

import { useAuth } from '../auth/AuthContext'

import {

  AuthPageShell,

  authInputClass,

  authLabelClass,

  authLinkClass,

  authSubmitClass,

} from '../components/auth/AuthPageShell'

import { AuthDivider } from '../components/auth/AuthDivider'

import { GoogleSignInButton, isGoogleSignInConfigured } from '../components/auth/GoogleSignInButton'

import { useSnackbar } from '../components/snackbar/SnackbarProvider'



export function SignupPage() {

  const { profile, loading, loginWithGoogle } = useAuth()

  const navigate = useNavigate()

  const { showSuccess, showError } = useSnackbar()

  const [username, setUsername] = useState('')

  const [email, setEmail] = useState('')

  const [password, setPassword] = useState('')

  const [confirmPassword, setConfirmPassword] = useState('')

  const [pending, setPending] = useState(false)

  const [googlePending, setGooglePending] = useState(false)



  const busy = pending || googlePending

  const googleEnabled = isGoogleSignInConfigured()



  if (!loading && profile) {

    return <Navigate to={`/workspace/${profile.role}`} replace />

  }



  async function onGoogleCredential(idToken: string) {

    setGooglePending(true)

    try {

      const { profile: p, isNewUser } = await loginWithGoogle(idToken)

      showSuccess(

        isNewUser ? 'Your account was created with Google.' : 'Welcome back!',

        isNewUser ? 'Account created' : 'Signed in',

      )

      navigate(`/workspace/${p.role}`, { replace: true })

    } catch (err) {

      showError(err instanceof Error ? err.message : 'Google sign-up failed', 'Could not continue')

    } finally {

      setGooglePending(false)

    }

  }



  return (

    <AuthPageShell

      title="Create account"

      subtitle="Sign up with Google or register with email. Google accounts skip the password step."

      footer={

        <>

          Already have an account?{' '}

          <Link to="/login" className={authLinkClass}>

            Sign in

          </Link>

        </>

      }

    >

      {googleEnabled ? (

        <>

          <GoogleSignInButton

            text="signup_with"

            disabled={busy}

            onCredential={(token) => void onGoogleCredential(token)}

            onError={() => showError('Google sign-up was cancelled or failed.', 'Sign up failed')}

          />

          <AuthDivider label="or with email" />

        </>

      ) : null}



      <form

        onSubmit={async (e) => {

          e.preventDefault()

          if (password !== confirmPassword) {

            showError('Passwords do not match.', 'Check your entries')

            return

          }

          setPending(true)

          try {

            await register({

              username: username.trim(),

              email: email.trim(),

              password,

            })

            showSuccess('Your account is ready. Sign in to continue.', 'Welcome aboard')

            navigate('/login', { replace: true })

          } catch (err) {

            showError(

              err instanceof Error ? err.message : 'Registration failed',

              'Could not create account',

            )

          } finally {

            setPending(false)

          }

        }}

        className="space-y-5"

      >

        <label className={authLabelClass}>

          Username

          <input

            className={authInputClass}

            value={username}

            onChange={(e) => setUsername(e.target.value)}

            autoComplete="username"

            required

            disabled={busy}

          />

        </label>

        <label className={authLabelClass}>

          Email

          <input

            type="email"

            className={authInputClass}

            value={email}

            onChange={(e) => setEmail(e.target.value)}

            autoComplete="email"

            required

            disabled={busy}

          />

        </label>

        <label className={authLabelClass}>

          Password

          <input

            type="password"

            className={authInputClass}

            value={password}

            onChange={(e) => setPassword(e.target.value)}

            autoComplete="new-password"

            required

            minLength={8}

            disabled={busy}

          />

        </label>

        <label className={authLabelClass}>

          Confirm password

          <input

            type="password"

            className={authInputClass}

            value={confirmPassword}

            onChange={(e) => setConfirmPassword(e.target.value)}

            autoComplete="new-password"

            required

            minLength={8}

            disabled={busy}

          />

        </label>

        <p className="text-xs leading-relaxed text-[var(--color-muted)]">

          At least 8 characters with uppercase, lowercase, a number, and a special character.

        </p>

        <button type="submit" disabled={busy} className={authSubmitClass}>

          {pending ? 'Creating account…' : 'Create account'}

        </button>

      </form>

    </AuthPageShell>

  )

}


