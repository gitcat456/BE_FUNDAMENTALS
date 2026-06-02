import type {
  InitiatePaymentResponse,
  PaymentRecord,
  VerifyPaymentResponse,
} from './types'
import { apiJson } from './client'

/** Matches Django `LOAN_PRICE_KES` in config/settings.py */
export const LOAN_PRICE_KES = 50
export const MAX_BOOKS_PER_LOAN = 5

export async function initiateLoanPayment(
  bookIds: number[],
): Promise<InitiatePaymentResponse> {
  return apiJson<InitiatePaymentResponse>('/payments/initiate/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      books: bookIds.map((book_id) => ({ book_id })),
    }),
  })
}

export async function verifyLoanPayment(reference: string): Promise<VerifyPaymentResponse> {
  return apiJson<VerifyPaymentResponse>('/payments/verify/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reference }),
  })
}

export async function fetchPaymentHistory(): Promise<PaymentRecord[]> {
  return apiJson<PaymentRecord[]>('/payments/history/')
}

/** Latest pending Paystack reference per loan (for retry verify). */
export function pendingReferenceByLoanId(payments: PaymentRecord[]): Map<number, string> {
  const map = new Map<number, string>()
  for (const p of payments) {
    if (p.status === 'pending') {
      map.set(p.loan_id, p.reference)
    }
  }
  return map
}
