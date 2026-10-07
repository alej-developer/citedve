import { CLAIM_META, ClaimBadge } from "@/components/ClaimBadge";
import { SignalCard } from "@/components/SignalCard";
import { loadLatest } from "@/lib/data";
import type { ClaimType } from "@radar/schema";

export default function Home() {
  const latest = loadLatest();
  const types = Object.keys(CLAIM_META) as ClaimType[];

  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <p className="font-mono text-xs uppercase tracking-widest text-ink-soft">
        Observatorio abierto · edición semanal
      </p>
      <h1 className="mt-3 font-serif text-5xl leading-tight">Radar Venezuela</h1>
      <p className="mt-4 max-w-prose text-lg text-ink-soft">
        Señales sobre FX, inflación, energía, sanciones, fintech, e-commerce e infraestructura
        digital. Cada cifra con fuente, fecha de captura y enlace.
      </p>

      <section aria-label="Tipos de afirmación" className="mt-10 grid gap-4 sm:grid-cols-3">
        {types.map((type) => (
          <div key={type} className="border-t border-rule pt-3">
            <ClaimBadge type={type} />
            <p className="mt-2 text-sm text-ink-soft">{CLAIM_META[type].hint}</p>
          </div>
        ))}
      </section>

      <section aria-label="Última edición" className="mt-14">
        <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">
          {latest.edition ? `Edición ${latest.edition}` : "Última edición"}
        </h2>
        {latest.signals.length === 0 ? (
          <p className="mt-4 border border-dashed border-rule bg-paper-raised p-6 text-ink-soft">
            Aún no hay ediciones publicadas. No mostramos cifras sin fuente, fecha de captura y
            enlace.
          </p>
        ) : (
          latest.signals.map((signal) => <SignalCard key={signal.id} signal={signal} />)
        )}
      </section>

      <footer className="mt-20 border-t border-rule pt-6 text-sm text-ink-soft">
        Información, no consejo de inversión. Datos de terceros bajo sus propias licencias.
      </footer>
    </main>
  );
}
