import React from 'react';
import Link from 'next/link';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export const metadata = {
  title: 'Curriculum - IntelliStack',
  description: '5-stage progressive learning path',
};

export default function CurriculumPage() {
  const stages = [
    { id: 1, title: 'Foundations', slug: 'stage-1', description: 'Learn ROS 2 fundamentals, workspace setup, and basic concepts' },
    { id: 2, title: 'ROS 2 & Simulation', slug: 'stage-2', description: 'Master Gazebo, URDF modeling, and simulation environments' },
    { id: 3, title: 'Perception & Planning', slug: 'stage-3', description: 'Implement computer vision, sensor fusion, and path planning' },
    { id: 4, title: 'AI Integration', slug: 'stage-4', description: 'Integrate machine learning models and AI-driven behaviors' },
    { id: 5, title: 'Capstone Project', slug: 'stage-5', description: 'Build a complete autonomous robotics system' },
  ];

  return (
    <main className="relative min-h-screen">
      <Header />

      <div className="container mx-auto px-4 py-20">
        <div className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-text-primary mb-4">
            Learning Curriculum
          </h1>
          <p className="text-xl text-text-secondary max-w-3xl">
            Master Physical AI and Humanoid Robotics through our progressive 5-stage learning path.
            Each stage builds on the previous one, unlocking as you demonstrate mastery.
          </p>
        </div>

        <div className="grid gap-6">
          {stages.map((stage) => (
            <Link
              key={stage.id}
              href={`${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/${stage.slug}/intro`}
              target="_blank"
              rel="noopener noreferrer"
              className="glass backdrop-blur-md rounded-xl p-6 border border-glass-border hover:border-accent-cyan transition-all group"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center text-white font-bold text-xl shadow-glow-cyan">
                  {stage.id}
                </div>
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-text-primary mb-2 group-hover:text-accent-cyan transition-colors">
                    Stage {stage.id}: {stage.title}
                  </h2>
                  <p className="text-text-secondary mb-3">
                    {stage.description}
                  </p>
                  <div className="flex items-center text-accent-cyan font-medium">
                    <span>Explore this stage</span>
                    <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        <div className="mt-12 glass backdrop-blur-md rounded-xl p-6 border border-glass-border">
          <h3 className="text-xl font-bold text-text-primary mb-3">
            How It Works
          </h3>
          <ul className="space-y-2 text-text-secondary">
            <li className="flex items-start">
              <svg className="w-5 h-5 text-accent-cyan mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Complete lessons, exercises, and assessments in each stage</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-accent-cyan mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Unlock the next stage by demonstrating mastery of prerequisites</span>
            </li>
            <li className="flex items-start">
              <svg className="w-5 h-5 text-accent-cyan mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Earn badges and certificates as you progress through the curriculum</span>
            </li>
          </ul>
        </div>
      </div>

      <Footer />
    </main>
  );
}
