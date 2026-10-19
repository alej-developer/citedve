import Link from "next/link";

export const metadata = {
  title: "Metodología | CitedVE",
};

export default function Methodology() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header className="mb-12 border-b border-rule pb-6">
        <h1 className="font-serif text-4xl text-ink">Metodología de Captura</h1>
        <p className="mt-2 text-ink-soft">Cómo validamos y clasificamos los datos.</p>
      </header>

      <article className="space-y-8 text-ink-soft leading-relaxed">
        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Principios Fundamentales</h2>
          <p>
            CitedVE no es un generador de opiniones ni un agregador de noticias. 
            Es un repositorio estricto de señales donde <strong>cada dato requiere una cita primaria</strong>. 
            Rechazamos los rumores de redes sociales y priorizamos los documentos oficiales, boletines académicos y reportes financieros verificables.
          </p>
        </section>

        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Niveles de Confianza (Confidence)</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li><strong>Alta (High):</strong> Datos publicados por entidades oficiales (BCV, OFAC) o documentos legales (Gaceta Oficial). No hay ambigüedad sobre la emisión del dato.</li>
            <li><strong>Media (Medium):</strong> Observatorios independientes de prestigio (OVF, ENCOVI) o reportes de agencias internacionales (Reuters, Bloomberg) basados en fuentes directas.</li>
            <li><strong>Baja (Low):</strong> Estimaciones propias del mercado, encuestas de muestras pequeñas o datos filtrados de operadores de la industria con un track record conocido.</li>
          </ul>
        </section>

        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Panel de tasas</h2>
          <p>
            La página de tasas es una foto semanal, no una cotización en vivo. El corte es el viernes.
            La tasa oficial usa la fecha de operación del BCV. Si el corte tiene más de 8 días, la página muestra «desactualizado».
          </p>
          <p className="mt-3">
            Cada fila lleva la URL exacta de su fuente. La lista de bancos es la que publica el BCV ese día y no es exhaustiva.
            La dispersión indica mínimo, máximo y amplitud, sin nombrar qué institución está en cada extremo.
          </p>
          <p className="mt-3">
            El rango P2P se publica con al menos dos mercados de origen distintos. Si el editor es uno solo, la página lo dice.
            USDT no es USD. La brecha se muestra frente al mínimo, al máximo y a la mediana, cada una con su etiqueta.
            La fórmula es (P2P − BCV) / BCV, con la venta del BCV como pata oficial.
          </p>
          <p className="mt-3">
            La captura es manual y citada. No hay ranking ni enlaces de afiliado.
          </p>
        </section>

        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Limitaciones</h2>
          <p>
            Dada la naturaleza del ecosistema de información venezolano, existe un rezago constante en la emisión de indicadores macroeconómicos. 
            Las &quot;brechas cambiarias&quot; representan promedios tomados de ventanas específicas del mercado P2P y no constituyen tasas de ejecución garantizadas.
          </p>
        </section>
      </article>

      <div className="mt-12 border-t border-rule pt-6">
        <Link href="/" className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; Volver al inicio</Link>
      </div>
    </main>
  );
}
