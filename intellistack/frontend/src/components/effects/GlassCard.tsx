'use client';

import React from 'react';

interface GlassCardProps {
  blur?: 'sm' | 'md' | 'lg';
  opacity?: number;
  border?: boolean;
  hover?: boolean;
  children: React.ReactNode;
  className?: string;
}

export function GlassCard({
  blur = 'md',
  opacity = 0.7,
  border = true,
  hover = false,
  children,
  className = '',
}: GlassCardProps) {
  const blurStyles = {
    sm: 'backdrop-blur-sm',
    md: 'backdrop-blur-md',
    lg: 'backdrop-blur-lg',
  };

  const baseStyles = 'rounded-lg transition-all duration-normal';
  const borderStyles = border ? 'border border-glass-border' : '';
  const hoverStyles = hover
    ? 'hover:bg-glass-highlight hover:border-accent-cyan hover:shadow-lg hover:shadow-glow-cyan'
    : '';

  return (
    <div
      className={`${baseStyles} ${blurStyles[blur]} ${borderStyles} ${hoverStyles} ${className}`}
      style={{
        background: `rgba(26, 26, 46, ${opacity})`,
        backdropFilter: `blur(${blur === 'sm' ? '8px' : blur === 'md' ? '12px' : '16px'}) saturate(180%)`,
        WebkitBackdropFilter: `blur(${blur === 'sm' ? '8px' : blur === 'md' ? '12px' : '16px'}) saturate(180%)`,
      }}
    >
      {children}
      <style jsx>{`
        @supports not (backdrop-filter: blur(12px)) {
          div {
            background: rgba(26, 26, 46, 0.95) !important;
          }
        }
      `}</style>
    </div>
  );
}
