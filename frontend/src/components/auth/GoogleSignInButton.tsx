import { GoogleLogin, type CredentialResponse } from '@react-oauth/google'

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID

type GoogleSignInButtonProps = {
  onCredential: (idToken: string) => void
  onError?: () => void
  disabled?: boolean
  text?: 'signin_with' | 'signup_with' | 'continue_with'
}

export function GoogleSignInButton({
  onCredential,
  onError,
  disabled,
  text = 'continue_with',
}: GoogleSignInButtonProps) {
  if (!GOOGLE_CLIENT_ID) return null

  function handleSuccess(response: CredentialResponse) {
    if (response.credential) {
      onCredential(response.credential)
      return
    }
    onError?.()
  }

  return (
    <div
      className={`flex w-full justify-center [&>div]:!w-full ${disabled ? 'pointer-events-none opacity-50' : ''}`}
    >
      <GoogleLogin
        text={text}
        shape="rectangular"
        theme="filled_black"
        size="large"
        width={360}
        onSuccess={handleSuccess}
        onError={() => onError?.()}
      />
    </div>
  )
}

export function isGoogleSignInConfigured(): boolean {
  return Boolean(GOOGLE_CLIENT_ID)
}
