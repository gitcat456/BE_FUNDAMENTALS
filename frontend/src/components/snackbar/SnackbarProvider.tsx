import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

export type SnackbarVariant = 'success' | 'error' | 'info'

export type Snackbar = {
  id: string
  message: string
  title?: string
  variant: SnackbarVariant
}

type SnackbarContextValue = {
  showSnackbar: (message: string, variant?: SnackbarVariant, title?: string) => void
  showSuccess: (message: string, title?: string) => void
  showError: (message: string, title?: string) => void
}

const SnackbarContext = createContext<SnackbarContextValue | null>(null)

const AUTO_DISMISS_MS = 5200

function SnackbarItem({ snackbar, onDismiss }: { snackbar: Snackbar; onDismiss: () => void }) {
  const accent =
    snackbar.variant === 'success'
      ? 'var(--color-ok)'
      : snackbar.variant === 'error'
        ? '#f87171'
        : 'var(--color-accent)'

  const icon =
    snackbar.variant === 'success' ? (
      <svg viewBox="0 0 20 20" fill="currentColor" className="size-4">
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
          clipRule="evenodd"
        />
      </svg>
    ) : snackbar.variant === 'error' ? (
      <svg viewBox="0 0 20 20" fill="currentColor" className="size-4">
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
          clipRule="evenodd"
        />
      </svg>
    ) : (
      <svg viewBox="0 0 20 20" fill="currentColor" className="size-4">
        <path
          fillRule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z"
          clipRule="evenodd"
        />
      </svg>
    )

  return (
    <div
      role="alert"
      className="snackbar-enter pointer-events-auto relative w-[min(100vw-2rem,22rem)] overflow-hidden rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)]/95 shadow-2xl backdrop-blur-md"
      style={{ boxShadow: `0 12px 40px -8px color-mix(in srgb, ${accent} 35%, transparent)` }}
    >
      <div className="absolute inset-y-0 left-0 w-1" style={{ backgroundColor: accent }} />
      <div className="flex items-start gap-3 px-4 py-3.5 pl-5">
        <span
          className="mt-0.5 flex size-7 shrink-0 items-center justify-center rounded-full"
          style={{
            color: accent,
            backgroundColor: `color-mix(in srgb, ${accent} 18%, transparent)`,
          }}
        >
          {icon}
        </span>
        <div className="min-w-0 flex-1 pt-0.5">
          {snackbar.title ? (
            <p className="font-display text-sm font-semibold text-[var(--color-ink)]">
              {snackbar.title}
            </p>
          ) : null}
          <p
            className={`text-sm leading-snug text-[var(--color-muted)] ${snackbar.title ? 'mt-0.5' : ''}`}
          >
            {snackbar.message}
          </p>
        </div>
        <button
          type="button"
          onClick={onDismiss}
          className="shrink-0 rounded-md p-1 text-[var(--color-muted)] transition hover:bg-[var(--color-surface-2)] hover:text-[var(--color-ink)]"
          aria-label="Dismiss"
        >
          <svg viewBox="0 0 20 20" fill="currentColor" className="size-4">
            <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
          </svg>
        </button>
      </div>
      <div
        className="snackbar-progress h-0.5 origin-left"
        style={{ backgroundColor: accent }}
        onAnimationEnd={onDismiss}
      />
    </div>
  )
}

export function SnackbarProvider({ children }: { children: ReactNode }) {
  const [snackbars, setSnackbars] = useState<Snackbar[]>([])

  const dismiss = useCallback((id: string) => {
    setSnackbars((prev) => prev.filter((s) => s.id !== id))
  }, [])

  const showSnackbar = useCallback(
    (message: string, variant: SnackbarVariant = 'info', title?: string) => {
      const id = crypto.randomUUID()
      setSnackbars((prev) => [...prev, { id, message, variant, title }])
      window.setTimeout(() => dismiss(id), AUTO_DISMISS_MS)
    },
    [dismiss],
  )

  const showSuccess = useCallback(
    (message: string, title?: string) => showSnackbar(message, 'success', title),
    [showSnackbar],
  )

  const showError = useCallback(
    (message: string, title?: string) => showSnackbar(message, 'error', title),
    [showSnackbar],
  )

  const value = useMemo(
    () => ({ showSnackbar, showSuccess, showError }),
    [showSnackbar, showSuccess, showError],
  )

  return (
    <SnackbarContext.Provider value={value}>
      {children}
      <div
        aria-live="polite"
        className="pointer-events-none fixed top-4 right-4 z-[100] flex flex-col gap-3"
      >
        {snackbars.map((snackbar) => (
          <SnackbarItem key={snackbar.id} snackbar={snackbar} onDismiss={() => dismiss(snackbar.id)} />
        ))}
      </div>
    </SnackbarContext.Provider>
  )
}

export function useSnackbar() {
  const ctx = useContext(SnackbarContext)
  if (!ctx) throw new Error('useSnackbar must be used within SnackbarProvider')
  return ctx
}
