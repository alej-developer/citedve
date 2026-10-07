import { ConfidencePill } from "@/components/ConfidencePill";
import { SignalRow } from "@/components/SignalRow";
import { SourceList } from "@/components/SourceList";
import { WeekNav } from "@/components/WeekNav";
import { FxGapMeter } from "@/components/FxGapMeter";
import { EmptyState } from "@/components/EmptyState";
import type { Signal } from "@radar/schema";

const mockSignal: Signal = {
  id: "mock-1",
  title: "Tasa oficial del BCV alcanza 36,00 Bs/USD",
  category: "fx",
  summary: "El Banco Central de Venezuela reporta una tasa oficial promedio de 36,00 Bs/USD en la primera jornada.",
  value_numeric: 36.0,
  value_text: null,
  unit: "Bs/USD",
  as_of_date: "2024-01-02",
  captured_at: "2024-01-02T16:00:00Z",
  direction: "flat",
  confidence: "high",
  sources: [{ name: "BCV", url: "https://bcv.org.ve", accessed_at: "2024-01-02" }],
  tags: ["bcv"],
  region: "VE",
  notes: null,
  status: "published"
};

const mockSignal2: Signal = {
  ...mockSignal,
  id: "mock-2",
  title: "OVF estima inflación mensual de 3.9%",
  category: "inflation",
  summary: "El observatorio independiente marca un descenso respecto al mes anterior.",
  value_numeric: 3.9,
  unit: "% mensual",
  direction: "down",
  confidence: "medium",
  sources: [{ name: "OVF", url: "https://observatoriodefinanzas.com", accessed_at: "2024-01-02" }]
};

export default function DesignPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16 space-y-16">
      <header>
        <h1 className="font-serif text-4xl mb-2">Sistema Visual</h1>
        <p className="text-ink-soft">Observatorio editorial. Sin gradientes, sin humo.</p>
      </header>

      <section>
        <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft mb-6 border-b border-rule pb-2">Señales (SignalRow)</h2>
        <div className="flex flex-col">
          <SignalRow signal={mockSignal} />
          <SignalRow signal={mockSignal2} />
        </div>
      </section>

      <section>
        <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft mb-6 border-b border-rule pb-2">Componentes Atómicos</h2>
        <div className="space-y-6">
          <div>
            <h3 className="text-sm font-medium mb-3">ConfidencePill</h3>
            <div className="flex gap-4">
              <ConfidencePill level="high" />
              <ConfidencePill level="medium" />
              <ConfidencePill level="low" />
            </div>
          </div>
          <div>
            <h3 className="text-sm font-medium mb-3">SourceList</h3>
            <SourceList sources={mockSignal.sources} />
          </div>
          <div>
            <h3 className="text-sm font-medium mb-3">FxGapMeter</h3>
            <div className="max-w-md">
              <FxGapMeter official={36.0} parallel={39.5} />
            </div>
          </div>
        </div>
      </section>

      <section>
        <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft mb-6 border-b border-rule pb-2">Navegación & Estados</h2>
        <div className="space-y-8">
          <WeekNav current="Semana 2026-10-05" prev="2026-09-28" next="2026-10-12" />
          <EmptyState />
        </div>
      </section>
    </main>
  );
}
