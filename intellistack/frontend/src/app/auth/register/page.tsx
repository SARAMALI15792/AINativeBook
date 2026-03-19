'use client';

import React from 'react';
import Link from 'next/link';
import { RegisterForm } from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  return (
    <div className="min-h-screen grid lg:grid-cols-2">
      {/* Left panel — ambient branding (hidden on mobile) */}
      <div className="hidden lg:flex flex-col justify-between bg-bg-secondary border-r border-border-subtle p-12 relative overflow-hidden">
        {/* Ambient glow orbs */}
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-accent-violet/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-0 w-64 h-64 bg-accent-blue/8 rounded-full blur-[80px] pointer-events-none" />

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
            Create your lab account.
            <br />
            <span className="text-accent-violet">Start building.</span>
          </h2>
          <p className="text-text-secondary text-lg leading-relaxed max-w-sm">
            Join thousands of engineers and researchers mastering the next generation of intelligent machines.
          </p>

          {/* Feature highlights */}
          <div className="space-y-3 pt-4">
            {[
              { icon: '⚡', text: 'AI-powered Socratic tutor' },
              { icon: '🤖', text: 'Gazebo & Isaac Sim environments' },
              { icon: '🏆', text: 'Earn verified certificates' },
            ].map((item) => (
              <div key={item.text} className="flex items-center gap-3 text-text-secondary">
                <span className="text-xl">{item.icon}</span>
                <span>{item.text}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Status pill */}
        <div className="flex items-center gap-2 w-fit surface rounded-full px-4 py-2">
          <span className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
          <span className="text-sm text-text-secondary">Free to start · No credit card required</span>
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
            <h1 className="text-3xl font-bold font-heading text-text-primary">Get started</h1>
            <p className="mt-2 text-text-secondary">Create your account to begin learning</p>
          </div>

          {/* Register form */}
          <div className="surface rounded-2xl p-6">
            <RegisterForm />

            <p className="mt-6 text-center text-text-secondary text-sm">
              Already have an account?{' '}
              <Link href="/auth/login" className="font-semibold text-accent-blue hover:text-accent-blue-light transition-colors">
                Sign in
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
