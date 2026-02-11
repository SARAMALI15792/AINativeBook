'use client';

import { useState } from 'react';
import Link from 'next/link';
import { authClient } from '@/lib/auth-client';
import { BetterAuthBadge } from '@/components/auth/BetterAuthBadge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/form';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle, CheckCircle, ArrowLeft, Mail } from 'lucide-react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await authClient.requestPasswordReset(email);
      setIsSuccess(true);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 sm:p-8">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center">
              <span className="text-white text-lg font-bold">IS</span>
            </div>
            <span className="text-xl font-bold font-serif text-foreground">IntelliStack</span>
          </div>
        </div>

        <div className="bg-card rounded-xl border border-border p-6 sm:p-8 shadow-book">
          {isSuccess ? (
            <div className="text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mx-auto">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold font-serif text-foreground">
                Check your email
              </h2>
              <p className="text-sm text-muted-foreground">
                If an account exists with <strong>{email}</strong>, you will
                receive password reset instructions shortly.
              </p>
              <div className="space-y-3 pt-2">
                <Link href="/login">
                  <Button className="w-full">Return to login</Button>
                </Link>
                <p className="text-sm text-muted-foreground">
                  Didn&apos;t receive the email?{' '}
                  <button
                    onClick={() => setIsSuccess(false)}
                    className="text-primary hover:underline font-medium"
                  >
                    Try again
                  </button>
                </p>
              </div>
            </div>
          ) : (
            <>
              <div className="text-center mb-6">
                <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                  <Mail className="w-6 h-6 text-primary" />
                </div>
                <h2 className="text-2xl font-bold font-serif text-foreground mb-1">
                  Reset your password
                </h2>
                <p className="text-sm text-muted-foreground m-0">
                  Enter your email address and we&apos;ll send you a link to
                  reset your password.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <Label htmlFor="email">Email address</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                  />
                </div>

                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? 'Sending...' : 'Send reset link'}
                </Button>

                <div className="text-center">
                  <Link
                    href="/login"
                    className="inline-flex items-center gap-1 text-sm text-primary hover:underline font-medium"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    Back to login
                  </Link>
                </div>
              </form>
            </>
          )}

          <BetterAuthBadge />
        </div>
      </div>
    </div>
  );
}
