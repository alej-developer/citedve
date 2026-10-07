import { ConfidencePill } from "./ConfidencePill";
import { SourceList } from "./SourceList";
import type { Signal } from "@radar/schema";

export function SignalRow({ signal }: { signal: Signal }) {
  const isUp = signal.direction === 'up';
  const isDown = signal.direction === 'down';
  
  return (
    <article className="group flex flex-col sm:flex-row gap-4 py-4 border-b border-rule last:border-0">
      <div className="sm:w-32 flex-shrink-0 pt-1">
        <span className="font-mono text-xs text-ink-soft tabular-data">{signal.as_of_date}</span>
      </div>
      <div className="flex-1">
        <div className="flex items-start justify-between gap-4">
          <h3 className="font-serif text-lg leading-snug text-ink">{signal.title}</h3>
          {(signal.value_numeric !== null || signal.value_text) && (
            <div className={`text-right tabular-data ${isUp ? 'text-up' : isDown ? 'text-down' : 'text-ink-soft'}`}>
              <span className="font-semibold text-lg">{signal.value_numeric ?? signal.value_text}</span>
              {signal.unit && <span className="text-xs ml-1 font-mono uppercase opacity-80">{signal.unit}</span>}
            </div>
          )}
        </div>
        <p className="mt-1 text-sm text-ink-soft leading-relaxed max-w-prose">
          {signal.summary}
        </p>
        <div className="mt-3 flex items-center gap-4">
          <ConfidencePill level={signal.confidence} />
          <SourceList sources={signal.sources} />
        </div>
      </div>
    </article>
  );
}
