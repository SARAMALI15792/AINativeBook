import React, { createContext, useContext, useState, useEffect } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
  role?: string;
  emailVerified?: boolean;
  image?: string | null;
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
      // Use the Better-Auth client (same one used by login/register/navbar)
      const mod = await import('../lib/auth-client');
      const client = mod.getAuthClient();
      const result = await client.getSession();
      if (result?.data?.user) {
        const u = result.data.user;
        setUser({
          id: u.id,
          email: u.email || '',
          name: u.name || '',
          role: u.role || 'student',
          emailVerified: u.emailVerified || false,
          image: u.image || null,
        });
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
    loadSession();

    // Listen for auth state changes (fired by login/register pages)
    const handleAuthChange = () => loadSession();
    window.addEventListener('auth-state-changed', handleAuthChange);
    return () => window.removeEventListener('auth-state-changed', handleAuthChange);
  }, []);

  const logout = async () => {
    try {
      const mod = await import('../lib/auth-client');
      const client = mod.getAuthClient();
      await client.signOut();
      setUser(null);
      window.location.href = '/login';
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
