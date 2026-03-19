'use client';

import React from 'react';
import Link from 'next/link';
import { LoginForm } from '@/components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      {/* Left panel — ambient branding (hidden on mobile) */}
      <div className="hidden lg:flex flex-col justify-between bg-bg-secondary border-r border-border-subtle p-12 relative overflow-hidden">
        {/* Ambient glow orb */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-accent-blue/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-0 w-64 h-64 bg-accent-violet/8 rounded-full blur-[80px] pointer-events-none" />

        {/* Logo */}
        <Link href="/" className="inline-flex items-center space-x-2 group w-fit">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent-blue to-accent-violet flex items-center justify-center group-hover:shadow-glow-blue transition-all">
            <span className="text-white font-bold text-xl font-heading">IS</span>
          </div>
          <span className="text-xl font-bold text-text-primary font-heading">IntelliStack</span>
        </Link>

        {/* Center copy */}
        <div className="relative z-10 space-y-6">
          <h2 className="text-4xl font-bold font-heading text-text-primary leading-tight">
            Enter the Lab.
            <br />
            <span className="text-accent-blue">Master Physical AI.</span>
          </h2>
          <p className="text-text-secondary text-lg leading-relaxed max-w-sm">
            Progressive robotics education from ROS 2 fundamentals to advanced humanoid AI integration.
          </p>

          {/* Social proof stats */}
          <div className="grid grid-cols-3 gap-4 pt-4">
            {[
              { value: '5K+', label: 'Learners' },
              { value: '50+', label: 'Lessons' },
              { value: '95%', label: 'Completion' },
            ].map((stat) => (
              <div key={stat.label} className="surface rounded-xl p-3 text-center">
                <div className="text-2xl font-bold font-heading text-accent-amber">{stat.value}</div>
                <div className="text-xs text-text-muted mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Status pill */}
        <div className="flex items-center gap-2 w-fit surface rounded-full px-4 py-2">
          <span className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
          <span className="text-sm text-text-secondary">Platform online · All systems nominal</span>
        </div>
      </div>

      {/* Right panel — form */}
      <div className="flex flex-col items-center justify-center bg-bg-primary px-6 py-16">
        <div className="w-full max-w-sm space-y-8">
          {/* Mobile logo */}
          <div className="lg:hidden text-center">
            <Link href="/" className="inline-flex items-center space-x-2 justify-center">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-accent-blue to-accent-violet flex items-center justify-center">
                <span className="text-white font-bold text-xl font-heading">IS</span>
              </div>
              <span className="text-xl font-bold text-text-primary font-heading">IntelliStack</span>
            </Link>
          </div>

          <div>
            <h1 className="text-3xl font-bold font-heading text-text-primary">Welcome back</h1>
            <p className="mt-2 text-text-secondary">Sign in to continue your learning journey</p>
          </div>

          {/* Login form */}
          <div className="surface rounded-2xl p-6">
            <LoginForm />

            <p className="mt-6 text-center text-text-secondary text-sm">
              Don&apos;t have an account?{' '}
              <Link href="/auth/register" className="font-semibold text-accent-blue hover:text-accent-blue-light transition-colors">
                Sign up
              </Link>
            </p>
          </div>

          <div className="text-center">
            <Link href="/" className="text-text-muted hover:text-text-secondary transition-colors text-sm">
              ← Back to home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
