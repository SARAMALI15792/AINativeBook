'use client';

import React, { useId } from 'react';

type TriangleLoaderProps = {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'inline' | 'page';
  className?: string;
};

const SIZES = { sm: 16, md: 32, lg: 64 } as const;

function TriangleSVG({ px, gradientId }: { px: number; gradientId: string }) {
  // Equilateral triangle inscribed in circle of radius r, centered in viewBox
  const r = px * 0.38;
  const cx = px / 2;
  const cy = px / 2;
  const v1x = cx;
  const v1y = cy - r;
  const v2x = cx + r * Math.sqrt(3) / 2;
  const v2y = cy + r / 2;
  const v3x = cx - r * Math.sqrt(3) / 2;
  const v3y = cy + r / 2;
  const side = r * Math.sqrt(3);
  const perimeter = Math.round(side * 3);
  const sw = px >= 64 ? 2.5 : px >= 32 ? 2 : 1.5;
  const animId = `tl-${gradientId}`;

  return (
    <svg
      width={px}
      height={px}
      viewBox={`0 0 ${px} ${px}`}
      aria-hidden="true"
    >
      <style>{`
        @keyframes ${animId}-draw {
          0%   { stroke-dashoffset: ${perimeter}; }
          50%  { stroke-dashoffset: 0; }
          100% { stroke-dashoffset: ${-perimeter}; }
        }
        @keyframes ${animId}-pulse {
          0%, 100% { transform: scale(0.95); }
          50%       { transform: scale(1.05); }
        }
        .${animId}-svg {
          animation: ${animId}-pulse 1.5s ease-in-out infinite;
          transform-origin: center;
          transform-box: fill-box;
        }
        .${animId}-path {
          stroke-dasharray: ${perimeter};
          stroke-dashoffset: ${perimeter};
          animation: ${animId}-draw 1.5s ease-in-out infinite;
        }
      `}</style>
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%"   stopColor="#4f46e5" />
          <stop offset="50%"  stopColor="#6366f1" />
          <stop offset="100%" stopColor="#a78bfa" />
        </linearGradient>
      </defs>
      <g className={`${animId}-svg`}>
        <path
          d={`M ${v1x.toFixed(2)},${v1y.toFixed(2)} L ${v2x.toFixed(2)},${v2y.toFixed(2)} L ${v3x.toFixed(2)},${v3y.toFixed(2)} Z`}
          fill="none"
          stroke={`url(#${gradientId})`}
          strokeWidth={sw}
          strokeLinecap="round"
          strokeLinejoin="round"
          className={`${animId}-path`}
        />
      </g>
    </svg>
  );
}

export function TriangleLoader({ size = 'md', variant = 'inline', className = '' }: TriangleLoaderProps) {
  const uid = useId().replace(/:/g, '');
  const px = SIZES[size];
  const gradientId = `tl-g-${uid}-${size}`;

  const svg = <TriangleSVG px={px} gradientId={gradientId} />;

  if (variant === 'page') {
    return (
      <div
        className={className}
        style={{
          position: 'fixed',
          inset: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'rgba(13, 13, 18, 0.85)',
          backdropFilter: 'blur(8px)',
          zIndex: 9998,
        }}
        role="status"
        aria-label="Loading"
      >
        <TriangleSVG px={SIZES.lg} gradientId={`${gradientId}-page`} />
      </div>
    );
  }

  return (
    <span className={className} role="status" aria-label="Loading">
      {svg}
    </span>
  );
}
