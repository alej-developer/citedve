"use client";

import { useSyncExternalStore } from "react";

import { isStale } from "@/lib/fxFreshness";

function subscribe(): () => void {
  return () => {};
}

export function StaleBanner({ cutoff, maxDays = 8 }: { cutoff: string; maxDays?: number }) {
  const stale = useSyncExternalStore(
    subscribe,
    () => isStale(cutoff, new Date().toISOString().slice(0, 10), maxDays),
    () => false,
  );

  if (!stale) return null;

  return (
    <p role="status" className="mt-4 border border-rule px-3 py-2 text-sm text-ink-soft">
      Desactualizado: último corte {cutoff}.
    </p>
  );
}
