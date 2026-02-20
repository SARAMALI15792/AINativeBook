/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove static export for Vercel serverless deployment
  // output: 'export', // REMOVED - enables server-side features
  // basePath: '/AINativeBook', // REMOVED - deploy to root domain
  images: {
    // Enable image optimization on Vercel
    unoptimized: false,
    domains: ['vercel.app', 'localhost'],
  },
  reactStrictMode: true,

  // Performance optimizations
  swcMinify: true,
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  env: {
    NEXT_PUBLIC_AUTH_URL: process.env.NEXT_PUBLIC_AUTH_URL,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_DOCUSAURUS_URL: process.env.NEXT_PUBLIC_DOCUSAURUS_URL,
  },

  // Vercel-specific configuration
  async rewrites() {
    return [
      {
        source: '/api/auth/:path*',
        destination: '/api/auth/:path*', // Handled by auth-server
      },
      {
        source: '/api/v1/:path*',
        destination: '/api/v1/:path*', // Handled by backend
      },
    ];
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
    // optimizeCss: true, // Disabled - requires critters package
    optimizePackageImports: ['framer-motion', '@react-three/fiber', '@react-three/drei'],
  },
};

module.exports = nextConfig;
