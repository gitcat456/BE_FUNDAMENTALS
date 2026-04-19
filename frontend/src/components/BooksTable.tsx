import type { Book } from '../api/types'

type Props = {
  books: Book[]
  onDelete?: (id: number) => void
  canDelete?: boolean
}

export function BooksTable({ books, onDelete, canDelete }: Props) {
  return (
    <div className="overflow-x-auto rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]">
      <table className="w-full min-w-[640px] text-left text-sm">
        <thead>
          <tr className="border-b border-[var(--color-border)] text-[var(--color-muted)]">
            <th className="px-4 py-3 font-medium">Title</th>
            <th className="px-4 py-3 font-medium">Author</th>
            <th className="px-4 py-3 font-medium">ISBN</th>
            <th className="px-4 py-3 font-medium">Available</th>
            {canDelete && onDelete ? <th className="px-4 py-3 font-medium w-24" /> : null}
          </tr>
        </thead>
        <tbody>
          {books.length === 0 ? (
            <tr>
              <td colSpan={5} className="px-4 py-8 text-center text-[var(--color-muted)]">
                No books loaded yet.
              </td>
            </tr>
          ) : (
            books.map((b) => (
              <tr
                key={b.id}
                className="border-b border-[var(--color-border)]/60 last:border-0 hover:bg-[var(--color-surface-2)]/80"
              >
                <td className="px-4 py-3 font-medium text-[var(--color-ink)]">{b.title}</td>
                <td className="px-4 py-3 text-[var(--color-muted)]">{b.author}</td>
                <td className="px-4 py-3 font-mono text-xs text-[var(--color-muted)]">{b.isbn}</td>
                <td className="px-4 py-3">
                  <span
                    className={
                      b.available_copies > 0
                        ? 'text-[var(--color-ok)]'
                        : 'text-[var(--color-warn)]'
                    }
                  >
                    {b.available_copies}
                  </span>
                </td>
                {canDelete && onDelete ? (
                  <td className="px-4 py-3">
                    <button
                      type="button"
                      onClick={() => onDelete(b.id)}
                      className="text-xs font-medium text-red-400/90 hover:text-red-300"
                    >
                      Remove
                    </button>
                  </td>
                ) : null}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
