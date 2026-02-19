import type { Metadata, Viewport } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import '@/styles/animations.css';
import { Providers } from './providers';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
  display: 'swap', // FOIT with swap after 3s timeout
  preload: true,
  fallback: ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
});

export const metadata: Metadata = {
  title: 'IntelliStack - Master Physical AI & Humanoid Robotics',
  description: 'Learn robotics with AI-powered tutoring, interactive simulations, and hands-on projects. From ROS 2 fundamentals to advanced perception and planning.',
  keywords: ['robotics', 'AI', 'ROS 2', 'humanoid robotics', 'machine learning', 'computer vision', 'autonomous systems', 'physical AI'],
  authors: [{ name: 'IntelliStack' }],
  creator: 'IntelliStack',
  publisher: 'IntelliStack',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://intellistack.com',
    title: 'IntelliStack - Master Physical AI & Humanoid Robotics',
    description: 'Learn robotics with AI-powered tutoring, interactive simulations, and hands-on projects.',
    siteName: 'IntelliStack',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'IntelliStack - Master Physical AI & Humanoid Robotics',
    description: 'Learn robotics with AI-powered tutoring, interactive simulations, and hands-on projects.',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        {/* Resource hints for performance */}
        <link rel="preconnect" href={process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3001'} />
        <link rel="preconnect" href={process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'} />
        <link rel="dns-prefetch" href={process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'} />

      </head>
      <body className={inter.variable}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
