export const metadata = {
  title: "Acerca de | Radar Venezuela",
};

export default function About() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header className="mb-12 border-b border-rule pb-6">
        <h1 className="font-serif text-4xl text-ink">Acerca del Proyecto</h1>
      </header>

      <article className="space-y-8 text-ink-soft leading-relaxed">
        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Motivación</h2>
          <p>
            Radar Venezuela nace ante la necesidad de la diáspora, inversores y operadores locales de contar con un resumen semanal <strong>citado y auditable</strong>, lejos del ruido y la opinión disfrazada de dato.
            El proyecto demuestra capacidades en diseño de productos de datos, ingeniería full-stack y curaduría institucional.
          </p>
        </section>

        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Licencia</h2>
          <p>
            El código fuente de este portal se distribuye bajo <strong>Apache-2.0</strong>. <br/>
            Los datos y el contenido editorial propio se publican bajo <strong>CC BY 4.0</strong>, permitiendo su libre reutilización siempre que se cite la fuente original.
          </p>
        </section>

        <section>
          <h2 className="font-serif text-2xl text-ink mb-3">Contacto & Contribuciones</h2>
          <p>
            Todo el código y los datos están abiertos en GitHub. Las contribuciones son procesadas exclusivamente mediante Pull Requests para garantizar la inmutabilidad de la cadena de datos ("Git as Database").
          </p>
          <a href="https://github.com/alej-developer/radar-venezuela" className="mt-4 inline-block px-4 py-2 bg-ink text-paper text-sm font-medium micro-hover" target="_blank" rel="noopener noreferrer">
            Ver Repositorio en GitHub
          </a>
        </section>
      </article>

      <div className="mt-12 border-t border-rule pt-6">
        <a href="/" className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; Volver al inicio</a>
      </div>
    </main>
  );
}
