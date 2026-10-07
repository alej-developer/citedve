import { loadAllSignals } from "@/lib/data";
import { SignalRow } from "@/components/SignalRow";
import { EmptyState } from "@/components/EmptyState";

export const metadata = {
  title: "Explorador de Señales | CitedVE",
};

export default function SignalsExplorer() {
  const signals = loadAllSignals();

  // En el futuro, los filtros interactivos se manejan con query params y useSearchParams
  // Por ahora mostramos todas (o las últimas 100) en el renderizado estático.
  const displaySignals = signals.slice(0, 100);

  return (
    <main className="mx-auto max-w-4xl px-6 py-16">
      <header className="mb-12 border-b border-rule pb-6 flex justify-between items-end">
        <div>
          <h1 className="font-serif text-4xl text-ink">Explorador de Señales</h1>
          <p className="mt-2 text-ink-soft">Registro histórico y auditable de todos los datos capturados.</p>
        </div>
        <div className="text-right font-mono text-sm text-ink-soft tabular-data">
          {signals.length} total
        </div>
      </header>

      {displaySignals.length === 0 ? (
        <EmptyState message="No hay señales en el archivo." />
      ) : (
        <div className="flex flex-col">
          {displaySignals.map((signal) => (
            <SignalRow key={signal.id} signal={signal} />
          ))}
        </div>
      )}
      
      <div className="mt-12">
        <a href="/" className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; Volver al inicio</a>
      </div>
    </main>
  );
}
