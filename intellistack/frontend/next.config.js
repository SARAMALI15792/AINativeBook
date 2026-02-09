/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Disable SWC to use Babel instead (for Windows compatibility)
  experimental: {
    swcPlugins: [],
  },
  // Explicitly disable SWC minification
  swcMinify: false,

  // API rewrites to backend
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL
          ? `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`
          : 'http://localhost:8000/api/:path*',
      },
    ];
  },

  // Image domains for external images
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.githubusercontent.com',
      },
    ],
  },
};

module.exports = nextConfig;
