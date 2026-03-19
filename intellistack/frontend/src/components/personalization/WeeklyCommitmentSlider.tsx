'use client';

import React from 'react';
import { Slider } from '@/components/ui';

interface WeeklyCommitmentSliderProps {
  value: number;
  onChange: (hours: number) => void;
  className?: string;
}

export function WeeklyCommitmentSlider({ value, onChange, className = '' }: WeeklyCommitmentSliderProps) {
  const getCommitmentLabel = (hours: number) => {
    if (hours <= 3) return 'Light';
    if (hours <= 7) return 'Moderate';
    if (hours <= 14) return 'Intensive';
    return 'Full-time';
  };

  const getCommitmentDescription = (hours: number) => {
    if (hours <= 3) return 'Perfect for busy schedules';
    if (hours <= 7) return 'Steady progress each week';
    if (hours <= 14) return 'Accelerated learning path';
    return 'Immersive learning experience';
  };

  const marks = [
    { value: 1, label: '1h' },
    { value: 5, label: '5h' },
    { value: 10, label: '10h' },
    { value: 15, label: '15h' },
    { value: 20, label: '20h' },
  ];

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-text-primary">Weekly time commitment</h2>
        <p className="text-text-secondary">How many hours per week can you dedicate to learning?</p>
      </div>

      {/* Current Selection Display */}
      <div className="glass backdrop-blur-md rounded-xl p-8 border border-glass-border text-center space-y-4">
        <div className="space-y-2">
          <div className="text-6xl font-bold bg-gradient-to-r from-accent-cyan to-accent-violet bg-clip-text text-transparent">
            {value}
          </div>
          <div className="text-text-tertiary text-sm">hours per week</div>
        </div>

        <div className="space-y-1">
          <div className="text-xl font-semibold text-text-primary">
            {getCommitmentLabel(value)} Pace
          </div>
          <div className="text-text-secondary text-sm">
            {getCommitmentDescription(value)}
          </div>
        </div>

        {/* Estimated Completion Time */}
        <div className="pt-4 border-t border-glass-border">
          <div className="text-sm text-text-tertiary">
            Estimated completion:{' '}
            <span className="text-accent-cyan font-medium">
              {Math.ceil(100 / value)} weeks
            </span>
          </div>
        </div>
      </div>

      {/* Slider */}
      <div className="space-y-4">
        <Slider
          min={1}
          max={20}
          step={1}
          value={value}
          onChange={onChange}
          marks={marks}
          aria-label="Weekly time commitment in hours"
        />

        {/* Helper Text */}
        <div className="flex items-start space-x-2 text-sm text-text-tertiary">
          <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p>
            You can adjust this anytime. We'll recommend content that fits your schedule and help you stay on track.
          </p>
        </div>
      </div>

      {/* Commitment Level Indicators */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { range: '1-3h', label: 'Light', color: 'from-green-500 to-teal-500' },
          { range: '4-7h', label: 'Moderate', color: 'from-accent-teal to-accent-cyan' },
          { range: '8-14h', label: 'Intensive', color: 'from-accent-cyan to-accent-violet' },
          { range: '15-20h', label: 'Full-time', color: 'from-accent-violet to-pink-500' },
        ].map((level, i) => (
          <div
            key={i}
            className="glass backdrop-blur-md rounded-lg p-3 border border-glass-border text-center space-y-1"
          >
            <div className={`w-full h-1 rounded-full bg-gradient-to-r ${level.color}`} />
            <div className="text-xs font-medium text-text-primary">{level.label}</div>
            <div className="text-xs text-text-tertiary">{level.range}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
