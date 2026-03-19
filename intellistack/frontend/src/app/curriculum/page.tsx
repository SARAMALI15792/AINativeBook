import React from 'react';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export const metadata = {
  title: 'Curriculum - IntelliStack',
  description: '5-stage progressive learning path',
};

const DOCUSAURUS_URL = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3005/AINativeBook';

const stages = [
  { id: 1, slug: 'stage-1', title: 'Foundations',           description: 'Learn ROS 2 fundamentals, workspace setup, and basic concepts' },
  { id: 2, slug: 'stage-2', title: 'ROS 2 & Simulation',    description: 'Master Gazebo, URDF modeling, and simulation environments' },
  { id: 3, slug: 'stage-3', title: 'Perception & Planning',  description: 'Implement computer vision, sensor fusion, and path planning' },
  { id: 4, slug: 'stage-4', title: 'AI Integration',         description: 'Integrate machine learning models and AI-driven behaviors' },
  { id: 5, slug: 'stage-5', title: 'Capstone Project',       description: 'Build a complete autonomous robotics system' },
];

export default function CurriculumPage() {
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
            <a
              key={stage.id}
              href={`${DOCUSAURUS_URL}/${stage.slug}/intro`}
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
                    <span>Open in learning platform</span>
                    <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </div>
                </div>
              </div>
            </a>
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
