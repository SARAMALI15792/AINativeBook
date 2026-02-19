'use client';

import React from 'react';
import { GlassCard } from '@/components/effects/GlassCard';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  className?: string;
}

export function FeatureCard({ icon, title, description, className = '' }: FeatureCardProps) {
  return (
    <GlassCard
      blur="md"
      opacity={0.7}
      border={true}
      hover={true}
      className={`p-6 transition-all duration-normal ${className}`}
    >
      <div className="space-y-4">
        {/* Icon */}
        <div className="w-14 h-14 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center shadow-glow-cyan">
          {icon}
        </div>

        {/* Title */}
        <h3 className="text-2xl font-bold text-text-primary">{title}</h3>

        {/* Description */}
        <p className="text-text-secondary leading-relaxed">{description}</p>
      </div>
    </GlassCard>
  );
}
