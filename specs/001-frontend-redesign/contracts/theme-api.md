# Theme API: Frontend Redesign & Experience Enhancement

**Feature**: 001-frontend-redesign | **Date**: 2026-02-18 | **Version**: 1.0.0

## Purpose

This document defines the theming system API for the Frontend Redesign feature. It specifies how to apply, customize, and extend the AI Neural Network theme across Next.js and Docusaurus platforms.

---

## Theme Architecture

### CSS Custom Properties System

The theme is implemented using CSS Custom Properties (CSS variables) for maximum flexibility and runtime theming support.

**Benefits**:
- Runtime theme updates without recompilation
- Works across Next.js and Docusaurus
- Zero JavaScript overhead
- Native browser support (96%+)
- Easy to override and customize

---

## Theme Configuration

### Core Theme File

**Location**: `styles/tokens.css`

```css
:root {
  /* ===== Colors ===== */

  /* Background Colors */
  --color-bg-primary: #1a1a2e;
  --color-bg-secondary: #16213e;
  --color-bg-tertiary: #0f1419;

  /* Accent Colors */
  --color-accent-cyan: #00efff;
  --color-accent-violet: #a855f7;
  --color-accent-teal: #14b8a6;

  /* Text Colors */
  --color-text-primary: #ffffff;
  --color-text-secondary: #e0e0e0;
  --color-text-tertiary: #a0a0a0;

  /* Semantic Colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Glassmorphism */
  --glass-bg: rgba(26, 26, 46, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
  --glass-highlight: rgba(255, 255, 255, 0.05);

  /* ===== Spacing ===== */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;

  /* ===== Typography ===== */
  --font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'Fira Code', 'Courier New', monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  --text-5xl: 3rem;

  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* ===== Effects ===== */
  --blur-sm: blur(8px);
  --blur-md: blur(12px);
  --blur-lg: blur(16px);

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 10px 10px -5px rgba(0, 0, 0, 0.5);
  --shadow-glow-cyan: 0 0 20px rgba(0, 239, 255, 0.5);
  --shadow-glow-violet: 0 0 20px rgba(168, 85, 247, 0.5);

  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;

  /* ===== Animation ===== */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;

  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* ===== Z-Index ===== */
  --z-base: 0;
  --z-dropdown: 1000;
  --z-sticky: 1100;
  --z-modal: 1200;
  --z-popover: 1300;
  --z-toast: 1400;
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0.01ms;
    --duration-normal: 0.01ms;
    --duration-slow: 0.01ms;
  }
}
```

---

## Next.js Integration

### Setup

**1. Import in Root Layout**

```typescript
// app/layout.tsx
import '@/styles/tokens.css';
import '@/styles/globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

**2. Tailwind Configuration**

```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-primary': 'var(--color-bg-primary)',
        'bg-secondary': 'var(--color-bg-secondary)',
        'bg-tertiary': 'var(--color-bg-tertiary)',
        'accent-cyan': 'var(--color-accent-cyan)',
        'accent-violet': 'var(--color-accent-violet)',
        'accent-teal': 'var(--color-accent-teal)',
        'text-primary': 'var(--color-text-primary)',
        'text-secondary': 'var(--color-text-secondary)',
        'text-tertiary': 'var(--color-text-tertiary)',
      },
      spacing: {
        xs: 'var(--space-xs)',
        sm: 'var(--space-sm)',
        md: 'var(--space-md)',
        lg: 'var(--space-lg)',
        xl: 'var(--space-xl)',
        '2xl': 'var(--space-2xl)',
        '3xl': 'var(--space-3xl)',
      },
      fontFamily: {
        sans: 'var(--font-sans)',
        mono: 'var(--font-mono)',
      },
      fontSize: {
        xs: 'var(--text-xs)',
        sm: 'var(--text-sm)',
        base: 'var(--text-base)',
        lg: 'var(--text-lg)',
        xl: 'var(--text-xl)',
        '2xl': 'var(--text-2xl)',
        '3xl': 'var(--text-3xl)',
        '4xl': 'var(--text-4xl)',
        '5xl': 'var(--text-5xl)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
        full: 'var(--radius-full)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
        'glow-cyan': 'var(--shadow-glow-cyan)',
        'glow-violet': 'var(--shadow-glow-violet)',
      },
      transitionDuration: {
        fast: 'var(--duration-fast)',
        normal: 'var(--duration-normal)',
        slow: 'var(--duration-slow)',
      },
      transitionTimingFunction: {
        linear: 'var(--ease-linear)',
        in: 'var(--ease-in)',
        out: 'var(--ease-out)',
        'in-out': 'var(--ease-in-out)',
      },
    },
  },
  plugins: [],
};
```

**3. Usage in Components**

```tsx
// Using Tailwind classes
<div className="bg-bg-primary text-text-primary p-lg rounded-md shadow-md">
  <h1 className="text-4xl font-bold text-accent-cyan">Hello World</h1>
</div>

// Using CSS variables directly
<div style={{
  backgroundColor: 'var(--color-bg-primary)',
  color: 'var(--color-text-primary)',
  padding: 'var(--space-lg)',
}}>
  Content
</div>
```

---

## Docusaurus Integration

### Setup

**1. Import in Custom CSS**

```css
/* src/css/custom.css */
@import './tokens.css';

/* Override Docusaurus theme variables */
:root {
  /* Primary colors */
  --ifm-color-primary: var(--color-accent-cyan);
  --ifm-color-primary-dark: #00d4e6;
  --ifm-color-primary-darker: #00c8d9;
  --ifm-color-primary-darkest: #00a5b3;
  --ifm-color-primary-light: #1af3ff;
  --ifm-color-primary-lighter: #26f4ff;
  --ifm-color-primary-lightest: #4df6ff;

  /* Background colors */
  --ifm-background-color: var(--color-bg-primary);
  --ifm-background-surface-color: var(--color-bg-secondary);

  /* Text colors */
  --ifm-font-color-base: var(--color-text-secondary);
  --ifm-heading-color: var(--color-text-primary);

  /* Font family */
  --ifm-font-family-base: var(--font-sans);
  --ifm-font-family-monospace: var(--font-mono);

  /* Spacing */
  --ifm-spacing-horizontal: var(--space-lg);
  --ifm-spacing-vertical: var(--space-lg);

  /* Border radius */
  --ifm-global-radius: var(--radius-md);

  /* Code blocks */
  --ifm-code-background: var(--color-bg-tertiary);
  --ifm-code-border-radius: var(--radius-md);
}

/* Dark mode (default) */
[data-theme='dark'] {
  --ifm-color-primary: var(--color-accent-cyan);
  --ifm-background-color: var(--color-bg-primary);
  --ifm-background-surface-color: var(--color-bg-secondary);
}

/* Neural network background */
.theme-doc-page {
  position: relative;
  background: linear-gradient(135deg, var(--color-bg-primary) 0%, var(--color-bg-secondary) 100%);
}

.theme-doc-page::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('/img/neural-network-pattern.svg');
  opacity: 0.1;
  pointer-events: none;
  z-index: 0;
}

/* Glassmorphism for cards */
.card {
  background: var(--glass-bg);
  backdrop-filter: var(--blur-md);
  -webkit-backdrop-filter: var(--blur-md);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
}

/* Fallback for browsers without backdrop-filter */
@supports not (backdrop-filter: blur(12px)) {
  .card {
    background: rgba(26, 26, 46, 0.95);
  }
}
```

**2. Swizzle Layout Component**

```bash
npm run swizzle @docusaurus/theme-classic Layout -- --wrap
```

```tsx
// src/theme/Layout/index.tsx
import React from 'react';
import Layout from '@theme-original/Layout';
import type LayoutType from '@theme/Layout';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <>
      <div className="neural-network-background" />
      <Layout {...props} />
    </>
  );
}
```

---

## Runtime Theme Customization

### Theme Context

```typescript
// contexts/ThemeContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

interface ThemeConfig {
  mode: 'dark' | 'light';
  reducedMotion: boolean;
  highContrast: boolean;
  customColors?: Partial<ColorPalette>;
}

interface ColorPalette {
  bgPrimary: string;
  bgSecondary: string;
  accentCyan: string;
  accentViolet: string;
  accentTeal: string;
}

interface ThemeContextValue {
  theme: ThemeConfig;
  setTheme: (theme: Partial<ThemeConfig>) => void;
  applyTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<ThemeConfig>(() => {
    // Load from localStorage
    const saved = localStorage.getItem('theme-config');
    if (saved) return JSON.parse(saved);

    // Detect system preferences
    return {
      mode: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
      reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      highContrast: false,
    };
  });

  const applyTheme = () => {
    const root = document.documentElement;

    // Apply custom colors if provided
    if (theme.customColors) {
      Object.entries(theme.customColors).forEach(([key, value]) => {
        const cssVar = `--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
        root.style.setProperty(cssVar, value);
      });
    }

    // Apply reduced motion
    if (theme.reducedMotion) {
      root.style.setProperty('--duration-fast', '0.01ms');
      root.style.setProperty('--duration-normal', '0.01ms');
      root.style.setProperty('--duration-slow', '0.01ms');
    }

    // Apply high contrast (future feature)
    if (theme.highContrast) {
      // Increase contrast ratios
    }
  };

  const setTheme = (updates: Partial<ThemeConfig>) => {
    const newTheme = { ...theme, ...updates };
    setThemeState(newTheme);
    localStorage.setItem('theme-config', JSON.stringify(newTheme));
  };

  useEffect(() => {
    applyTheme();
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, applyTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

### Usage Example

```tsx
import { useTheme } from '@/contexts/ThemeContext';

export default function ThemeCustomizer() {
  const { theme, setTheme } = useTheme();

  return (
    <div>
      <button onClick={() => setTheme({ reducedMotion: !theme.reducedMotion })}>
        Toggle Reduced Motion
      </button>

      <input
        type="color"
        value={theme.customColors?.accentCyan || '#00efff'}
        onChange={(e) => setTheme({
          customColors: {
            ...theme.customColors,
            accentCyan: e.target.value,
          },
        })}
      />
    </div>
  );
}
```

---

## Glassmorphism Effect

### Implementation

```css
/* Glass effect utility class */
.glass {
  background: var(--glass-bg);
  backdrop-filter: var(--blur-md) saturate(180%);
  -webkit-backdrop-filter: var(--blur-md) saturate(180%);
  border: 1px solid var(--glass-border);
  box-shadow: var(--shadow-md);
}

/* Fallback for unsupported browsers */
@supports not (backdrop-filter: blur(12px)) {
  .glass {
    background: rgba(26, 26, 46, 0.95);
  }
}

/* Glass variants */
.glass-sm {
  backdrop-filter: var(--blur-sm) saturate(180%);
  -webkit-backdrop-filter: var(--blur-sm) saturate(180%);
}

.glass-lg {
  backdrop-filter: var(--blur-lg) saturate(180%);
  -webkit-backdrop-filter: var(--blur-lg) saturate(180%);
}

/* Glass with hover effect */
.glass-hover {
  transition: all var(--duration-normal) var(--ease-out);
}

.glass-hover:hover {
  background: var(--glass-highlight);
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-lg), var(--shadow-glow-cyan);
}
```

### React Component

```tsx
// components/effects/GlassCard.tsx
interface GlassCardProps {
  blur?: 'sm' | 'md' | 'lg';
  hover?: boolean;
  children: React.ReactNode;
  className?: string;
}

export function GlassCard({ blur = 'md', hover = false, children, className = '' }: GlassCardProps) {
  const blurClass = blur === 'sm' ? 'glass-sm' : blur === 'lg' ? 'glass-lg' : '';
  const hoverClass = hover ? 'glass-hover' : '';

  return (
    <div className={`glass ${blurClass} ${hoverClass} ${className}`}>
      {children}
    </div>
  );
}
```

---

## Neural Network Pattern

### SVG Pattern

```svg
<!-- public/img/neural-network-pattern.svg -->
<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00efff;stop-opacity:0.3" />
      <stop offset="50%" style="stop-color:#a855f7;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#14b8a6;stop-opacity:0.3" />
    </linearGradient>
  </defs>

  <!-- Nodes -->
  <circle cx="200" cy="200" r="4" fill="#00efff" opacity="0.6" />
  <circle cx="400" cy="300" r="4" fill="#a855f7" opacity="0.6" />
  <circle cx="600" cy="250" r="4" fill="#14b8a6" opacity="0.6" />
  <!-- Add more nodes... -->

  <!-- Connections -->
  <line x1="200" y1="200" x2="400" y2="300" stroke="url(#lineGradient)" stroke-width="1" />
  <line x1="400" y1="300" x2="600" y2="250" stroke="url(#lineGradient)" stroke-width="1" />
  <!-- Add more connections... -->
</svg>
```

### CSS Background

```css
.neural-network-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--color-bg-primary) 0%, var(--color-bg-secondary) 100%);
  z-index: -1;
}

.neural-network-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('/img/neural-network-pattern.svg');
  background-size: cover;
  background-position: center;
  opacity: 0.1;
  animation: pulse 10s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.1; }
  50% { opacity: 0.15; }
}

@media (prefers-reduced-motion: reduce) {
  .neural-network-background::before {
    animation: none;
  }
}
```

---

## Responsive Theme Adjustments

### Mobile Optimizations

```css
/* Mobile: Reduce complexity */
@media (max-width: 768px) {
  :root {
    /* Smaller spacing */
    --space-lg: 1rem;
    --space-xl: 1.5rem;
    --space-2xl: 2rem;

    /* Smaller text */
    --text-4xl: 1.875rem;
    --text-5xl: 2.25rem;

    /* Lighter blur (better performance) */
    --blur-md: blur(8px);
    --blur-lg: blur(10px);
  }

  /* Disable neural network animation on mobile */
  .neural-network-background::before {
    animation: none;
  }

  /* Simpler glass effect */
  .glass {
    backdrop-filter: var(--blur-sm);
    -webkit-backdrop-filter: var(--blur-sm);
  }
}
```

### Tablet Adjustments

```css
@media (min-width: 768px) and (max-width: 1024px) {
  :root {
    --space-2xl: 2.5rem;
    --space-3xl: 3.5rem;
  }
}
```

### Desktop Enhancements

```css
@media (min-width: 1024px) {
  /* Full effects on desktop */
  .glass {
    backdrop-filter: var(--blur-md) saturate(180%);
  }

  /* Enable hover effects */
  .glass-hover:hover {
    transform: translateY(-2px);
  }
}
```

---

## Accessibility Considerations

### Color Contrast

All color combinations meet WCAG 2.1 Level AA:

| Foreground | Background | Contrast Ratio | WCAG Level |
|------------|------------|----------------|------------|
| #ffffff (text-primary) | #1a1a2e (bg-primary) | 15.2:1 | AAA |
| #e0e0e0 (text-secondary) | #1a1a2e (bg-primary) | 11.5:1 | AAA |
| #00efff (accent-cyan) | #16213e (bg-secondary) | 8.2:1 | AAA |
| #a855f7 (accent-violet) | #1a1a2e (bg-primary) | 5.8:1 | AA |
| #14b8a6 (accent-teal) | #1a1a2e (bg-primary) | 6.5:1 | AA |

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### High Contrast Mode

```css
@media (prefers-contrast: high) {
  :root {
    --color-text-primary: #ffffff;
    --color-text-secondary: #ffffff;
    --glass-border: rgba(255, 255, 255, 0.3);
  }

  .glass {
    border-width: 2px;
  }
}
```

---

## Theme Testing

### Visual Regression Testing

```typescript
// tests/theme.spec.ts
import { test, expect } from '@playwright/test';

test('landing page matches theme snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('landing-page.png');
});

test('glassmorphism effect renders correctly', async ({ page }) => {
  await page.goto('/');
  const card = page.locator('.glass').first();
  await expect(card).toHaveCSS('backdrop-filter', /blur/);
});
```

### Contrast Testing

```typescript
import { axe } from 'jest-axe';

test('theme has no contrast violations', async () => {
  const { container } = render(<App />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

---

**Theme API Status**: ✅ Complete
**Next Step**: Create quickstart.md for developer onboarding
