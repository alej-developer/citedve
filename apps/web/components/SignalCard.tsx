import type { Signal } from "@radar/schema";
import { ClaimBadge } from "./ClaimBadge";

function formatValue(signal: Signal): string | null {
  if (signal.range) {
    return `${signal.range.min}–${signal.range.max}${signal.unit ? ` ${signal.unit}` : ""}`;
  }
  if (signal.value !== null && signal.value !== undefined) {
    return `${signal.value}${signal.unit ? ` ${signal.unit}` : ""}`;
  }
  return null;
}

export function SignalCard({ signal }: { signal: Signal }) {
  const value = formatValue(signal);
  return (
    <article className="border-t border-rule py-6">
      <div className="flex flex-wrap items-center gap-3">
        <ClaimBadge type={signal.claim_type} />
        <span className="font-mono text-xs uppercase tracking-wider text-ink-soft">
          {signal.domain.replace("_", " ")}
        </span>
      </div>
      <h3 className="mt-3 font-serif text-xl leading-snug">{signal.title}</h3>
      {value && <p className="mt-1 font-mono text-2xl">{value}</p>}
      <p className="mt-2 max-w-prose text-ink-soft">{signal.statement}</p>
      <ul className="mt-3 space-y-1 text-sm">
        {signal.sources.map((source) => (
          <li key={source.url}>
            <a className="underline decoration-rule underline-offset-4 hover:decoration-ink" href={source.url}>
              {source.name}
            </a>{" "}
            <span className="font-mono text-xs text-ink-soft">captura {source.captured_at}</span>
          </li>
        ))}
      </ul>
    </article>
  );
}
