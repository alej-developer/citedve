import Link from "next/link";

import { EmptyState } from "@/components/EmptyState";
import { FxGapMeter } from "@/components/FxGapMeter";
import { BankRateTable } from "@/components/fx/BankRateTable";
import { OfficialRateCard } from "@/components/fx/OfficialRateCard";
import { P2PRangeCard } from "@/components/fx/P2PRangeCard";
import { StaleBanner } from "@/components/fx/StaleBanner";
import { loadFxLatest } from "@/lib/fxLatest";
import { GAP_FORMULA, GAP_UNAVAILABLE, P2P_EMPTY, dispersionLine } from "@/lib/fxView";

export const metadata = {
  title: "Tasas | CitedVE",
};

const SOURCES_URL = "https://github.com/alej-developer/citedve/blob/main/docs/SOURCES.md";

export default function FxPage() {
  const latest = loadFxLatest();
  const edition = latest.edition;

  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header>
        <p className="font-mono text-xs uppercase tracking-widest text-ink-soft">Panel de tasas</p>
        <h1 className="mt-3 font-serif text-4xl text-ink">Tasas por banco y brecha</h1>
        {edition ? (
          <p className="mt-4 text-ink">Fecha de corte: {edition.cutoff_date}</p>
        ) : null}
        <p className="mt-3 max-w-prose text-ink-soft">{latest.notice}</p>
        {edition ? <StaleBanner cutoff={edition.cutoff_date} maxDays={latest.freshness_max_days} /> : null}
        {latest.retracted_banner ? (
          <p className="mt-4 border border-rule px-3 py-2 text-sm text-ink-soft">{latest.retracted_banner}</p>
        ) : null}
      </header>

      {!edition ? (
        <div className="mt-10">
          <EmptyState />
        </div>
      ) : (
        <>
          {latest.official ? <OfficialRateCard official={latest.official} /> : null}
          <BankRateTable rows={latest.banks ?? []} />
          {latest.dispersion ? (
            <section className="mt-8">
              <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">
                Dispersión entre bancos
              </h2>
              <p className="mt-3 text-sm text-ink">{dispersionLine("Compra", latest.dispersion.compra)}</p>
              <p className="mt-1 text-sm text-ink">{dispersionLine("Venta", latest.dispersion.venta)}</p>
            </section>
          ) : null}
          {latest.p2p?.estado === "publicado" ? (
            <P2PRangeCard p2p={latest.p2p} />
          ) : (
            <div className="mt-10">
              <EmptyState message={P2P_EMPTY} />
            </div>
          )}
          <section className="mt-10">
            <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">Brecha</h2>
            <p className="mt-3 text-sm text-ink-soft">Fórmula: {GAP_FORMULA}.</p>
            {latest.p2p?.estado === "publicado" && latest.gaps ? (
              latest.gaps.map((gap) => (
                <div key={gap.label} className="mt-4">
                  <p className="text-sm text-ink">
                    {gap.label} frente a la venta BCV. Lado P2P: {gap.side}.
                  </p>
                  <FxGapMeter
                    official={gap.official}
                    parallel={gap.parallel}
                    officialLabel={gap.official_label}
                    parallelLabel={gap.parallel_label}
                  />
                </div>
              ))
            ) : (
              <p className="mt-3 text-sm text-ink-soft">{GAP_UNAVAILABLE}</p>
            )}
          </section>
        </>
      )}

      <footer className="mt-16 border-t border-rule pt-6 text-sm text-ink-soft">
        <p>
          <Link href="/methodology" className="underline decoration-rule underline-offset-2 hover:text-ink">
            Metodología
          </Link>
          {" · "}
          <a
            href={SOURCES_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="underline decoration-rule underline-offset-2 hover:text-ink"
          >
            Fuentes
          </a>
          {" · "}
          <Link href="/" className="underline decoration-rule underline-offset-2 hover:text-ink">
            Inicio
          </Link>
        </p>
      </footer>
    </main>
  );
}
