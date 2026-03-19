'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui';
import { NeuralNetworkBackground } from '@/components/effects/NeuralNetworkBackground';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to monitoring service
    console.error('Application error:', error);
  }, [error]);

  return (
    <main className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Neural Network Background */}
      <NeuralNetworkBackground />

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-2xl mx-auto text-center space-y-8">
          {/* Error Illustration */}
          <div className="relative">
            <div className="flex justify-center">
              <div className="w-32 h-32 rounded-full bg-error/20 flex items-center justify-center animate-pulse">
                <svg
                  className="w-16 h-16 text-error"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
              </div>
            </div>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-48 h-48 rounded-full bg-gradient-to-br from-error/20 to-warning/20 blur-3xl animate-glow" />
            </div>
          </div>

          {/* Error Message */}
          <div className="space-y-4">
            <h1 className="text-4xl md:text-5xl font-bold text-text-primary">
              Something Went Wrong
            </h1>
            <p className="text-xl text-text-secondary max-w-lg mx-auto">
              We encountered an unexpected error. Our team has been notified and is working on a fix.
            </p>
          </div>

          {/* Error Details (Development Only) */}
          {process.env.NODE_ENV === 'development' && (
            <div className="glass backdrop-blur-md rounded-2xl p-6 border border-glass-border text-left">
              <h3 className="text-sm font-semibold text-text-primary mb-3">
                Error Details (Development Only)
              </h3>
              <div className="bg-bg-tertiary rounded-lg p-4 overflow-auto max-h-40">
                <p className="text-xs text-error font-mono break-all">
                  {error.message}
                </p>
                {error.digest && (
                  <p className="text-xs text-text-tertiary font-mono mt-2">
                    Digest: {error.digest}
                  </p>
                )}
              </div>
            </div>
          )}

          {/* What You Can Do */}
          <div className="glass backdrop-blur-md rounded-2xl p-8 border border-glass-border space-y-4">
            <h3 className="text-lg font-semibold text-text-primary">
              What you can do:
            </h3>
            <ul className="space-y-3 text-left">
              <li className="flex items-start space-x-3">
                <svg
                  className="w-5 h-5 text-accent-cyan flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-text-secondary">
                  Try refreshing the page or clicking the retry button below
                </span>
              </li>
              <li className="flex items-start space-x-3">
                <svg
                  className="w-5 h-5 text-accent-violet flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-text-secondary">
                  Check your internet connection and try again
                </span>
              </li>
              <li className="flex items-start space-x-3">
                <svg
                  className="w-5 h-5 text-accent-teal flex-shrink-0 mt-0.5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="text-text-secondary">
                  If the problem persists, contact our support team
                </span>
              </li>
            </ul>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Button
              variant="primary"
              size="lg"
              onClick={reset}
              className="w-full sm:w-auto"
            >
              Try Again
            </Button>
            <Link href="/">
              <Button variant="outline" size="lg" className="w-full sm:w-auto">
                Go to Homepage
              </Button>
            </Link>
          </div>

          {/* Support Link */}
          <p className="text-sm text-text-tertiary">
            Need help?{' '}
            <Link
              href="/contact"
              className="text-accent-cyan hover:text-accent-teal transition-colors underline"
            >
              Contact Support
            </Link>
          </p>
        </div>
      </div>
    </main>
  );
}
