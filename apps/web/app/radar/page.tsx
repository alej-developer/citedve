import { getRadarPosts } from "@/lib/data";
import { EmptyState } from "@/components/EmptyState";

export const metadata = {
  title: "Archivo | Radar Venezuela",
};

export default function RadarArchive() {
  const posts = getRadarPosts();

  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <header className="mb-12 border-b border-rule pb-6">
        <h1 className="font-serif text-4xl text-ink">Archivo del Radar</h1>
        <p className="mt-2 text-ink-soft">Resúmenes semanales históricos.</p>
      </header>

      {posts.length === 0 ? (
        <EmptyState message="Aún no hay informes publicados." />
      ) : (
        <ul className="space-y-4">
          {posts.map((post) => (
            <li key={post.slug} className="group">
              <a href={`/radar/${post.slug}`} className="flex justify-between items-center py-3 border-b border-dashed border-rule micro-hover">
                <span className="font-serif text-lg">{post.title}</span>
                <span className="font-mono text-sm text-ink-soft tabular-data">{post.edition}</span>
              </a>
            </li>
          ))}
        </ul>
      )}
      
      <div className="mt-12">
        <a href="/" className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; Volver al inicio</a>
      </div>
    </main>
  );
}
