'use client';

import React from 'react';
import { GlassCard } from '@/components/effects/GlassCard';
import { LearningGoal } from '@/types/api';

interface LearningGoalOption {
  value: LearningGoal;
  label: string;
  description: string;
  icon: React.ReactNode;
}

interface LearningGoalSelectorProps {
  value?: LearningGoal;
  onChange: (goal: LearningGoal) => void;
  className?: string;
}

export function LearningGoalSelector({ value, onChange, className = '' }: LearningGoalSelectorProps) {
  const goals: LearningGoalOption[] = [
    {
      value: LearningGoal.CAREER_TRANSITION,
      label: 'Career Transition',
      description: 'Switch to robotics engineering or AI development',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
    },
    {
      value: LearningGoal.ACADEMIC_RESEARCH,
      label: 'Academic Research',
      description: 'Pursue graduate studies or research in robotics',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      ),
    },
    {
      value: LearningGoal.HOBBY_PROJECT,
      label: 'Hobby Project',
      description: 'Build robots for fun and personal projects',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    {
      value: LearningGoal.SKILL_ENHANCEMENT,
      label: 'Skill Enhancement',
      description: 'Expand existing skills in robotics or AI',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      ),
    },
  ];

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-text-primary">What's your learning goal?</h2>
        <p className="text-text-secondary">This helps us personalize your learning path</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {goals.map((goal) => (
          <button
            key={goal.value}
            onClick={() => onChange(goal.value)}
            className="text-left focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded-lg"
          >
            <GlassCard
              blur="md"
              opacity={0.7}
              border={true}
              hover={true}
              className={`p-6 transition-all duration-normal ${
                value === goal.value
                  ? 'border-accent-cyan shadow-glow-cyan'
                  : 'border-glass-border'
              }`}
            >
              <div className="space-y-4">
                <div
                  className={`w-14 h-14 rounded-lg flex items-center justify-center transition-all ${
                    value === goal.value
                      ? 'bg-gradient-to-br from-accent-cyan to-accent-violet text-white'
                      : 'bg-glass-highlight text-text-tertiary'
                  }`}
                >
                  {goal.icon}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-text-primary mb-2">{goal.label}</h3>
                  <p className="text-text-secondary text-sm">{goal.description}</p>
                </div>
                {value === goal.value && (
                  <div className="flex items-center space-x-2 text-accent-cyan">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="text-sm font-medium">Selected</span>
                  </div>
                )}
              </div>
            </GlassCard>
          </button>
        ))}
      </div>
    </div>
  );
}
