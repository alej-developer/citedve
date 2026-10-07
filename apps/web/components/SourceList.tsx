import type { Source } from "@radar/schema";

export function SourceList({ sources }: { sources: Source[] }) {
  if (sources.length === 0) return null;
  return (
    <ul className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-ink-soft">
      {sources.map((s, i) => (
        <li key={i} className="flex items-center gap-1">
          <span className="w-1 h-1 rounded-full bg-rule"></span>
          {s.url ? (
            <a href={s.url} target="_blank" rel="noopener noreferrer" className="hover:text-ink underline decoration-rule underline-offset-2 micro-hover">
              {s.name}
            </a>
          ) : (
            <span>{s.name}</span>
          )}
        </li>
      ))}
    </ul>
  );
}
