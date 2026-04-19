export type UserRole = 'admin' | 'librarian' | 'member' | 'customer'

export interface Profile {
  id: number
  username: string
  email: string
  role: UserRole
}

export interface Book {
  id: number
  title: string
  author: string
  isbn: string
  available_copies: number
}

export interface LoanRow {
  id: number
  borrower_name: string
  borrowed_date: string
  due_date: string
  status: string
  total_books: number
}
