import { useCallback, useState } from 'react'
import { refundPayment } from '../api/paymentsApi'
import { useSnackbar } from '../components/snackbar/SnackbarProvider'

const REFUND_CONFIRM =
  'Refund this payment? Paystack will return the charge, the loan will be cancelled, and book copies will be restored.'

export function usePaymentRefund(onRefunded?: () => void | Promise<void>) {
  const { showSuccess, showError } = useSnackbar()
  const [refundingPaymentId, setRefundingPaymentId] = useState<number | null>(null)

  const refund = useCallback(
    async (paymentId: number) => {
      if (!window.confirm(REFUND_CONFIRM)) return

      setRefundingPaymentId(paymentId)
      try {
        const result = await refundPayment(paymentId)
        const detail =
          result.amount_refunded != null
            ? `${result.message} (KES ${result.amount_refunded})`
            : result.message
        showSuccess(detail, 'Refund processed')
        await onRefunded?.()
      } catch (e) {
        showError(e instanceof Error ? e.message : 'Refund failed')
      } finally {
        setRefundingPaymentId(null)
      }
    },
    [onRefunded, showError, showSuccess],
  )

  return { refund, refundingPaymentId }
}
