'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Input, Button } from '@/components/ui';
import { loginSchema, type LoginFormData } from '@/lib/validation';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/components/ui/Toast';

interface LoginFormProps {
  onSuccess?: () => void;
  className?: string;
}

export function LoginForm({ onSuccess, className = '' }: LoginFormProps) {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { login, session, isLoading: authLoading } = useAuth();
  const { success, error: showError, info } = useToast();
  const justLoggedIn = useRef(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  // Redirect after session updates post-login
  useEffect(() => {
    if (justLoggedIn.current && session.isAuthenticated && !authLoading) {
      justLoggedIn.current = false;

      // Show success toast with user name
      const userName = session.user?.name || 'there';
      success('Welcome back!', `You're now signed in as ${userName}`);

      onSuccess?.();

      if (!session.hasCompletedPersonalization) {
        info('Setup Required', 'Let\'s personalize your learning experience');
        setTimeout(() => {
          router.push('/personalization');
        }, 500);
      } else {
        info('Redirecting...', 'Taking you to your learning dashboard');
        setTimeout(() => {
          const docusaurusUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002';
          window.location.href = `${docusaurusUrl}/docs/stage-1/intro?from=login`;
        }, 500);
      }
    }
  }, [session.isAuthenticated, session.hasCompletedPersonalization, session.user, authLoading, onSuccess, router, success, info]);

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      justLoggedIn.current = true;
      await login(data.email, data.password);
    } catch (err) {
      justLoggedIn.current = false;
      const errorMessage = err instanceof Error && err.message
        ? err.message
        : 'Login failed. Please try again.';
      setError(errorMessage);
      showError('Login Failed', errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className={`space-y-6 ${className}`}>
      {/* Error Message */}
      {error && (
        <div
          className="p-4 rounded-lg bg-red-500/10 border border-red-500/50 text-red-400"
          role="alert"
        >
          {error}
        </div>
      )}

      {/* Email Field */}
      <Input
        {...register('email')}
        type="email"
        label="Email"
        placeholder="you@example.com"
        error={errors.email?.message}
        leftIcon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
            />
          </svg>
        }
        disabled={isLoading}
      />

      {/* Password Field */}
      <Input
        {...register('password')}
        type={showPassword ? 'text' : 'password'}
        label="Password"
        placeholder="••••••••"
        error={errors.password?.message}
        leftIcon={
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
        }
        rightIcon={
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="text-text-tertiary hover:text-text-primary transition-colors focus:outline-none"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                />
              </svg>
            ) : (
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                />
              </svg>
            )}
          </button>
        }
        disabled={isLoading}
      />

      {/* Forgot Password Link */}
      <div className="flex justify-end">
        <a
          href="/auth/forgot-password"
          className="text-sm text-accent-cyan hover:text-accent-teal transition-colors focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded px-1"
        >
          Forgot password?
        </a>
      </div>

      {/* Submit Button */}
      <Button
        type="submit"
        variant="primary"
        size="lg"
        fullWidth
        loading={isLoading}
        disabled={isLoading}
      >
        {isLoading ? 'Signing in...' : 'Sign In'}
      </Button>
    </form>
  );
}
