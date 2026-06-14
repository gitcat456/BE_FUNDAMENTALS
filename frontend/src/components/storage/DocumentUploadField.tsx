import { useRef, useState } from 'react'
import { ALLOWED_DOCUMENT_ACCEPT } from '../../api/storageApi'

type Props = {
  label: string
  hint: string
  existingFilename?: string | null
  disabled?: boolean
  uploading?: boolean
  onUpload: (file: File) => Promise<void>
  onDownload?: () => Promise<void>
}

export function DocumentUploadField({
  label,
  hint,
  existingFilename,
  disabled,
  uploading,
  onUpload,
  onDownload,
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [downloading, setDownloading] = useState(false)

  async function onFileSelected(file: File | undefined) {
    if (!file) return
    try {
      await onUpload(file)
    } finally {
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  async function handleDownload() {
    if (!onDownload) return
    setDownloading(true)
    try {
      await onDownload()
    } finally {
      setDownloading(false)
    }
  }

  const busy = Boolean(disabled || uploading || downloading)

  return (
    <div className="rounded-2xl border border-border bg-surface/80 p-6">
      <p className="text-sm font-medium text-ink">{label}</p>
      <p className="mt-2 text-sm text-muted">{hint}</p>

      {existingFilename ? (
        <p className="mt-4 truncate text-sm text-ink">
          <span className="text-muted">Current file:</span> {existingFilename}
        </p>
      ) : (
        <p className="mt-4 text-sm text-muted">No file uploaded yet.</p>
      )}

      <div className="mt-4 flex flex-wrap gap-3">
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
          className="rounded-xl border border-border px-4 py-2 text-sm font-medium text-ink transition hover:border-accent-dim disabled:opacity-50"
        >
          {uploading ? 'Uploading…' : existingFilename ? 'Replace file' : 'Upload file'}
        </button>
        {existingFilename && onDownload ? (
          <button
            type="button"
            disabled={busy}
            onClick={() => void handleDownload()}
            className="rounded-xl border border-accent-dim/50 px-4 py-2 text-sm font-medium text-accent transition hover:border-accent disabled:opacity-50"
          >
            {downloading ? 'Preparing…' : 'Download'}
          </button>
        ) : null}
      </div>
    </div>
  )
}
