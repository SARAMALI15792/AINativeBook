'use client';

import React from 'react';
import Link from 'next/link';
import { RobotDisplay } from '@/components/effects/RobotDisplay';

interface HeroProps {
  className?: string;
}

const docusaurusUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3005/AINativeBook';

export function Hero({ className = '' }: HeroProps) {
  return (
    <section className={`relative min-h-screen flex items-center justify-center overflow-hidden ${className}`}>
      {/* Ambient gradient orbs — Electric Blue + Indigo */}
      <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-accent-blue/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] bg-accent-violet/8 rounded-full blur-[120px] pointer-events-none" />

      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Column */}
          <div className="text-center lg:text-left space-y-8 animate-fade-in-up">
            {/* Headline — tricolor gradient */}
            <div className="space-y-4">
              <h2 className="text-5xl md:text-6xl lg:text-7xl font-bold font-heading leading-tight">
                <span className="text-text-primary">Master </span>
                <span className="bg-gradient-to-r from-accent-blue via-accent-violet to-accent-emerald bg-clip-text text-transparent">
                  Physical AI
                </span>
              </h2>
              <h3 className="text-3xl md:text-4xl font-semibold text-text-secondary">
                & Humanoid Robotics
              </h3>
            </div>

            {/* Description */}
            <p className="text-xl text-text-secondary max-w-2xl mx-auto lg:mx-0 leading-relaxed">
              Learn robotics with AI-powered tutoring, interactive simulations, and hands-on projects.
              From ROS 2 fundamentals to advanced perception and planning.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <a
                href={`${docusaurusUrl}/stage-1/intro`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center rounded-lg font-semibold transition-all duration-normal px-6 py-3 text-lg bg-gradient-to-r from-accent-blue to-accent-violet text-white hover:shadow-glow-blue hover:scale-105 active:scale-95 w-full sm:w-auto"
              >
                Start Learning Free
              </a>
              <Link
                href="/curriculum"
                className="inline-flex items-center justify-center rounded-lg font-semibold transition-all duration-normal px-6 py-3 text-lg border border-border-emphasis text-text-secondary hover:border-accent-blue hover:text-accent-blue w-full sm:w-auto"
              >
                Explore Curriculum
              </Link>
            </div>

            {/* Stats — amber for achievement warmth */}
            <div className="flex items-center justify-center lg:justify-start space-x-8 pt-4">
              <div className="text-center">
                <div className="text-3xl font-bold font-heading text-accent-amber">5K+</div>
                <div className="text-sm text-text-muted">Students</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold font-heading text-accent-amber">50+</div>
                <div className="text-sm text-text-muted">Lessons</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold font-heading text-accent-amber">100+</div>
                <div className="text-sm text-text-muted">Exercises</div>
              </div>
            </div>
          </div>

          {/* Right Column - Robot Display */}
          <div className="relative h-[400px] md:h-[500px] lg:h-[600px] animate-fade-in">
            <RobotDisplay
              className="w-full h-full"
              autoRotate={true}
              enableZoom={false}
              force2D={true}
            />

            {/* Floating tech badges — surface style with emerald pulse dot */}
            <div className="absolute top-10 left-0 surface rounded-full px-4 py-2 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
                <span className="text-sm text-text-primary font-medium">AI Tutor</span>
              </div>
            </div>

            <div className="absolute top-32 right-0 surface rounded-full px-4 py-2 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
                <span className="text-sm text-text-primary font-medium">Live Simulations</span>
              </div>
            </div>

            <div className="absolute bottom-20 left-10 surface rounded-full px-4 py-2 animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-accent-emerald animate-pulse" />
                <span className="text-sm text-text-primary font-medium">Hands-on Projects</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <svg className="w-6 h-6 text-text-muted" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>
  );
}
