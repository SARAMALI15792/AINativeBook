'use client';

import React from 'react';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  className?: string;
}

export function FeatureCard({ icon, title, description, className = '' }: FeatureCardProps) {
  return (
    <div
      className={`group surface rounded-2xl p-6 transition-all duration-normal hover:border-accent-blue hover:shadow-glow-blue ${className}`}
    >
      <div className="space-y-4">
        {/* Icon container */}
        <div className="w-14 h-14 rounded-xl bg-accent-blue/10 border border-accent-blue/20 flex items-center justify-center group-hover:bg-accent-blue/20 transition-all">
          {icon}
        </div>

        {/* Title */}
        <h3 className="text-xl font-bold font-heading text-text-primary">{title}</h3>

        {/* Description */}
        <p className="text-text-secondary leading-relaxed text-sm">{description}</p>
      </div>
    </div>
  );
}
