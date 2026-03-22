/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Performance optimizations
  swcMinify: true,
  compiler: {
    removeConsole: false, // Keep console.error for debugging
  },

  env: {
    // Production URLs are hardcoded as fallbacks (all are public, non-secret URLs).
    // Override via environment variables in local dev.
    NEXT_PUBLIC_AUTH_URL: process.env.NEXT_PUBLIC_AUTH_URL || 'https://intellistack-auth-production.up.railway.app',
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://intellistack-backend-production.up.railway.app/api/v1',
    NEXT_PUBLIC_DOCUSAURUS_URL: process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'https://saramali15792.github.io/AINativeBook/',
  },

  webpack: (config, { isServer }) => {
    // GLTF/GLB support
    config.module.rules.push({
      test: /\.(glb|gltf)$/,
      type: 'asset/resource',
    });

    // Bundle analyzer (run with ANALYZE=true npm run build)
    if (process.env.ANALYZE === 'true') {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: isServer
            ? '../analyze/server.html'
            : './analyze/client.html',
          openAnalyzer: false,
        })
      );
    }

    return config;
  },

  // Experimental features for better performance
  experimental: {
    optimizePackageImports: ['framer-motion', '@react-three/fiber', '@react-three/drei'],
  },
};

module.exports = nextConfig;
