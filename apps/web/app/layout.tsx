import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Radar Venezuela — señales semanales citadas",
  description:
    "Radar semanal de señales sobre Venezuela (FX, inflación, energía, sanciones, fintech, e-commerce, infraestructura digital). Cada cifra con fuente, fecha de captura y enlace.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="es">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
