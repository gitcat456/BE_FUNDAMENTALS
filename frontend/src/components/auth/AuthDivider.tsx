export function AuthDivider({ label = 'or' }: { label?: string }) {
  return (
    <div className="relative my-6">
      <div className="absolute inset-0 flex items-center" aria-hidden>
        <div className="w-full border-t border-[var(--color-border)]" />
      </div>
      <div className="relative flex justify-center">
        <span className="bg-[var(--color-surface)] px-3 text-xs font-medium uppercase tracking-wide text-[var(--color-muted)]">
          {label}
        </span>
      </div>
    </div>
  )
}
