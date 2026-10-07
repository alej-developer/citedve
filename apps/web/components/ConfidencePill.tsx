export function ConfidencePill({ level }: { level: 'high' | 'medium' | 'low' }) {
  const map = {
    high: { label: "Alta", className: "bg-paper-raised border-rule text-ink" },
    medium: { label: "Media", className: "bg-paper border-rule text-ink-soft opacity-80" },
    low: { label: "Baja", className: "bg-paper border-rule text-ink-soft border-dashed" }
  };
  const { label, className } = map[level];
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] uppercase tracking-wider border ${className}`}>
      {label}
    </span>
  );
}
