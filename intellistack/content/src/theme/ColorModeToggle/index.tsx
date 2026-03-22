import React from 'react';

// Swizzle of Docusaurus ColorModeToggle — custom Sun/Moon SVG icons
// Follows Docusaurus swizzle convention: src/theme/[ComponentName]/index.tsx

interface Props {
  value: 'light' | 'dark';
  onChange: (value: 'light' | 'dark') => void;
  className?: string;
}

function SunIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  );
}

function MoonIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}

export default function ColorModeToggle({ value, onChange, className }: Props) {
  const isDark = value === 'dark';

  const handleToggle = () => {
    const next = isDark ? 'light' : 'dark';
    onChange(next);

    // Persist theme preference to backend if session exists
    try {
      const backendUrl = (window as any).__ENV__?.BACKEND_URL || 'http://localhost:8000';
      fetch(`${backendUrl}/api/v1/users/preferences/theme`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ theme: next }),
      }).catch(() => {/* silent — user may not be logged in */});
    } catch {
      // Silent — non-critical
    }
  };

  return (
    <button
      className={className}
      onClick={handleToggle}
      aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
      style={{
        background: 'none',
        border: 'none',
        cursor: 'pointer',
        padding: '6px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--ifm-font-color-base)',
        opacity: 0.65,
        transition: 'opacity 0.2s ease, color 0.2s ease',
        borderRadius: '6px',
        lineHeight: 0,
      }}
      onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.opacity = '1'; }}
      onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.opacity = '0.65'; }}
    >
      <span style={{ transition: 'opacity 0.2s ease' }}>
        {isDark ? <SunIcon /> : <MoonIcon />}
      </span>
    </button>
  );
}
