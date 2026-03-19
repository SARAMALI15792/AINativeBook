import React from 'react';
import Link from 'next/link';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export const metadata = {
  title: 'Dashboard - IntelliStack',
  description: 'Your learning dashboard',
};

const stages = [
  {
    number: 1,
    slug: 'stage-1',
    title: 'Foundations',
    description: 'ROS 2 fundamentals, workspace setup, and basic concepts',
    color: 'accent-emerald',
    unlocked: true,
  },
  {
    number: 2,
    slug: 'stage-2',
    title: 'ROS 2 & Simulation',
    description: 'Gazebo, URDF modeling, and simulation environments',
    color: 'accent-blue',
    unlocked: true,
  },
  {
    number: 3,
    slug: 'stage-3',
    title: 'Perception & Planning',
    description: 'Computer vision, sensor fusion, and path planning',
    color: 'text-muted',
    unlocked: false,
  },
  {
    number: 4,
    slug: 'stage-4',
    title: 'AI Integration',
    description: 'Machine learning models and AI-driven behaviors',
    color: 'text-muted',
    unlocked: false,
  },
  {
    number: 5,
    slug: 'stage-5',
    title: 'Capstone Project',
    description: 'Build a complete autonomous robotics system',
    color: 'text-muted',
    unlocked: false,
  },
];

const docusaurusUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3005/AINativeBook';

export default function DashboardPage() {
  return (
    <main className="relative min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="relative py-32 overflow-hidden">
        {/* Ambient glow orbs */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-accent-blue/5 blur-[120px]"
        />
        <div
          aria-hidden="true"
          className="pointer-events-none absolute bottom-0 right-1/3 w-80 h-80 rounded-full bg-accent-violet/8 blur-[100px]"
        />

        <div className="container mx-auto px-4 relative z-10">
          <p className="font-mono text-accent-blue text-sm uppercase tracking-[0.2em] mb-4">
            Neural Command Center
          </p>
          <h1 className="text-5xl font-heading font-bold bg-gradient-to-r from-text-primary via-accent-blue to-accent-violet bg-clip-text text-transparent animate-fade-up mb-4">
            Mission Control
          </h1>
          <p className="text-text-secondary text-lg animate-fade-up max-w-xl" style={{ animationDelay: '100ms' }}>
            Track your progress through the Physical AI curriculum. Each stage unlocks the next frontier.
          </p>
        </div>
      </section>

      {/* Main Grid */}
      <div className="container mx-auto px-4 pb-24">
        <div className="grid grid-cols-12 gap-6">

          {/* Progress card — 8 cols */}
          <div className="col-span-12 lg:col-span-8 surface rounded-2xl p-8 space-y-6">
            <div>
              <p className="font-mono text-text-muted text-xs uppercase tracking-widest mb-2">Mission Status</p>
              <h2 className="text-2xl font-bold font-heading text-text-primary">
                Welcome back to the Lab
              </h2>
              <p className="text-text-secondary mt-1">
                You are on track with your robotics curriculum. Keep building!
              </p>
            </div>

            {/* Progress bar */}
            <div>
              <div className="flex justify-between text-sm text-text-muted mb-2">
                <span>Overall completion</span>
                <span className="text-accent-blue font-medium">2 / 5 stages</span>
              </div>
              <div className="h-2 bg-bg-elevated rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full bg-gradient-to-r from-accent-blue to-accent-emerald transition-all duration-slow"
                  style={{ width: '40%' }}
                />
              </div>
            </div>

            <Link
              href={`${docusaurusUrl}/stage-1/intro`}
              className="inline-flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-accent-blue to-accent-violet text-white rounded-xl font-semibold hover:shadow-glow-blue hover:scale-[1.02] transition-all"
            >
              Continue Learning
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </div>

          {/* Stats panel — 4 cols */}
          <div className="col-span-12 lg:col-span-4 surface rounded-2xl p-6 flex flex-col justify-between">
            <p className="font-mono text-text-muted text-xs uppercase tracking-widest mb-6">Field Stats</p>
            <div className="space-y-6">
              <StatRow label="Current streak" value="7 🔥" colorClass="text-accent-amber" />
              <StatRow label="Badges earned" value="3 🏅" colorClass="text-accent-violet" />
              <StatRow label="XP points" value="1,250" colorClass="text-accent-emerald" />
            </div>
          </div>

          {/* Stage cards — 4 cols each */}
          {stages.map((stage, i) => (
            <div
              key={stage.number}
              className="col-span-12 sm:col-span-6 lg:col-span-4 animate-entry-up"
              style={{ '--stagger-delay': `${i * 80}ms` } as React.CSSProperties}
            >
              {stage.unlocked ? (
                <Link
                  href={`${docusaurusUrl}/${stage.slug}/intro`}
                  className="flex flex-col h-full surface rounded-2xl p-6 group hover:border-accent-blue hover:shadow-glow-blue transition-all"
                >
                  <StageCardContent stage={stage} index={i} />
                </Link>
              ) : (
                <div className="flex flex-col h-full surface rounded-2xl p-6 opacity-40 cursor-not-allowed">
                  <StageCardContent stage={stage} index={i} locked />
                </div>
              )}
            </div>
          ))}

        </div>
      </div>

      <Footer />
    </main>
  );
}

const stageGradients: Record<number, string> = {
  1: 'from-accent-emerald/20 to-accent-emerald/5 text-accent-emerald border-accent-emerald/30',
  2: 'from-accent-blue/20 to-accent-blue/5 text-accent-blue border-accent-blue/30',
  3: 'from-bg-elevated to-bg-elevated text-text-muted border-border-subtle',
  4: 'from-bg-elevated to-bg-elevated text-text-muted border-border-subtle',
  5: 'from-bg-elevated to-bg-elevated text-text-muted border-border-subtle',
};

function StageCardContent({ stage, index, locked }: { stage: typeof stages[0]; index: number; locked?: boolean }) {
  return (
    <>
      <div className={`w-12 h-12 rounded-xl border bg-gradient-to-br flex items-center justify-center font-bold font-mono text-lg mb-4 ${stageGradients[stage.number]}`}>
        {locked ? '🔒' : stage.number}
      </div>
      <h3 className="font-semibold font-heading text-text-primary group-hover:text-accent-blue transition-colors mb-1">
        Stage {stage.number}: {stage.title}
      </h3>
      <p className="text-text-secondary text-sm flex-1">{stage.description}</p>
      {!locked && (
        <div className="mt-4 flex items-center gap-1 text-accent-blue text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
          Open stage
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
          </svg>
        </div>
      )}
      {locked && (
        <p className="mt-4 font-mono text-xs text-text-muted">🔒 Locked</p>
      )}
    </>
  );
}

function StatRow({ label, value, colorClass }: { label: string; value: string; colorClass: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-text-secondary text-sm">{label}</span>
      <span className={`text-3xl font-bold font-heading ${colorClass}`}>{value}</span>
    </div>
  );
}
