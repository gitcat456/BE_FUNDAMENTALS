import { useCallback, useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../../auth/AuthContext'
import { fetchBooks } from '../../api/libApi'
import type { Book } from '../../api/types'
import { BooksTable } from '../../components/BooksTable'

export function BrowsePage() {
  const { profile } = useAuth()
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setBooks(await fetchBooks())
      setError(null)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load books')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void load()
  }, [load])

  if (!profile) return null
  if (profile.role === 'admin' || profile.role === 'librarian') {
    return <Navigate to={`/workspace/${profile.role}/books`} replace />
  }

  return (
    <div className="max-w-5xl">
      <h1 className="font-display text-2xl font-semibold text-[var(--color-ink)]">
        {profile.role === 'member' ? 'Browse the stacks' : 'Catalog'}
      </h1>
      <p className="mt-2 text-sm text-[var(--color-muted)]">
        Read-only view of everything returned by <code className="text-[var(--color-accent)]">GET /api/list/</code>.
      </p>
      {error ? (
        <p className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </p>
      ) : null}
      <div className="mt-8">
        {loading ? (
          <p className="text-sm text-[var(--color-muted)]">Loading…</p>
        ) : (
          <BooksTable books={books} />
        )}
      </div>
    </div>
  )
}
