import React from 'react';

type TriangleLoaderProps = {
  size?: 'sm' | 'md' | 'lg';
  variant?: 'inline' | 'page';
  className?: string;
};

const SIZES = { sm: 16, md: 32, lg: 64 } as const;

let _uid = 0;

function TriangleSVG({ px, uid }: { px: number; uid: string }) {
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
  const gradId = `tl-g-${uid}`;
  const animId = `tl-a-${uid}`;

  return (
    <svg width={px} height={px} viewBox={`0 0 ${px} ${px}`} aria-hidden="true">
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
        .${animId}-group {
          animation: ${animId}-pulse 1.5s ease-in-out infinite;
          transform-origin: ${cx}px ${cy}px;
        }
        .${animId}-path {
          stroke-dasharray: ${perimeter};
          stroke-dashoffset: ${perimeter};
          animation: ${animId}-draw 1.5s ease-in-out infinite;
        }
      `}</style>
      <defs>
        <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%"   stopColor="#4f46e5" />
          <stop offset="50%"  stopColor="#6366f1" />
          <stop offset="100%" stopColor="#a78bfa" />
        </linearGradient>
      </defs>
      <g className={`${animId}-group`}>
        <path
          d={`M ${v1x.toFixed(1)},${v1y.toFixed(1)} L ${v2x.toFixed(1)},${v2y.toFixed(1)} L ${v3x.toFixed(1)},${v3y.toFixed(1)} Z`}
          fill="none"
          stroke={`url(#${gradId})`}
          strokeWidth={sw}
          strokeLinecap="round"
          strokeLinejoin="round"
          className={`${animId}-path`}
        />
      </g>
    </svg>
  );
}

export default function TriangleLoader({ size = 'md', variant = 'inline', className = '' }: TriangleLoaderProps) {
  const [uid] = React.useState(() => `${++_uid}`);
  const px = SIZES[size];

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
          WebkitBackdropFilter: 'blur(8px)',
          zIndex: 9998,
        }}
        role="status"
        aria-label="Loading"
      >
        <TriangleSVG px={SIZES.lg} uid={`${uid}-page`} />
      </div>
    );
  }

  return (
    <span className={className} role="status" aria-label="Loading" style={{ display: 'inline-flex' }}>
      <TriangleSVG px={px} uid={uid} />
    </span>
  );
}
