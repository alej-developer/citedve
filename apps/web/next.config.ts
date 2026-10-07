import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // MVP: sitio 100 % estático + JSON versionado (ver docs/ARCHITECTURE.md).
  output: "export",
  transpilePackages: ["@radar/schema"],
};

export default nextConfig;
