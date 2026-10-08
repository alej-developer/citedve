import Link from "next/link";
import { getRadarPost, getRadarPosts } from "@/lib/data";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { WeekNav } from "@/components/WeekNav";

export async function generateStaticParams() {
  const posts = getRadarPosts();
  return posts.map((post) => ({
    date: post.slug,
  }));
}

export default async function RadarPostPage({ params }: { params: Promise<{ date: string }> }) {
  const { date } = await params;
  const post = getRadarPost(date);

  if (!post) {
    notFound();
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <div className="mb-12">
        <WeekNav current={`Semana ${post.edition}`} prev={post.edition} />
      </div>

      <article className="prose prose-p:font-sans prose-headings:font-serif prose-a:text-ink prose-a:decoration-rule hover:prose-a:decoration-ink prose-a:underline-offset-2 prose-hr:border-rule prose-blockquote:border-l-4 prose-blockquote:border-ink prose-blockquote:bg-paper-raised prose-blockquote:px-4 prose-blockquote:py-1 max-w-none">
        <ReactMarkdown>{post.content}</ReactMarkdown>
      </article>
      
      <div className="mt-16 border-t border-rule pt-6">
        <Link href="/radar" className="text-sm font-mono hover:text-ink text-ink-soft micro-hover">&larr; Volver al archivo</Link>
      </div>
    </main>
  );
}
