import { useRef, useState } from 'react'
import type { Book } from '../api/types'
import { ALLOWED_DOCUMENT_ACCEPT } from '../api/storageApi'

type Props = {
  book: Book
  canUpload?: boolean
  onUpload?: (bookId: number, file: File) => Promise<void>
  onDownload: (book: Book) => Promise<void>
}

export function BookDigitalResourceCell({ book, canUpload, onUpload, onDownload }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [uploading, setUploading] = useState(false)
  const [downloading, setDownloading] = useState(false)

  const hasFile = Boolean(book.digital_object_name && book.digital_filename)
  const busy = uploading || downloading

  async function onFileSelected(file: File | undefined) {
    if (!file || !onUpload) return
    setUploading(true)
    try {
      await onUpload(book.id, file)
    } finally {
      setUploading(false)
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  return (
    <div className="flex flex-wrap items-center gap-2">
      {hasFile ? (
        <button
          type="button"
          disabled={busy}
          onClick={() => {
            setDownloading(true)
            void onDownload(book).finally(() => setDownloading(false))
          }}
          className="max-w-[10rem] truncate text-xs font-medium text-accent hover:underline disabled:opacity-50"
          title={book.digital_filename ?? undefined}
        >
          {downloading ? 'Opening…' : book.digital_filename}
        </button>
      ) : (
        <span className="text-xs text-muted">—</span>
      )}
      {canUpload && onUpload ? (
        <>
          <input
            ref={inputRef}
            type="file"
            accept={ALLOWED_DOCUMENT_ACCEPT}
            className="sr-only"
            disabled={busy}
            onChange={(e) => void onFileSelected(e.target.files?.[0])}
          />
          <button
            type="button"
            disabled={busy}
            onClick={() => inputRef.current?.click()}
            className="text-xs font-medium text-muted hover:text-ink disabled:opacity-50"
          >
            {uploading ? 'Uploading…' : hasFile ? 'Replace' : 'Attach'}
          </button>
        </>
      ) : null}
    </div>
  )
}
