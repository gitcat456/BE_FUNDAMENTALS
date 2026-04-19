import { useCallback, useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../../auth/AuthContext'
import { createBook, deleteBook, fetchBooks } from '../../api/libApi'
import type { Book } from '../../api/types'
import { BooksTable } from '../../components/BooksTable'

export function BooksManagePage() {
  const { profile } = useAuth()
  const [books, setBooks] = useState<Book[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [form, setForm] = useState({ title: '', author: '', isbn: '', available_copies: '1' })

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
  if (profile.role === 'member' || profile.role === 'customer') {
    return <Navigate to={`/workspace/${profile.role}/browse`} replace />
  }

  const canDelete = profile.role === 'librarian' || profile.role === 'admin'

  async function onCreate(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      await createBook({
        title: form.title.trim(),
        author: form.author.trim(),
        isbn: form.isbn.trim(),
        available_copies: Number(form.available_copies) || 0,
      })
      setForm({ title: '', author: '', isbn: '', available_copies: '1' })
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not create book')
    }
  }

  async function onDelete(id: number) {
    if (!confirm('Remove this book from the catalog?')) return
    setError(null)
    try {
      await deleteBook(id)
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed')
    }
  }

  return (
    <div className="max-w-5xl">
      <h1 className="font-display text-2xl font-semibold text-[var(--color-ink)]">Catalog</h1>
      <p className="mt-2 text-sm text-[var(--color-muted)]">
        Backed by <code className="text-[var(--color-accent)]">GET /api/list/</code>,{' '}
        <code className="text-[var(--color-accent)]">POST /api/create/</code>, and{' '}
        <code className="text-[var(--color-accent)]">DELETE /api/del/&lt;id&gt;/</code>.
      </p>

      {canDelete ? (
        <form
          onSubmit={onCreate}
          className="mt-8 rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/80 p-6"
        >
          <p className="text-sm font-medium text-[var(--color-ink)]">Add a title</p>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <label className="text-xs uppercase text-[var(--color-muted)]">
              Title
              <input
                required
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm"
                value={form.title}
                onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              />
            </label>
            <label className="text-xs uppercase text-[var(--color-muted)]">
              Author
              <input
                required
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm"
                value={form.author}
                onChange={(e) => setForm((f) => ({ ...f, author: e.target.value }))}
              />
            </label>
            <label className="text-xs uppercase text-[var(--color-muted)]">
              ISBN
              <input
                required
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm font-mono"
                value={form.isbn}
                onChange={(e) => setForm((f) => ({ ...f, isbn: e.target.value }))}
              />
            </label>
            <label className="text-xs uppercase text-[var(--color-muted)]">
              Copies
              <input
                required
                type="number"
                min={0}
                className="mt-1 w-full rounded-lg border border-[var(--color-border)] bg-[var(--color-canvas)] px-3 py-2 text-sm"
                value={form.available_copies}
                onChange={(e) => setForm((f) => ({ ...f, available_copies: e.target.value }))}
              />
            </label>
          </div>
          <button
            type="submit"
            className="mt-4 rounded-xl bg-[var(--color-accent)] px-4 py-2 text-sm font-semibold text-[var(--color-canvas)] hover:brightness-110"
          >
            Create book
          </button>
        </form>
      ) : null}

      {error ? (
        <p className="mt-6 rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
          {error}
        </p>
      ) : null}

      <div className="mt-8">
        {loading ? (
          <p className="text-sm text-[var(--color-muted)]">Loading catalog…</p>
        ) : (
          <BooksTable books={books} canDelete={canDelete} onDelete={canDelete ? onDelete : undefined} />
        )}
      </div>
    </div>
  )
}
