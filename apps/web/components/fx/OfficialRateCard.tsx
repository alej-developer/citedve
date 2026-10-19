import type { FxCell } from "@/lib/fxLatest";
import { operationDate, sideText } from "@/lib/fxView";

export function OfficialRateCard({
  official,
}: {
  official: { compra: FxCell | null; venta: FxCell | null };
}) {
  const fecha = operationDate(official.venta) ?? operationDate(official.compra);
  const source = official.venta?.source ?? official.compra?.source;

  return (
    <section className="mt-10">
      <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">Tasa oficial BCV</h2>
      <p className="mt-2 text-sm text-ink-soft">Unidad: VES/USD</p>
      <dl className="mt-4 grid grid-cols-2 gap-4 border-y border-rule py-4">
        <div>
          <dt className="font-mono text-xs uppercase tracking-widest text-ink-soft">Compra</dt>
          <dd className="mt-1 font-serif text-2xl text-ink">{sideText(official.compra)}</dd>
        </div>
        <div>
          <dt className="font-mono text-xs uppercase tracking-widest text-ink-soft">Venta</dt>
          <dd className="mt-1 font-serif text-2xl text-ink">{sideText(official.venta)}</dd>
        </div>
      </dl>
      {fecha ? <p className="mt-3 text-sm text-ink-soft">Fecha de operación: {fecha}</p> : null}
      {source ? (
        <p className="mt-2 text-sm text-ink-soft">
          Fuente:{" "}
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="underline decoration-rule underline-offset-2 hover:text-ink"
          >
            {source.name}
          </a>
          {source.locator ? <span> · {source.locator}</span> : null}
        </p>
      ) : null}
    </section>
  );
}
