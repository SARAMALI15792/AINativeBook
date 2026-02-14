'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/form';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';
import { SocialLoginButtons } from '@/components/auth/SocialLoginButtons';
import { BetterAuthBadge } from '@/components/auth/BetterAuthBadge';

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      await login(email, password);
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
    <div className="min-h-screen flex">
      {/* Left Brand Panel (desktop only) */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary to-primary-400 relative items-center justify-center p-12 overflow-hidden">
        {/* Floating translucent circles */}
        <div className="absolute top-10 left-10 w-32 h-32 rounded-full bg-white/5 animate-float" />
        <div className="absolute bottom-20 right-10 w-24 h-24 rounded-full bg-white/10 animate-float" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/3 right-20 w-16 h-16 rounded-full bg-white/5 animate-float" style={{ animationDelay: '2s' }} />
        {/* Pulsing accent dots */}
        <div className="absolute top-20 right-1/3 w-3 h-3 rounded-full bg-white/40 animate-pulse-soft" />
        <div className="absolute bottom-32 left-1/4 w-2 h-2 rounded-full bg-white/30 animate-pulse-soft" style={{ animationDelay: '1s' }} />

        <div className="max-w-md text-white relative z-10">
          <div className="flex items-center gap-3 mb-8 animate-fade-in-up">
            <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center animate-glow">
              <span className="text-2xl font-bold">IS</span>
            </div>
            <div>
              <h2 className="text-2xl font-bold font-serif m-0">IntelliStack</h2>
              <p className="text-sm text-white/70 m-0">Physical AI & Humanoid Robotics</p>
            </div>
          </div>
          <h1 className="text-4xl font-bold font-serif mb-4 leading-tight animate-fade-in-up" style={{ animationDelay: '0.2s', animationFillMode: 'both' }}>
            Welcome back to your learning journey
          </h1>
          <p className="text-lg text-white/80 leading-relaxed mb-8 animate-fade-in-up" style={{ animationDelay: '0.4s', animationFillMode: 'both' }}>
            Continue mastering robotics with AI-powered tutoring, structured
            curricula, and hands-on projects.
          </p>

          {/* Feature highlights */}
          <div className="space-y-3">
            {[
              '5-Stage Progressive Learning Path',
              'AI-Powered Socratic Tutoring',
              'Hands-on Simulation Projects',
            ].map((feature, i) => (
              <div
                key={feature}
                className="flex items-center gap-3 animate-slide-in-right"
                style={{ animationDelay: `${0.6 + i * 0.15}s`, animationFillMode: 'both' }}
              >
                <div className="w-2 h-2 rounded-full bg-white/60 flex-shrink-0" />
                <span className="text-sm text-white/90 font-medium">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Form Panel */}
      <div className="flex-1 flex items-center justify-center p-6 sm:p-8">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="lg:hidden text-center mb-8 animate-fade-in-up">
            <div className="inline-flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-primary-400 flex items-center justify-center">
                <span className="text-white text-lg font-bold">IS</span>
              </div>
              <span className="text-xl font-bold font-serif text-foreground">IntelliStack</span>
            </div>
          </div>

          <div className="bg-card rounded-xl border border-border p-6 sm:p-8 shadow-book animate-scale-in">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold font-serif text-foreground mb-1">Sign In</h2>
              <p className="text-sm text-muted-foreground m-0">
                Or{' '}
                <Link href="/register" className="text-primary hover:underline font-medium">
                  create a new account
                </Link>
              </p>
            </div>

            <SocialLoginButtons />

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

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 rounded border-border text-primary focus:ring-ring"
                  />
                  <Label htmlFor="remember-me" className="text-sm font-normal">
                    Remember me
                  </Label>
                </div>

                <Link
                  href="/forgot-password"
                  className="text-sm text-primary hover:underline font-medium"
                >
                  Forgot password?
                </Link>
              </div>

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? 'Signing in...' : 'Sign in'}
              </Button>
            </form>

            <BetterAuthBadge />
          </div>
        </div>
      </div>
    </div>
  );
}
