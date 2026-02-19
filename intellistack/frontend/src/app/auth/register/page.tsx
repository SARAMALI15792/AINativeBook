import React from 'react';
import Link from 'next/link';
import { RegisterForm } from '@/components/auth/RegisterForm';
import { SocialAuthButtons } from '@/components/auth/SocialAuthButtons';
import { NeuralNetworkBackground } from '@/components/effects/NeuralNetworkBackground';

export const metadata = {
  title: 'Sign Up - IntelliStack',
  description: 'Create your IntelliStack account and start learning robotics with AI-powered guidance.',
};

export default function RegisterPage() {
  return (
    <main className="relative min-h-screen flex items-center justify-center">
      {/* Neural Network Background */}
      <NeuralNetworkBackground />

      <div className="container mx-auto px-4 py-12 relative z-10">
        <div className="max-w-md mx-auto">
          {/* Logo and Header */}
          <div className="text-center mb-8 space-y-4">
            <Link href="/" className="inline-flex items-center justify-center space-x-3 group">
              <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-glow-cyan group-hover:shadow-glow-violet transition-all">
                <span className="text-white font-bold text-2xl">IS</span>
              </div>
              <span className="text-2xl font-bold text-text-primary">IntelliStack</span>
            </Link>
            <h1 className="text-3xl font-bold text-text-primary">Create Your Account</h1>
            <p className="text-text-secondary">Start your robotics learning journey today</p>
          </div>

          {/* Auth Card */}
          <div className="glass backdrop-blur-md rounded-2xl p-8 border border-glass-border shadow-xl">
            {/* Social Auth Buttons */}
            <SocialAuthButtons mode="register" />

            {/* Register Form */}
            <RegisterForm />

            {/* Terms and Privacy */}
            <p className="mt-6 text-sm text-text-tertiary text-center">
              By signing up, you agree to our{' '}
              <Link
                href="/terms"
                className="text-accent-cyan hover:text-accent-teal transition-colors focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded px-1"
              >
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link
                href="/privacy"
                className="text-accent-cyan hover:text-accent-teal transition-colors focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded px-1"
              >
                Privacy Policy
              </Link>
            </p>

            {/* Login Link */}
            <div className="mt-6 text-center">
              <p className="text-text-secondary">
                Already have an account?{' '}
                <Link
                  href="/auth/login"
                  className="text-accent-cyan hover:text-accent-teal font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded px-1"
                >
                  Sign in
                </Link>
              </p>
            </div>
          </div>

          {/* Back to Home */}
          <div className="mt-6 text-center">
            <Link
              href="/"
              className="text-text-tertiary hover:text-text-secondary transition-colors focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded px-2 py-1"
            >
              ← Back to home
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
