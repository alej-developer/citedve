import type { FxP2PPublished } from "@/lib/fxLatest";
import { SINGLE_PUBLISHER, USDT_NOTE, p2pSummary } from "@/lib/fxView";

export function P2PRangeCard({ p2p }: { p2p: FxP2PPublished }) {
  return (
    <section className="mt-10">
      <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">Rango P2P</h2>
      <p className="mt-2 text-sm text-ink-soft">Lado {p2p.side} · unidad {p2p.unit}</p>
      <p className="mt-3 font-serif text-2xl text-ink">{p2pSummary(p2p)}</p>
      <ul className="mt-4 space-y-2 text-sm text-ink-soft">
        {p2p.fuentes.map((source) => (
          <li key={source.url}>
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="underline decoration-rule underline-offset-2 hover:text-ink"
            >
              {source.name}
            </a>
            {source.archive_url ? (
              <>
                {" "}
                ·{" "}
                <a
                  href={source.archive_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="underline decoration-rule underline-offset-2 hover:text-ink"
                >
                  instantánea archivada
                </a>
              </>
            ) : null}
          </li>
        ))}
      </ul>
      {p2p.limitacion_editor_unico ? <p className="mt-3 text-sm text-ink-soft">{SINGLE_PUBLISHER}</p> : null}
      <p className="mt-3 text-sm text-ink-soft">{USDT_NOTE}</p>
    </section>
  );
}
