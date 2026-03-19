'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui';
import { NeuralNetworkBackground } from '@/components/effects/NeuralNetworkBackground';

export default function NotFound() {
  return (
    <main className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Neural Network Background */}
      <NeuralNetworkBackground />

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-2xl mx-auto text-center space-y-8">
          {/* 404 Illustration */}
          <div className="relative">
            <h1 className="text-9xl md:text-[12rem] font-bold bg-gradient-to-r from-accent-cyan via-accent-violet to-accent-teal bg-clip-text text-transparent animate-pulse">
              404
            </h1>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-32 h-32 rounded-full bg-gradient-to-br from-accent-cyan/20 to-accent-violet/20 blur-3xl animate-glow" />
            </div>
          </div>

          {/* Error Message */}
          <div className="space-y-4">
            <h2 className="text-3xl md:text-4xl font-bold text-text-primary">
              Page Not Found
            </h2>
            <p className="text-xl text-text-secondary max-w-lg mx-auto">
              The page you're looking for doesn't exist or has been moved. Let's get you back on track.
            </p>
          </div>

          {/* Suggestions */}
          <div className="glass backdrop-blur-md rounded-2xl p-8 border border-glass-border space-y-4">
            <h3 className="text-lg font-semibold text-text-primary">
              Here are some helpful links:
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Link
                href="/"
                className="flex items-center space-x-3 p-4 rounded-lg hover:bg-glass-highlight transition-colors group"
              >
                <svg
                  className="w-6 h-6 text-accent-cyan group-hover:scale-110 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                  />
                </svg>
                <div className="text-left">
                  <div className="text-sm font-medium text-text-primary">Home</div>
                  <div className="text-xs text-text-tertiary">Back to landing page</div>
                </div>
              </Link>

              <Link
                href={process.env.NEXT_PUBLIC_DOCUSAURUS_URL || '/learn'}
                className="flex items-center space-x-3 p-4 rounded-lg hover:bg-glass-highlight transition-colors group"
              >
                <svg
                  className="w-6 h-6 text-accent-violet group-hover:scale-110 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                  />
                </svg>
                <div className="text-left">
                  <div className="text-sm font-medium text-text-primary">Learn</div>
                  <div className="text-xs text-text-tertiary">Browse curriculum</div>
                </div>
              </Link>

              <Link
                href="/auth/login"
                className="flex items-center space-x-3 p-4 rounded-lg hover:bg-glass-highlight transition-colors group"
              >
                <svg
                  className="w-6 h-6 text-accent-teal group-hover:scale-110 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
                  />
                </svg>
                <div className="text-left">
                  <div className="text-sm font-medium text-text-primary">Login</div>
                  <div className="text-xs text-text-tertiary">Access your account</div>
                </div>
              </Link>

              <Link
                href="/about"
                className="flex items-center space-x-3 p-4 rounded-lg hover:bg-glass-highlight transition-colors group"
              >
                <svg
                  className="w-6 h-6 text-accent-cyan group-hover:scale-110 transition-transform"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <div className="text-left">
                  <div className="text-sm font-medium text-text-primary">About</div>
                  <div className="text-xs text-text-tertiary">Learn about us</div>
                </div>
              </Link>
            </div>
          </div>

          {/* CTA */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link href="/">
              <Button variant="primary" size="lg" className="w-full sm:w-auto">
                Go to Homepage
              </Button>
            </Link>
            <button
              onClick={() => window.history.back()}
              className="inline-flex items-center justify-center px-6 py-3 glass backdrop-blur-md rounded-lg text-text-primary font-semibold border border-accent-cyan hover:bg-glass-highlight transition-all duration-normal focus:outline-none focus:ring-2 focus:ring-accent-cyan"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
