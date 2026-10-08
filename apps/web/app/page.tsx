import Link from "next/link";
import { SignalRow } from "@/components/SignalRow";
import { EmptyState } from "@/components/EmptyState";
import { WeekNav } from "@/components/WeekNav";
import { FxGapMeter } from "@/components/FxGapMeter";
import { loadLatest } from "@/lib/data";

export default function Home() {
  const latest = loadLatest();
  const editionDate = latest.edition || "Sin publicar";
  
  // Extract FX signals for the FxGapMeter
  const bcvSignal = latest.signals.find(s => s.tags?.includes("bcv"));
  const parallelSignal = latest.signals.find(s => s.tags?.includes("parallel"));
  
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header>
        <p className="font-mono text-xs uppercase tracking-widest text-ink-soft">
          Observatorio abierto · edición semanal
        </p>
        <h1 className="mt-3 font-serif text-5xl leading-tight text-ink">CitedVE</h1>
        <p className="mt-4 max-w-prose text-lg text-ink-soft leading-relaxed">
          Señales sobre FX, inflación, energía, sanciones, fintech, e-commerce e infraestructura digital. 
          Cada cifra publicada incluye su fuente primaria verificable, fecha de captura y enlace.
        </p>
        <div className="mt-6 flex gap-4">
          <a href="/methodology" className="px-4 py-2 bg-ink text-paper text-sm font-medium micro-hover">Ver metodología</a>
          <a href="https://github.com/alej-developer/citedve/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer" className="px-4 py-2 border border-rule text-ink text-sm font-medium micro-hover">Contribuir</a>
        </div>
      </header>

      <div className="mt-12">
        <WeekNav current={`Semana ${editionDate}`} prev={editionDate} />
      </div>

      {(bcvSignal && parallelSignal && bcvSignal.value_numeric && parallelSignal.value_numeric) ? (
        <section className="mt-8 mb-12">
          <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft mb-2">Monitor FX</h2>
          <FxGapMeter official={bcvSignal.value_numeric} parallel={parallelSignal.value_numeric} />
        </section>
      ) : null}

      <section aria-label="Última edición" className="mt-12">
        <div className="flex justify-between items-end border-b border-rule pb-2 mb-4">
          <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">
            Top Señales ({editionDate})
          </h2>
          <Link href="/signals" className="text-sm underline decoration-rule underline-offset-2 hover:text-ink text-ink-soft">Ver todas</Link>
        </div>
        
        {latest.signals.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="flex flex-col">
            {latest.signals.slice(0, 8).map((signal) => (
              <SignalRow key={signal.id} signal={signal} />
            ))}
          </div>
        )}
      </section>

      <footer className="mt-20 border-t border-rule pt-6 pb-12 flex justify-between text-sm text-ink-soft">
        <span>Información factual, no consejo de inversión.</span>
        <div className="space-x-4">
          <a href="/about" className="hover:text-ink">Acerca de</a>
          <Link href="/radar" className="hover:text-ink">Archivo</Link>
        </div>
      </footer>
    </main>
  );
}
