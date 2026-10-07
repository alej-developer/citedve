import { getSignalById, loadAllSignals } from "@/lib/data";
import { notFound } from "next/navigation";
import { ConfidencePill } from "@/components/ConfidencePill";
import { SourceList } from "@/components/SourceList";

export async function generateStaticParams() {
  const signals = loadAllSignals();
  return signals.map((s) => ({
    id: s.id,
  }));
}

export default async function SignalDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const signal = getSignalById(id);

  if (!signal) {
    notFound();
  }

  const isUp = signal.direction === 'up';
  const isDown = signal.direction === 'down';

  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header className="mb-8 border-b border-rule pb-6">
        <div className="flex justify-between items-start mb-4">
          <span className="font-mono text-xs uppercase tracking-widest text-ink-soft">{signal.category}</span>
          <ConfidencePill level={signal.confidence} />
        </div>
        <h1 className="font-serif text-3xl sm:text-4xl text-ink leading-tight">{signal.title}</h1>
        
        {(signal.value_numeric !== null || signal.value_text) && (
          <div className={`mt-6 tabular-data text-2xl ${isUp ? 'text-up' : isDown ? 'text-down' : 'text-ink-soft'}`}>
            <span className="font-semibold">{signal.value_numeric ?? signal.value_text}</span>
            {signal.unit && <span className="ml-2 font-mono text-base uppercase opacity-80">{signal.unit}</span>}
          </div>
        )}
      </header>

      <section className="space-y-6 text-ink-soft leading-relaxed">
        <p className="text-lg">{signal.summary}</p>
        
        {signal.notes && (
          <div className="bg-paper-raised p-4 border-l-2 border-rule">
            <h3 className="font-mono text-xs uppercase tracking-widest text-ink mb-2">Notas Adicionales</h3>
            <p className="text-sm">{signal.notes}</p>
          </div>
        )}

        <div>
          <h3 className="font-mono text-xs uppercase tracking-widest text-ink mb-2 border-b border-rule pb-1">Fuentes & Citas</h3>
          <div className="mt-3">
            <SourceList sources={signal.sources} />
          </div>
        </div>

        <div className="mt-12 p-4 border border-dashed border-rule bg-paper-raised">
          <h3 className="font-mono text-xs uppercase tracking-widest text-ink mb-2">Cómo Citar Esta Señal</h3>
          <code className="text-xs font-mono block break-all text-ink-soft select-all">
            CitedVE ({signal.as_of_date.substring(0,4)}). {signal.title}. Capturado el {new Date(signal.captured_at).toLocaleDateString("es-ES")}. URL: https://citedve.vercel.app/signals/{signal.id}
          </code>
        </div>
      </section>

      <div className="mt-12 border-t border-rule pt-6">
        <a href="/signals" className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; Volver al explorador</a>
      </div>
    </main>
  );
}
