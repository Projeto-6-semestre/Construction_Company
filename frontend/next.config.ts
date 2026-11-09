import type { NextConfig } from "next";

// Configuracao do Next.js (framework do front-end). Liga recursos experimentais
// de performance (cache de componentes e prefetch parcial de rotas).
const nextConfig: NextConfig = {
  /* config options here */
  cacheComponents: true,
  partialPrefetching: true,
};

export default nextConfig;
