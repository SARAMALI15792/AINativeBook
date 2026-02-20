import React from 'react';
import Link from 'next/link';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export const metadata = {
  title: 'Dashboard - IntelliStack',
  description: 'Your learning dashboard',
};

export default function DashboardPage() {
  return (
    <main className="relative min-h-screen">
      <Header />

      <div className="container mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold text-text-primary mb-8">
          Your Learning Dashboard
        </h1>

        <div className="glass backdrop-blur-md rounded-2xl p-8 border border-glass-border">
          <p className="text-text-secondary mb-6">
            Welcome to your learning dashboard. Start your journey with Stage 1.
          </p>

          <Link
            href={`${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/stage-1/intro`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-6 py-3 bg-gradient-to-r from-accent-cyan to-accent-violet rounded-lg text-white font-semibold hover:shadow-glow-cyan transition-all"
          >
            Start Stage 1: Foundations
          </Link>
        </div>
      </div>

      <Footer />
    </main>
  );
}
