import React from 'react';
import Link from 'next/link';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export const metadata = {
  title: 'Dashboard - IntelliStack',
  description: 'Your learning dashboard',
};

const stages = [
  { number: 1, slug: 'stage-1', title: 'Foundations', description: 'ROS 2 fundamentals, workspace setup, and basic concepts' },
  { number: 2, slug: 'stage-2', title: 'ROS 2 & Simulation', description: 'Gazebo, URDF modeling, and simulation environments' },
  { number: 3, slug: 'stage-3', title: 'Perception & Planning', description: 'Computer vision, sensor fusion, and path planning' },
  { number: 4, slug: 'stage-4', title: 'AI Integration', description: 'Machine learning models and AI-driven behaviors' },
  { number: 5, slug: 'stage-5', title: 'Capstone Project', description: 'Build a complete autonomous robotics system' },
];

export default function DashboardPage() {
  return (
    <main className="relative min-h-screen">
      <Header />

      <div className="container mx-auto px-4 py-20">
        <h1 className="text-4xl font-bold text-text-primary mb-4">
          Your Learning Dashboard
        </h1>
        <p className="text-text-secondary mb-10">
          Continue your robotics journey through the 5-stage curriculum.
        </p>

        <div className="grid gap-4">
          {stages.map((stage) => (
            <Link
              key={stage.number}
              href={`/curriculum/${stage.slug}`}
              className="glass backdrop-blur-md rounded-xl p-6 border border-glass-border hover:border-accent-cyan transition-all group flex items-center gap-4"
            >
              <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center text-white font-bold text-xl shadow-glow-cyan">
                {stage.number}
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-bold text-text-primary group-hover:text-accent-cyan transition-colors">
                  Stage {stage.number}: {stage.title}
                </h2>
                <p className="text-text-secondary text-sm">{stage.description}</p>
              </div>
              <svg className="w-5 h-5 text-accent-cyan group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          ))}
        </div>
      </div>

      <Footer />
    </main>
  );
}
