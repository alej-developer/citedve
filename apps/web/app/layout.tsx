import type { Metadata } from "next";
import { Newsreader, IBM_Plex_Sans } from "next/font/google";
import "./globals.css";

const serifFont = Newsreader({
  subsets: ["latin"],
  variable: "--font-serif-main",
  display: "swap",
});

const sansFont = IBM_Plex_Sans({
  weight: ["400", "500", "600"],
  subsets: ["latin"],
  variable: "--font-sans-main",
  display: "swap",
});

export const metadata: Metadata = {
  title: "CitedVE — señales citadas sobre Venezuela, open source",
  description:
    "Señales citadas sobre Venezuela, open source. Cada cifra con fuente, fecha de captura y enlace.",
  openGraph: {
    title: "CitedVE",
    description: "Señales citadas sobre Venezuela, open source. Cada cifra incluye fuente primaria, fecha de captura y enlace.",
    url: "https://citedve.vercel.app",
    siteName: "CitedVE",
    locale: "es_VE",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "CitedVE",
    description: "Señales citadas sobre Venezuela, open source. Cada cifra incluye fuente primaria, fecha de captura y enlace.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es" className={`${serifFont.variable} ${sansFont.variable}`}>
      <body className="min-h-screen font-sans bg-paper text-ink selection:bg-ink selection:text-paper">
        {children}
      </body>
    </html>
  );
}
