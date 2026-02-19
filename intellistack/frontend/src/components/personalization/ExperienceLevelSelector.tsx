'use client';

import React from 'react';
import { GlassCard } from '@/components/effects/GlassCard';
import { ExperienceLevel } from '@/types/api';

interface ExperienceLevelOption {
  value: ExperienceLevel;
  label: string;
  description: string;
  skills: string[];
}

interface ExperienceLevelSelectorProps {
  value?: ExperienceLevel;
  onChange: (level: ExperienceLevel) => void;
  className?: string;
}

export function ExperienceLevelSelector({ value, onChange, className = '' }: ExperienceLevelSelectorProps) {
  const levels: ExperienceLevelOption[] = [
    {
      value: ExperienceLevel.BEGINNER,
      label: 'Beginner',
      description: 'New to robotics and programming',
      skills: ['Basic programming', 'No ROS experience', 'Learning fundamentals'],
    },
    {
      value: ExperienceLevel.INTERMEDIATE,
      label: 'Intermediate',
      description: 'Some robotics or programming experience',
      skills: ['Python/C++ basics', 'Some ROS knowledge', 'Built simple projects'],
    },
    {
      value: ExperienceLevel.ADVANCED,
      label: 'Advanced',
      description: 'Experienced in robotics and AI',
      skills: ['Strong programming', 'ROS 2 proficient', 'Complex projects'],
    },
  ];

  const getLevelColor = (level: ExperienceLevel) => {
    switch (level) {
      case ExperienceLevel.BEGINNER:
        return 'from-green-500 to-teal-500';
      case ExperienceLevel.INTERMEDIATE:
        return 'from-accent-cyan to-accent-violet';
      case ExperienceLevel.ADVANCED:
        return 'from-accent-violet to-pink-500';
    }
  };

  const getLevelIndicator = (level: ExperienceLevel) => {
    switch (level) {
      case ExperienceLevel.BEGINNER:
        return 1;
      case ExperienceLevel.INTERMEDIATE:
        return 2;
      case ExperienceLevel.ADVANCED:
        return 3;
    }
  };

  return (
    <div className={`space-y-4 ${className}`}>
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-text-primary">What's your experience level?</h2>
        <p className="text-text-secondary">We'll adjust the curriculum to match your skills</p>
      </div>

      <div className="space-y-4">
        {levels.map((level) => {
          const isSelected = value === level.value;
          const levelNum = getLevelIndicator(level.value);

          return (
            <button
              key={level.value}
              onClick={() => onChange(level.value)}
              className="w-full text-left focus:outline-none focus:ring-2 focus:ring-accent-cyan rounded-lg"
            >
              <GlassCard
                blur="md"
                opacity={0.7}
                border={true}
                hover={true}
                className={`p-6 transition-all duration-normal ${
                  isSelected ? 'border-accent-cyan shadow-glow-cyan' : 'border-glass-border'
                }`}
              >
                <div className="flex items-start space-x-4">
                  {/* Level Indicator */}
                  <div className="flex-shrink-0">
                    <div
                      className={`w-16 h-16 rounded-lg flex items-center justify-center bg-gradient-to-br ${
                        isSelected ? getLevelColor(level.value) : 'from-glass-highlight to-glass-highlight'
                      }`}
                    >
                      <div className="flex space-x-1">
                        {Array.from({ length: 3 }).map((_, i) => (
                          <div
                            key={i}
                            className={`w-1.5 rounded-full transition-all ${
                              i < levelNum
                                ? 'h-8 bg-white'
                                : 'h-4 bg-white/30'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="flex-1 space-y-3">
                    <div>
                      <h3 className="text-xl font-semibold text-text-primary mb-1">
                        {level.label}
                      </h3>
                      <p className="text-text-secondary text-sm">{level.description}</p>
                    </div>

                    {/* Skills */}
                    <div className="flex flex-wrap gap-2">
                      {level.skills.map((skill, i) => (
                        <span
                          key={i}
                          className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                            isSelected
                              ? 'bg-accent-cyan/20 text-accent-cyan'
                              : 'bg-glass-highlight text-text-tertiary'
                          }`}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>

                    {/* Selected Indicator */}
                    {isSelected && (
                      <div className="flex items-center space-x-2 text-accent-cyan pt-2">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                          <path
                            fillRule="evenodd"
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                            clipRule="evenodd"
                          />
                        </svg>
                        <span className="text-sm font-medium">Selected</span>
                      </div>
                    )}
                  </div>
                </div>
              </GlassCard>
            </button>
          );
        })}
      </div>
    </div>
  );
}
