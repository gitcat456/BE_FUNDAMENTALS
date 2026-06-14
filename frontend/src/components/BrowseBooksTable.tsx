import type { Book } from '../api/types'
import { BookDigitalResourceCell } from './BookDigitalResourceCell'

type Props = {
  books: Book[]
  selectedIds: Set<number>
  onToggle: (bookId: number) => void
  maxSelection: number
  onDigitalDownload?: (book: Book) => Promise<void>
}

export function BrowseBooksTable({
  books,
  selectedIds,
  onToggle,
  maxSelection,
  onDigitalDownload,
}: Props) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border bg-surface">
      <table className="w-full min-w-[720px] text-left text-sm">
        <thead>
          <tr className="border-b border-border text-muted">
            <th className="w-12 px-4 py-3 font-medium" />
            <th className="px-4 py-3 font-medium">Title</th>
            <th className="px-4 py-3 font-medium">Author</th>
            <th className="px-4 py-3 font-medium">ISBN</th>
            <th className="px-4 py-3 font-medium">Available</th>
            <th className="px-4 py-3 font-medium">Resource</th>
          </tr>
        </thead>
        <tbody>
          {books.length === 0 ? (
            <tr>
              <td colSpan={6} className="px-4 py-8 text-center text-muted">
                No books in the catalog.
              </td>
            </tr>
          ) : (
            books.map((b) => {
              const available = b.available_copies > 0
              const selected = selectedIds.has(b.id)
              const atMax = selectedIds.size >= maxSelection && !selected

              return (
                <tr
                  key={b.id}
                  className={[
                    'border-b border-border/60 last:border-0',
                    available ? 'hover:bg-surface-2/80' : 'opacity-60',
                    selected ? 'bg-accent/5' : '',
                  ].join(' ')}
                >
                  <td className="px-4 py-3">
                    <input
                      type="checkbox"
                      checked={selected}
                      disabled={!available || atMax}
                      onChange={() => onToggle(b.id)}
                      className="size-4 rounded border-border accent-accent"
                      aria-label={`Select ${b.title}`}
                    />
                  </td>
                  <td className="px-4 py-3 font-medium text-ink">{b.title}</td>
                  <td className="px-4 py-3 text-muted">{b.author}</td>
                  <td className="px-4 py-3 font-mono text-xs text-muted">{b.isbn}</td>
                  <td className="px-4 py-3">
                    <span
                      className={
                        available ? 'text-ok' : 'text-warn'
                      }
                    >
                      {b.available_copies}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    {onDigitalDownload && b.digital_object_name ? (
                      <BookDigitalResourceCell
                        book={b}
                        onDownload={onDigitalDownload}
                      />
                    ) : (
                      <span className="text-xs text-muted">—</span>
                    )}
                  </td>
                </tr>
              )
            })
          )}
        </tbody>
      </table>
    </div>
  )
}
