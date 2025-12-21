import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    unoptimized: true, // Optimized for 1GB Server: Saves RAM & fixes 'private ip' error
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
      },
    ],
  },
  // reactCompiler: true, // Commenting out experimental feature if causing issues, or leave it if works
  experimental: {
    // reactCompiler: true, // Usually it's in experimental
  },
};

export default nextConfig;
