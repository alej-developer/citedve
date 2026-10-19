import { computeFxGap } from "@/lib/fxGap";

export function FxGapMeter({
  official,
  parallel,
  officialLabel = "BCV",
  parallelLabel = "P2P",
}: {
  official: number;
  parallel: number;
  officialLabel?: string;
  parallelLabel?: string;
}) {
  const gap = computeFxGap(official, parallel);

  return (
    <div className="flex items-center gap-4 py-3 border-y border-rule">
      <div className="flex-1">
        <div className="flex justify-between text-xs font-mono uppercase tracking-widest text-ink-soft mb-1">
          <span>
            {officialLabel} ({official})
          </span>
          <span>
            {parallelLabel} ({parallel})
          </span>
        </div>
        <svg
          className="w-full h-2 rounded-full overflow-hidden"
          preserveAspectRatio="none"
          role="img"
          aria-label={`Brecha ${gap.label} entre ${officialLabel} ${official} y ${parallelLabel} ${parallel}`}
        >
          <rect width="100%" height="100%" fill="var(--color-paper-raised)" />
          <rect width={gap.baseWidth} height="100%" fill="var(--color-flat)" />
          <rect x={gap.gapX} width={gap.gapWidth} height="100%" fill="var(--color-down)" opacity="0.8" />
        </svg>
      </div>
      <div className="w-16 text-right">
        <span className="block font-mono text-xs text-ink-soft uppercase">Brecha</span>
        <span className="font-semibold text-down tabular-data">{gap.label}</span>
      </div>
    </div>
  );
}
