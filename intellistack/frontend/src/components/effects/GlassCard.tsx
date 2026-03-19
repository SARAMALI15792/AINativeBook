'use client';

import React from 'react';

interface GlassCardProps {
  blur?: 'sm' | 'md' | 'lg';
  border?: boolean;
  hover?: boolean;
  children: React.ReactNode;
  className?: string;
}

export function GlassCard({
  blur = 'md',
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

  const baseStyles = 'bg-bg-secondary rounded-lg transition-all duration-normal';
  const borderStyles = border ? 'border border-border-default' : '';
  const hoverStyles = hover
    ? 'hover:border-accent-blue hover:shadow-glow-blue cursor-pointer'
    : '';

  return (
    <div
      className={`${baseStyles} ${blurStyles[blur]} ${borderStyles} ${hoverStyles} ${className}`}
    >
      {children}
    </div>
  );
}
