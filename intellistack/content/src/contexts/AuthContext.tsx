import React, { createContext, useContext, useState, useEffect } from 'react';
import { authClient, User as AuthUser } from '../lib/auth';

interface User {
  id: string;
  email: string;
  name: string;
  email_verified: boolean;
  onboarding_completed: boolean;
  current_stage: number;
  role: string;
  avatar_url?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  logout: () => Promise<void>;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const loadSession = async () => {
    try {
      const result = await authClient.getSession();
      if (result?.data) {
        setUser(result.data as User);
      } else {
        setUser(null);
      }
    } catch (error) {
      console.error('Failed to load session:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Only run in browser
    if (typeof window === 'undefined') {
      setLoading(false);
      return;
    }

    loadSession();

    // Listen for auth state changes (fired by login/register pages)
    const handleAuthChange = () => loadSession();
    window.addEventListener('auth-state-changed', handleAuthChange);
    return () => window.removeEventListener('auth-state-changed', handleAuthChange);
  }, []);

  const logout = async () => {
    try {
      await authClient.signOut();
      setUser(null);
      // Dispatch event for other components
      window.dispatchEvent(new Event('auth-state-changed'));
      // Redirect to login (use full base URL for correct routing)
      const baseUrl = (window as any).docusaurus?.siteConfig?.baseUrl || '/AINativeBook/';
      window.location.href = `${baseUrl}auth/login`;
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const refreshSession = async () => {
    await loadSession();
  };

  return (
    <AuthContext.Provider value={{ user, loading, logout, refreshSession }}>
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
