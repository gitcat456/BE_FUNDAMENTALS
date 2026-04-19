type Props = {
  label: string
  value: string | number
  hint?: string
}

export function StatCard({ label, value, hint }: Props) {
  return (
    <div className="rounded-2xl border border-[var(--color-border)] bg-[var(--color-surface)]/90 p-5 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-wider text-[var(--color-muted)]">
        {label}
      </p>
      <p className="mt-2 font-display text-3xl font-semibold text-[var(--color-accent)]">{value}</p>
      {hint ? <p className="mt-2 text-xs text-[var(--color-muted)]">{hint}</p> : null}
    </div>
  )
}
