'use client';

import React from 'react';

interface CardProps {
  variant?: 'default' | 'glass' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
}

export function Card({
  variant = 'default',
  padding = 'md',
  hover = false,
  onClick,
  children,
  className = '',
}: CardProps) {
  const baseStyles = 'rounded-lg transition-all duration-normal';

  const variantStyles = {
    default: 'bg-bg-secondary border border-glass-border shadow-md',
    glass: 'glass',
    elevated: 'bg-bg-secondary shadow-lg hover:shadow-xl',
  };

  const paddingStyles = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
  };

  const hoverStyles = hover
    ? 'cursor-pointer hover:scale-105 hover:shadow-glow-cyan'
    : '';

  const clickableStyles = onClick ? 'cursor-pointer' : '';

  return (
    <div
      onClick={onClick}
      className={`${baseStyles} ${variantStyles[variant]} ${paddingStyles[padding]} ${hoverStyles} ${clickableStyles} ${className}`}
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
    >
      {children}
    </div>
  );
}
