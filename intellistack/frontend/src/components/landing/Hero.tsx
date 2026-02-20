'use client';

import React from 'react';
import Link from 'next/link';
import { RobotDisplay } from '@/components/effects/RobotDisplay';

interface HeroProps {
  className?: string;
}

export function Hero({ className = '' }: HeroProps) {
  return (
    <section className={`relative min-h-screen flex items-center justify-center overflow-hidden ${className}`}>
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-bg-primary via-bg-secondary to-bg-primary" />

      {/* Accent Gradients */}
      <div className="absolute top-0 left-0 w-1/2 h-1/2 bg-gradient-radial from-accent-cyan/20 to-transparent blur-3xl" />
      <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-gradient-radial from-accent-violet/20 to-transparent blur-3xl" />

      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Column - Content */}
          <div className="text-center lg:text-left space-y-8 animate-fade-in-up">
            {/* Logo/Brand */}
            <div className="flex items-center justify-center lg:justify-start space-x-3">
              <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-glow-cyan">
                <span className="text-white font-bold text-3xl">IS</span>
              </div>
              <div>
                <h1 className="text-4xl md:text-5xl font-bold text-text-primary">
                  IntelliStack
                </h1>
                <p className="text-text-tertiary text-sm">AI-Native Learning Platform</p>
              </div>
            </div>

            {/* Headline */}
            <div className="space-y-4">
              <h2 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
                <span className="text-text-primary">Master </span>
                <span className="bg-gradient-to-r from-accent-cyan via-accent-violet to-accent-teal bg-clip-text text-transparent">
                  Physical AI
                </span>
              </h2>
              <h3 className="text-3xl md:text-4xl font-semibold text-text-secondary">
                & Humanoid Robotics
              </h3>
            </div>

            {/* Description */}
            <p className="text-xl text-text-secondary max-w-2xl mx-auto lg:mx-0">
              Learn robotics with AI-powered tutoring, interactive simulations, and hands-on projects.
              From ROS 2 fundamentals to advanced perception and planning.
            </p>

            {/* CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link
                href={`${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/stage-1/intro`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center rounded-md font-semibold transition-all duration-normal focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-cyan focus-visible:ring-offset-2 px-6 py-3 text-lg bg-accent-cyan text-bg-primary hover:shadow-glow-cyan hover:scale-105 active:scale-95 w-full sm:w-auto"
              >
                Start Learning Free
              </Link>
              <Link
                href={`${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/stage-1/intro`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center rounded-md font-semibold transition-all duration-normal focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent-cyan focus-visible:ring-offset-2 px-6 py-3 text-lg border-2 border-accent-cyan text-accent-cyan hover:bg-accent-cyan hover:text-bg-primary w-full sm:w-auto"
              >
                Explore Curriculum
              </Link>
            </div>

            {/* Social Proof */}
            <div className="flex items-center justify-center lg:justify-start space-x-8 pt-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-accent-cyan">5K+</div>
                <div className="text-sm text-text-tertiary">Students</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-accent-violet">50+</div>
                <div className="text-sm text-text-tertiary">Lessons</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-accent-teal">100+</div>
                <div className="text-sm text-text-tertiary">Exercises</div>
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

            {/* Floating Feature Pills */}
            <div className="absolute top-10 left-0 glass backdrop-blur-md rounded-full px-4 py-2 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-accent-cyan animate-pulse" />
                <span className="text-sm text-text-primary font-medium">AI Tutor</span>
              </div>
            </div>

            <div className="absolute top-32 right-0 glass backdrop-blur-md rounded-full px-4 py-2 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-accent-violet animate-pulse" />
                <span className="text-sm text-text-primary font-medium">Live Simulations</span>
              </div>
            </div>

            <div className="absolute bottom-20 left-10 glass backdrop-blur-md rounded-full px-4 py-2 animate-fade-in-up" style={{ animationDelay: '0.6s' }}>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-accent-teal animate-pulse" />
                <span className="text-sm text-text-primary font-medium">Hands-on Projects</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <svg
          className="w-6 h-6 text-text-tertiary"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 14l-7 7m0 0l-7-7m7 7V3"
          />
        </svg>
      </div>
    </section>
  );
}
