'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getSession, signIn, signOut, signUp } from '@/lib/auth';
import { apiClient } from '@/lib/api-client';
import { ThemeMode } from '@/types/api';
import type { UserSession, User, PersonalizationPreferences } from '@/types/api';

interface AuthContextValue {
  session: UserSession;
  login: (email: string, password: string, rememberMe?: boolean) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  updatePreferences: (preferences: Partial<PersonalizationPreferences>) => Promise<void>;
  refreshSession: () => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const DEFAULT_THEME = {
  mode: ThemeMode.DARK,
  reducedMotion: false,
  highContrast: false,
};

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<UserSession>({
    user: null,
    isAuthenticated: false,
    preferences: null,
    hasCompletedPersonalization: false,
    theme: DEFAULT_THEME,
  });
  const [isLoading, setIsLoading] = useState(true);

  const refreshSession = async () => {
    try {
      const user = await getSession();
      if (user) {
        // Try to get preferences, but don't fail the session if it errors
        let prefs: PersonalizationPreferences | null = null;
        try {
          const prefsResponse = await apiClient.getPreferences();
          prefs = prefsResponse.data;
        } catch {
          // Preferences endpoint may not be available yet - that's ok
          console.warn('Could not fetch preferences, continuing without them');
        }
        setSession({
          user,
          isAuthenticated: true,
          preferences: prefs,
          hasCompletedPersonalization: !!prefs,
          theme: DEFAULT_THEME,
        });
      } else {
        setSession({
          user: null,
          isAuthenticated: false,
          preferences: null,
          hasCompletedPersonalization: false,
          theme: DEFAULT_THEME,
        });
      }
    } catch (error) {
      console.error('Failed to refresh session:', error);
      setSession({
        user: null,
        isAuthenticated: false,
        preferences: null,
        hasCompletedPersonalization: false,
        theme: DEFAULT_THEME,
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    refreshSession();
  }, []);

  const login = async (email: string, password: string, rememberMe = false) => {
    const response = await signIn(email, password, rememberMe);
    await refreshSession();
  };

  const logout = async () => {
    await signOut();
    setSession({
      user: null,
      isAuthenticated: false,
      preferences: null,
      hasCompletedPersonalization: false,
      theme: DEFAULT_THEME,
    });
  };

  const register = async (email: string, password: string, name: string) => {
    const response = await signUp(email, password, name);
    await refreshSession();
  };

  const updatePreferences = async (preferences: Partial<PersonalizationPreferences>) => {
    await apiClient.updatePreferences(preferences as any);
    await refreshSession();
  };

  return (
    <AuthContext.Provider
      value={{
        session,
        login,
        logout,
        register,
        updatePreferences,
        refreshSession,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
