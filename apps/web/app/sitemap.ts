import { MetadataRoute } from 'next';
import { getRadarPosts, loadAllSignals } from '@/lib/data';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = "https://radarvenezuela.org";

  // Static routes
  const staticRoutes = [
    { url: `${baseUrl}`, lastModified: new Date() },
    { url: `${baseUrl}/radar`, lastModified: new Date() },
    { url: `${baseUrl}/signals`, lastModified: new Date() },
    { url: `${baseUrl}/methodology`, lastModified: new Date() },
    { url: `${baseUrl}/about`, lastModified: new Date() },
  ];

  // Dynamic radar posts
  const posts = getRadarPosts();
  const postRoutes = posts.map((post) => ({
    url: `${baseUrl}/radar/${post.slug}`,
    lastModified: new Date(),
  }));

  // Dynamic signals
  const signals = loadAllSignals();
  const signalRoutes = signals.map((signal) => ({
    url: `${baseUrl}/signals/${signal.id}`,
    lastModified: new Date(signal.captured_at),
  }));

  return [...staticRoutes, ...postRoutes, ...signalRoutes];
}
