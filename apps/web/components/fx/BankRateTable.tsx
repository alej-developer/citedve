import type { FxBankRow, FxCell } from "@/lib/fxLatest";
import { AGGREGATE_NOTE, BANK_FOOTNOTE, SOURCE_DISCREPANCY, sideText } from "@/lib/fxView";

export function BankRateTable({ rows }: { rows: FxBankRow[] }) {
  return (
    <section className="mt-10">
      <h2 className="font-mono text-xs uppercase tracking-widest text-ink-soft">Tasas por institución</h2>
      <table className="mt-4 w-full text-left text-sm">
        <thead>
          <tr className="border-b border-rule font-mono text-xs uppercase tracking-widest text-ink-soft">
            <th className="py-2 pr-3 font-normal">Institución</th>
            <th className="py-2 pr-3 font-normal">Compra</th>
            <th className="py-2 pr-3 font-normal">Venta</th>
            <th className="py-2 pr-3 font-normal">Fecha del dato</th>
            <th className="py-2 font-normal">Fuente</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.institution.id} className="border-b border-rule align-top">
              <td className="py-3 pr-3 text-ink">
                {row.institution.name}
                {row.institution.kind === "agregado_fuente" ? (
                  <span className="mt-1 block text-xs text-ink-soft">{AGGREGATE_NOTE}</span>
                ) : null}
                {row.discrepancia ? (
                  <span className="mt-1 block text-xs text-ink-soft">{SOURCE_DISCREPANCY}</span>
                ) : null}
              </td>
              <td className="py-3 pr-3 text-ink">{sideText(row.compra)}</td>
              <td className="py-3 pr-3 text-ink">{sideText(row.venta)}</td>
              <td className="py-3 pr-3 text-ink-soft">{dated(row)}</td>
              <td className="py-3 text-ink-soft">{sourceLinks(row)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-3 text-sm text-ink-soft">{BANK_FOOTNOTE}</p>
    </section>
  );
}

function dated(row: FxBankRow): string {
  const compra = row.compra?.as_of_date;
  const venta = row.venta?.as_of_date;
  if (compra && venta && compra !== venta) return `compra ${compra} · venta ${venta}`;
  return compra ?? venta ?? "—";
}

function sourceLinks(row: FxBankRow) {
  const cells = [row.compra, row.venta].filter((cell): cell is FxCell => cell != null);
  const seen = new Set<string>();
  const links = cells.filter((cell) => {
    if (seen.has(cell.source.url)) return false;
    seen.add(cell.source.url);
    return true;
  });
  return links.map((cell) => (
    <a
      key={cell.source.url}
      href={cell.source.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block underline decoration-rule underline-offset-2 hover:text-ink"
    >
      {cell.source.name}
    </a>
  ));
}
