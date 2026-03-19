'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getAuthClient } from '@/lib/auth';
import type { PersonalizationPreferences } from '@/types/api';

interface User {
  id: string;
  email: string;
  name?: string;
  avatar?: string;
  image?: string;
  role?: string;
  current_stage?: number;
  onboarding_completed?: boolean;
  emailVerified?: boolean;
}

interface Session {
  isAuthenticated: boolean;
  user?: User | null;
  hasCompletedPersonalization?: boolean;
}

interface AuthContextType {
  user: User | null;
  session: Session;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  updatePreferences: (preferences: PersonalizationPreferences) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in
  useEffect(() => {
    const checkSession = async () => {
      try {
        const client = getAuthClient();
        const result = await (client as any).getSession();

        if (result.data?.user) {
          setUser(result.data.user);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const client = getAuthClient();
      const result = await (client as any).signIn.email({
        email,
        password,
      });

      if (result.error) {
        throw new Error(result.error.message || 'Login failed');
      }

      if (result.data?.user) {
        setUser(result.data.user);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      const client = getAuthClient();
      await (client as any).signOut();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (email: string, password: string, name: string) => {
    setIsLoading(true);
    try {
      const client = getAuthClient();
      const result = await (client as any).signUp.email({
        email,
        password,
        name,
      });

      if (result.error) {
        throw new Error(result.error.message || 'Registration failed');
      }

      if (result.data?.user) {
        setUser(result.data.user);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const updatePreferences = async (preferences: PersonalizationPreferences) => {
    const authUrl = process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3001';
    const response = await fetch(`${authUrl}/api/auth/onboarding/preferences`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ preferences }),
    });
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.message || `Failed to save preferences (${response.status})`);
    }
  };

  const isAuthenticated = !!user;
  const session: Session = {
    isAuthenticated,
    user,
    hasCompletedPersonalization: user?.onboarding_completed ?? false,
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        session,
        isLoading,
        isAuthenticated,
        login,
        logout,
        register,
        updatePreferences,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
