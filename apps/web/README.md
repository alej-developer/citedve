# web

Next.js (App Router) + TypeScript estricto + Tailwind 4, exportado como sitio estático.
Lee `data/latest.json` en tiempo de build.

```bash
npm install          # desde la raíz del monorepo
npm run web:dev      # http://localhost:3000
npm run web:lint && npm run web:typecheck && npm run web:build
```

Esta versión de Next.js tiene convenciones propias: `AGENTS.md` pide consultar `node_modules/next/dist/docs/`
antes de cambiar la estructura del framework.
