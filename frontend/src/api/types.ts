export type UserRole = 'admin' | 'librarian' | 'member' | 'customer'

export interface Profile {
  id: number
  username: string
  email: string
  role: UserRole
  photo_url: string | null
  bio: string
}

export interface UserProfileDetail {
  username: string
  email: string
  photo_url: string | null
  bio: string
  location: string | null
  place_name: string | null
  lat: number | null
  lng: number | null
}

export interface GeocodeResult {
  lat: number
  lng: number
  place_name: string
}

export interface NearbyUser {
  user_id: number
  username: string
  place_name: string | null
  distance_km: number
}

export interface NearbyUsersResponse {
  count: number
  radius_km: number
  users: NearbyUser[]
}

export interface Book {
  id: number
  title: string
  author: string
  isbn: string
  available_copies: number
}

export type LoanStatus = 'pending_payment' | 'borrowed' | 'returned' | 'cancelled'

export interface LoanRow {
  id: number
  borrower_name: string
  borrowed_date: string
  due_date: string
  status: LoanStatus | string
  total_books: number
}

export type PaymentStatus = 'pending' | 'success' | 'failed' | 'refunded'

export interface PaymentRecord {
  id: number
  reference: string
  expected_amount: string
  amount_paid: string | null
  status: PaymentStatus
  loan_id: number
  created_at: string
  paid_at: string | null
}

export interface InitiatePaymentResponse {
  authorization_url: string
  reference: string
  amount: number
  book_count: number
  loan_id: number
  message: string
}

export interface VerifyPaymentResponse {
  message: string
  status: 'success' | 'failed'
  loan_id: number
  amount_paid?: number
  due_date?: string
}
