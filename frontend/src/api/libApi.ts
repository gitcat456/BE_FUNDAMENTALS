import type { Book, LoanRow } from './types'
import { apiFetch, apiJson } from './client'

export async function fetchBooks(): Promise<Book[]> {
  return apiJson<Book[]>('/list/')
}

export async function fetchLoans(): Promise<LoanRow[]> {
  return apiJson<LoanRow[]>('/loan-list/')
}

export async function createBook(body: Omit<Book, 'id'>): Promise<Book> {
  return apiJson<Book>('/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}

export async function deleteBook(id: number): Promise<void> {
  const res = await apiFetch(`/del/${id}/`, { method: 'DELETE' })
  if (!res.ok) {
    const t = await res.text()
    throw new Error(t || `HTTP ${res.status}`)
  }
}

export async function createLoan(body: {
  borrower_email: string
  due_date: string
  book_isbns: string[]
}): Promise<unknown> {
  return apiJson('/loans/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
}
