import type { ReactNode } from 'react'
import { PencilIcon } from './PencilIcon'

type EditableProfileFieldProps = {
  label: string
  display: ReactNode
  emptyLabel?: string
  editing: boolean
  disabled?: boolean
  onEdit: () => void
  onCancel: () => void
  onSave: () => void
  saving?: boolean
  children: ReactNode
}

export function EditableProfileField({
  label,
  display,
  emptyLabel = 'Not set',
  editing,
  disabled,
  onEdit,
  onCancel,
  onSave,
  saving,
  children,
}: EditableProfileFieldProps) {
  return (
    <section className="rounded-2xl border border-border bg-surface/80 p-6">
      <div className="flex items-start justify-between gap-3">
        <p className="text-sm font-medium text-ink">{label}</p>
        {!editing ? (
          <button
            type="button"
            onClick={onEdit}
            disabled={disabled}
            aria-label={`Edit ${label.toLowerCase()}`}
            className="shrink-0 rounded-lg p-2 text-muted transition hover:bg-canvas hover:text-accent disabled:opacity-50"
          >
            <PencilIcon />
          </button>
        ) : null}
      </div>

      {!editing ? (
        <div className="mt-3 text-sm leading-relaxed text-ink">
          {display ?? (
            <span className="text-muted italic">{emptyLabel}</span>
          )}
        </div>
      ) : (
        <div className="mt-3">
          {children}
          <div className="mt-4 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={onSave}
              disabled={disabled || saving}
              className="rounded-xl bg-accent px-4 py-2 text-sm font-semibold text-canvas transition hover:brightness-110 disabled:opacity-50"
            >
              {saving ? 'Saving…' : 'Save'}
            </button>
            <button
              type="button"
              onClick={onCancel}
              disabled={disabled || saving}
              className="rounded-xl border border-border px-4 py-2 text-sm font-medium text-ink transition hover:border-accent-dim disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </section>
  )
}
