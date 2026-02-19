'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { ThemeMode } from '@/types/api';
import type { ThemeConfig } from '@/types/api';

interface ThemeContextValue {
  theme: ThemeConfig;
  setTheme: (theme: Partial<ThemeConfig>) => void;
  toggleMode: () => void;
  applyTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

const DEFAULT_THEME: ThemeConfig = {
  mode: ThemeMode.DARK,
  reducedMotion: false,
  highContrast: false,
};

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<ThemeConfig>(() => {
    if (typeof window === 'undefined') return DEFAULT_THEME;

    // Load from localStorage
    const saved = localStorage.getItem('theme-config');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return DEFAULT_THEME;
      }
    }

    // Detect system preferences
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    return {
      ...DEFAULT_THEME,
      mode: prefersDark ? ThemeMode.DARK : ThemeMode.LIGHT,
      reducedMotion: prefersReducedMotion,
    };
  });

  const applyTheme = () => {
    if (typeof window === 'undefined') return;

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
    } else {
      root.style.setProperty('--duration-fast', '150ms');
      root.style.setProperty('--duration-normal', '300ms');
      root.style.setProperty('--duration-slow', '500ms');
    }

    // Apply high contrast (future feature)
    if (theme.highContrast) {
      // Increase contrast ratios
      root.style.setProperty('--color-text-primary', '#ffffff');
      root.style.setProperty('--color-text-secondary', '#ffffff');
      root.style.setProperty('--glass-border', 'rgba(255, 255, 255, 0.3)');
    }
  };

  const setTheme = (updates: Partial<ThemeConfig>) => {
    const newTheme = { ...theme, ...updates };
    setThemeState(newTheme);
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme-config', JSON.stringify(newTheme));
    }
  };

  const toggleMode = () => {
    setTheme({ mode: theme.mode === ThemeMode.DARK ? ThemeMode.LIGHT : ThemeMode.DARK });
  };

  useEffect(() => {
    applyTheme();
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleMode, applyTheme }}>
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
