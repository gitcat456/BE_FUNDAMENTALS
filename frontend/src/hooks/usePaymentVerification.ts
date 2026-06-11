import { useCallback, useState } from 'react'
import { verifyLoanPayment } from '../api/paymentsApi'
import { useSnackbar } from '../components/snackbar/SnackbarProvider'

export function usePaymentVerification(onVerified?: () => void | Promise<void>) {
  const { showSuccess, showError } = useSnackbar()
  const [verifyingReference, setVerifyingReference] = useState<string | null>(null)

  const verify = useCallback(
    async (reference: string) => {
      setVerifyingReference(reference)
      try {
        const result = await verifyLoanPayment(reference)
        showSuccess(result.message, 'Payment verified')
        await onVerified?.()
      } catch (e) {
        showError(e instanceof Error ? e.message : 'Verification failed')
      } finally {
        setVerifyingReference(null)
      }
    },
    [onVerified, showError, showSuccess],
  )

  return { verify, verifyingReference }
}
