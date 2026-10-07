export function FxGapMeter({ official, parallel }: { official: number, parallel: number }) {
  const gap = ((parallel - official) / official) * 100;
  const gapFormatted = gap.toFixed(1) + "%";
  
  return (
    <div className="flex items-center gap-4 py-3 border-y border-rule">
      <div className="flex-1">
        <div className="flex justify-between text-xs font-mono uppercase tracking-widest text-ink-soft mb-1">
          <span>BCV ({official})</span>
          <span>P2P ({parallel})</span>
        </div>
        <svg className="w-full h-2 rounded-full overflow-hidden" preserveAspectRatio="none">
          <rect width="100%" height="100%" fill="var(--color-paper-raised)" />
          {/* Base BCV line */}
          <rect width="50%" height="100%" fill="var(--color-flat)" />
          {/* Gap line */}
          <rect x="50%" width="50%" height="100%" fill="var(--color-down)" opacity="0.8" />
        </svg>
      </div>
      <div className="w-16 text-right">
        <span className="block font-mono text-xs text-ink-soft uppercase">Brecha</span>
        <span className="font-semibold text-down tabular-data">{gapFormatted}</span>
      </div>
    </div>
  );
}
