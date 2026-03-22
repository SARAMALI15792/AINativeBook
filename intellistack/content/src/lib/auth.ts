/**
 * Better Auth Client for Docusaurus
 * Lazy singleton pattern with Proxy for SSR compatibility
 */

// Get auth server URL from Docusaurus config or environment
const getAuthServerUrl = (): string => {
  if (typeof window !== 'undefined' && (window as any).__ENV__?.BETTER_AUTH_URL) {
    return (window as any).__ENV__.BETTER_AUTH_URL;
  }
  return 'http://localhost:3001';
};

// Auth client with fetch-based implementation
export const authClient = {
  get baseURL() {
    return getAuthServerUrl();
  },

  // Get current session
  async getSession() {
    if (typeof window === 'undefined') {
      throw new Error('getSession can only be called in browser');
    }

    try {
      const response = await fetch(`${this.baseURL}/api/auth/get-session`, {
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        return { data: null, error: null };
      }

      const data = await response.json();
      return { data: data?.user || null, error: null };
    } catch (error) {
      console.error('Get session error:', error);
      return { data: null, error };
    }
  },

  // Sign in with email/password
  async signIn(email: string, password: string, rememberMe = false) {
    if (typeof window === 'undefined') {
      throw new Error('signIn can only be called in browser');
    }

    try {
      const response = await fetch(`${this.baseURL}/api/auth/sign-in/email`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, rememberMe }),
      });

      const data = await response.json();

      if (!response.ok) {
        return { data: null, error: data };
      }

      return { data: data.user, error: null };
    } catch (error) {
      console.error('Sign in error:', error);
      return { data: null, error };
    }
  },

  // Sign up with email/password
  async signUp(email: string, password: string, name: string) {
    if (typeof window === 'undefined') {
      throw new Error('signUp can only be called in browser');
    }

    try {
      const response = await fetch(`${this.baseURL}/api/auth/sign-up/email`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      const data = await response.json();

      if (!response.ok) {
        return { data: null, error: data };
      }

      return { data: data.user, error: null };
    } catch (error) {
      console.error('Sign up error:', error);
      return { data: null, error };
    }
  },

  // Sign out
  async signOut() {
    if (typeof window === 'undefined') {
      throw new Error('signOut can only be called in browser');
    }

    try {
      const response = await fetch(`${this.baseURL}/api/auth/sign-out`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Sign out failed');
      }

      return { success: true, error: null };
    } catch (error) {
      console.error('Sign out error:', error);
      return { success: false, error };
    }
  },

  // OAuth sign in — direct browser navigation to auth server (first-party).
  // Using fetch() here causes cross-origin state cookies which Chrome blocks.
  // A full-page redirect makes the auth server first-party so state cookies work.
  signInWithOAuth(provider: 'google' | 'github', callbackURL?: string) {
    if (typeof window === 'undefined') {
      throw new Error('signInWithOAuth can only be called in browser');
    }
    const baseUrl = '/AINativeBook/';
    const callback = callbackURL || `${window.location.origin}${baseUrl}auth/callback`;
    const authServerUrl = getAuthServerUrl();
    window.location.href = `${authServerUrl}/api/auth/sign-in/social?provider=${provider}&callbackURL=${encodeURIComponent(callback)}`;
    return { data: null, error: null };
  },
};

// Export convenience functions
export const getSession = () => authClient.getSession();
export const signIn = (email: string, password: string, rememberMe?: boolean) =>
  authClient.signIn(email, password, rememberMe);
export const signUp = (email: string, password: string, name: string) =>
  authClient.signUp(email, password, name);
export const signOut = () => authClient.signOut();
export const signInWithGoogle = (callbackURL?: string) =>
  authClient.signInWithOAuth('google', callbackURL);
export const signInWithGitHub = (callbackURL?: string) =>
  authClient.signInWithOAuth('github', callbackURL);

// Export types
export type User = {
  id: string;
  email: string;
  name: string;
  email_verified: boolean;
  onboarding_completed: boolean;
  current_stage: number;
  role: string;
  avatar_url?: string;
};

export type Session = {
  user: User;
  expires_at: string;
};
