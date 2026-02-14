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
import { PasswordStrengthMeter } from '@/components/auth/PasswordStrengthMeter';

export default function RegisterPage() {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setIsLoading(true);

    try {
      await register(formData.email, formData.name, formData.password);
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
        <div className="absolute top-16 right-12 w-28 h-28 rounded-full bg-white/5 animate-float" />
        <div className="absolute bottom-16 left-8 w-20 h-20 rounded-full bg-white/10 animate-float" style={{ animationDelay: '1.5s' }} />
        <div className="absolute top-1/2 left-16 w-14 h-14 rounded-full bg-white/5 animate-float" style={{ animationDelay: '0.8s' }} />
        {/* Pulsing accent dots */}
        <div className="absolute top-24 left-1/3 w-3 h-3 rounded-full bg-white/40 animate-pulse-soft" />
        <div className="absolute bottom-24 right-1/4 w-2 h-2 rounded-full bg-white/30 animate-pulse-soft" style={{ animationDelay: '1.2s' }} />

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
            Begin your journey into Physical AI
          </h1>
          <p className="text-lg text-white/80 leading-relaxed mb-8 animate-fade-in-up" style={{ animationDelay: '0.4s', animationFillMode: 'both' }}>
            Join thousands of learners mastering humanoid robotics through structured,
            simulation-first education with AI-powered guidance.
          </p>

          {/* Stats grid */}
          <div className="grid grid-cols-3 gap-4">
            {[
              { value: '5', label: 'Learning Stages' },
              { value: 'AI', label: 'Powered Tutoring' },
              { value: '24/7', label: 'Access' },
            ].map((stat, i) => (
              <div
                key={stat.label}
                className="text-center p-3 rounded-lg bg-white/10 backdrop-blur-sm animate-slide-in-right"
                style={{ animationDelay: `${0.6 + i * 0.15}s`, animationFillMode: 'both' }}
              >
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-xs text-white/70 mt-1">{stat.label}</div>
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
              <h2 className="text-2xl font-bold font-serif text-foreground mb-1">
                Create Account
              </h2>
              <p className="text-sm text-muted-foreground m-0">
                Or{' '}
                <Link href="/login" className="text-primary hover:underline font-medium">
                  sign in to existing account
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
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  autoComplete="name"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Create a strong password"
                />
                <PasswordStrengthMeter password={formData.password} />
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm Password</Label>
                <Input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  placeholder="Confirm your password"
                />
                {formData.confirmPassword && formData.password !== formData.confirmPassword && (
                  <p className="text-xs text-destructive">Passwords do not match</p>
                )}
              </div>

              <div className="flex items-start space-x-2">
                <input
                  id="terms"
                  name="terms"
                  type="checkbox"
                  required
                  className="h-4 w-4 mt-1 rounded border-border text-primary focus:ring-ring"
                />
                <Label htmlFor="terms" className="text-sm font-normal leading-relaxed">
                  I agree to the{' '}
                  <Link href="/terms" className="text-primary hover:underline">
                    Terms of Service
                  </Link>{' '}
                  and{' '}
                  <Link href="/privacy" className="text-primary hover:underline">
                    Privacy Policy
                  </Link>
                </Label>
              </div>

              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? 'Creating account...' : 'Create account'}
              </Button>
            </form>

            <BetterAuthBadge />
          </div>
        </div>
      </div>
    </div>
  );
}
