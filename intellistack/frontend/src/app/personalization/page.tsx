'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { PersonalizationWizard } from '@/components/personalization/PersonalizationWizard';
import { NeuralNetworkBackground } from '@/components/effects/NeuralNetworkBackground';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/components/ui/Toast';
import type { PersonalizationPreferences } from '@/types/api';

export default function PersonalizationPage() {
  const router = useRouter();
  const { session, isLoading, updatePreferences } = useAuth();
  const { success, error: showError, info } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auth guard - redirect if not authenticated
  React.useEffect(() => {
    if (!isLoading && !session.isAuthenticated) {
      router.push('/auth/login?redirect=/personalization');
    }
  }, [session.isAuthenticated, isLoading, router]);

  // Show loading state while checking auth
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Don't render if not authenticated
  if (!session.isAuthenticated) {
    return null;
  }

  const handleComplete = async (preferences: PersonalizationPreferences) => {
    setIsSubmitting(true);
    setError(null);

    // Show loading toast
    info('Saving...', 'Saving your preferences');

    try {
      await updatePreferences(preferences);

      // Show success toast
      success('Preferences Saved!', 'Your learning experience has been personalized');

      // Verify session is active before redirect
      const authModule = await import('@/lib/auth');
      const sessionCheck = await authModule.getSession();

      if (!sessionCheck?.user) {
        showError('Session Expired', 'Please log in again');
        setError('Session expired. Please log in again.');
        setIsSubmitting(false);
        return;
      }

      // Add small delay to ensure cookie is set
      await new Promise(resolve => setTimeout(resolve, 500));

      // Show redirect toast
      info('Redirecting...', 'Taking you to your learning content');

      // Redirect to Docusaurus with indicator
      const docusaurusUrl = `${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/docs/stage-1/intro?from=personalization`;
      window.location.href = docusaurusUrl;
    } catch (err) {
      console.error('Error in handleComplete:', err);
      const errorMessage = err instanceof Error && err.message
        ? err.message
        : typeof err === 'string'
        ? err
        : 'Failed to save preferences. Please try again.';
      setError(errorMessage);
      showError('Save Failed', errorMessage);
      setIsSubmitting(false);
    }
  };

  const handleSkip = () => {
    // Redirect to Docusaurus without saving preferences
    const docusaurusUrl = `${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/docs/stage-1/intro`;
    window.location.href = docusaurusUrl;
  };

  return (
    <main className="relative min-h-screen">
      {/* Neural Network Background */}
      <NeuralNetworkBackground />

      <div className="container mx-auto px-4 py-12 relative z-10">
        {/* Header */}
        <div className="text-center mb-12 space-y-4">
          <Link href="/" className="inline-flex items-center justify-center space-x-3 group mb-4">
            <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-glow-cyan group-hover:shadow-glow-violet transition-all">
              <span className="text-white font-bold text-2xl">IS</span>
            </div>
            <span className="text-2xl font-bold text-text-primary">IntelliStack</span>
          </Link>
          <h1 className="text-4xl md:text-5xl font-bold text-text-primary">
            Personalize Your Learning
          </h1>
          <p className="text-xl text-text-secondary max-w-2xl mx-auto">
            Help us tailor your robotics education to your goals, experience, and schedule
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8">
            <div
              className="p-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400"
              role="alert"
            >
              {error}
            </div>
          </div>
        )}

        {/* Loading Overlay */}
        {isSubmitting && (
          <div className="fixed inset-0 z-modal flex items-center justify-center bg-black/60 backdrop-blur-sm">
            <div className="glass backdrop-blur-md rounded-xl p-8 text-center space-y-4">
              <div className="w-16 h-16 mx-auto border-4 border-accent-cyan border-t-transparent rounded-full animate-spin" />
              <p className="text-text-primary font-medium">Saving your preferences...</p>
            </div>
          </div>
        )}

        {/* Wizard */}
        <PersonalizationWizard onComplete={handleComplete} onSkip={handleSkip} />

        {/* Benefits Section */}
        <div className="max-w-4xl mx-auto mt-16 pt-16 border-t border-glass-border">
          <h2 className="text-2xl font-bold text-text-primary text-center mb-8">
            Why personalize your experience?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="glass backdrop-blur-md rounded-lg p-6 border border-glass-border text-center space-y-3">
              <div className="w-12 h-12 mx-auto rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-text-primary">Faster Progress</h3>
              <p className="text-sm text-text-secondary">
                Learn at your own pace with content matched to your experience level
              </p>
            </div>

            <div className="glass backdrop-blur-md rounded-lg p-6 border border-glass-border text-center space-y-3">
              <div className="w-12 h-12 mx-auto rounded-lg bg-gradient-to-br from-accent-violet to-pink-500 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-text-primary">Relevant Content</h3>
              <p className="text-sm text-text-secondary">
                Focus on topics that align with your interests and career goals
              </p>
            </div>

            <div className="glass backdrop-blur-md rounded-lg p-6 border border-glass-border text-center space-y-3">
              <div className="w-12 h-12 mx-auto rounded-lg bg-gradient-to-br from-accent-teal to-green-500 flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-text-primary">Smart Scheduling</h3>
              <p className="text-sm text-text-secondary">
                Get recommendations that fit your weekly time commitment
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
