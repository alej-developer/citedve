export function WeekNav({ current, prev, next }: { current: string; prev?: string; next?: string }) {
  return (
    <nav className="flex items-center justify-between py-6 border-b border-rule">
      {prev ? (
        <a href={`/radar/${prev}`} className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; {prev}</a>
      ) : <span className="w-20" />}
      
      <span className="font-serif text-lg font-medium">{current}</span>
      
      {next ? (
        <a href={`/radar/${next}`} className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">{next} &rarr;</a>
      ) : <span className="w-20" />}
    </nav>
  );
}
