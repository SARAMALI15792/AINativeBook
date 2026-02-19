'use client';

import React, { useEffect, useState } from 'react';

interface Robot2DProps {
  className?: string;
  animate?: boolean;
}

export function Robot2D({ className = '', animate = true }: Robot2DProps) {
  const [isVisible, setIsVisible] = useState(true);

  // Page Visibility API - pause animations when tab is inactive
  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsVisible(!document.hidden);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
  }, []);

  const shouldAnimate = animate && isVisible;

  return (
    <div
      className={`w-full h-full flex items-center justify-center ${className}`}
      role="img"
      aria-label="2D animated humanoid robot illustration with glowing effects"
    >
      <svg
        viewBox="0 0 200 300"
        className="w-full h-full max-w-md"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="robotGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#00efff', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#14b8a6', stopOpacity: 1 }} />
          </linearGradient>
          <linearGradient id="robotGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#a855f7', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#00efff', stopOpacity: 1 }} />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Head */}
        <rect
          x="70"
          y="40"
          width="60"
          height="60"
          rx="8"
          fill="url(#robotGrad1)"
          filter="url(#glow)"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="40;35;40"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Antenna */}
        <line
          x1="100"
          y1="40"
          x2="100"
          y2="20"
          stroke="#00efff"
          strokeWidth="3"
          strokeLinecap="round"
        >
          {shouldAnimate && (
            <animate
              attributeName="y1"
              values="40;35;40"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </line>
        <circle cx="100" cy="20" r="5" fill="#a855f7" filter="url(#glow)">
          {shouldAnimate && (
            <animate
              attributeName="opacity"
              values="0.6;1;0.6"
              dur="1.5s"
              repeatCount="indefinite"
            />
          )}
        </circle>

        {/* Left Eye */}
        <circle cx="85" cy="65" r="8" fill="#a855f7" filter="url(#glow)">
          {shouldAnimate && (
            <>
              <animate
                attributeName="cy"
                values="65;60;65"
                dur="2s"
                repeatCount="indefinite"
              />
              <animate
                attributeName="opacity"
                values="0.8;1;0.8"
                dur="1s"
                repeatCount="indefinite"
              />
            </>
          )}
        </circle>

        {/* Right Eye */}
        <circle cx="115" cy="65" r="8" fill="#a855f7" filter="url(#glow)">
          {shouldAnimate && (
            <>
              <animate
                attributeName="cy"
                values="65;60;65"
                dur="2s"
                repeatCount="indefinite"
              />
              <animate
                attributeName="opacity"
                values="0.8;1;0.8"
                dur="1s"
                repeatCount="indefinite"
              />
            </>
          )}
        </circle>

        {/* Body */}
        <rect
          x="60"
          y="110"
          width="80"
          height="100"
          rx="10"
          fill="url(#robotGrad2)"
          filter="url(#glow)"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="110;105;110"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Chest Panel */}
        <rect
          x="80"
          y="130"
          width="40"
          height="60"
          rx="5"
          fill="#1a1a2e"
          opacity="0.5"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="130;125;130"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Left Arm */}
        <rect
          x="40"
          y="120"
          width="15"
          height="60"
          rx="7"
          fill="url(#robotGrad1)"
        >
          {shouldAnimate && (
            <animateTransform
              attributeName="transform"
              type="rotate"
              values="0 47.5 120; -10 47.5 120; 0 47.5 120"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Left Hand */}
        <circle cx="47.5" cy="185" r="10" fill="#a855f7" filter="url(#glow)">
          {shouldAnimate && (
            <animateTransform
              attributeName="transform"
              type="rotate"
              values="0 47.5 120; -10 47.5 120; 0 47.5 120"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </circle>

        {/* Right Arm */}
        <rect
          x="145"
          y="120"
          width="15"
          height="60"
          rx="7"
          fill="url(#robotGrad1)"
        >
          {shouldAnimate && (
            <animateTransform
              attributeName="transform"
              type="rotate"
              values="0 152.5 120; 10 152.5 120; 0 152.5 120"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Right Hand */}
        <circle cx="152.5" cy="185" r="10" fill="#a855f7" filter="url(#glow)">
          {shouldAnimate && (
            <animateTransform
              attributeName="transform"
              type="rotate"
              values="0 152.5 120; 10 152.5 120; 0 152.5 120"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </circle>

        {/* Left Leg */}
        <rect
          x="70"
          y="215"
          width="20"
          height="60"
          rx="5"
          fill="url(#robotGrad2)"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="215;210;215"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Left Foot */}
        <rect
          x="65"
          y="270"
          width="30"
          height="15"
          rx="5"
          fill="#00efff"
          filter="url(#glow)"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="270;265;270"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Right Leg */}
        <rect
          x="110"
          y="215"
          width="20"
          height="60"
          rx="5"
          fill="url(#robotGrad2)"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="215;210;215"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>

        {/* Right Foot */}
        <rect
          x="105"
          y="270"
          width="30"
          height="15"
          rx="5"
          fill="#00efff"
          filter="url(#glow)"
        >
          {shouldAnimate && (
            <animate
              attributeName="y"
              values="270;265;270"
              dur="2s"
              repeatCount="indefinite"
            />
          )}
        </rect>
      </svg>
    </div>
  );
}
