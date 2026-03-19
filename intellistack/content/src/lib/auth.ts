/**
 * Better Auth Client for Docusaurus
 * Lazy singleton pattern with Proxy for SSR compatibility
 */

// Get auth server URL from Docusaurus config or environment
const getAuthServerUrl = (): string => {
  if (typeof window !== 'undefined') {
    // Try to get from Docusaurus customFields first
    if (window.docusaurus?.siteConfig?.customFields?.betterAuthUrl) {
      return window.docusaurus.siteConfig.customFields.betterAuthUrl as string;
    }
    // Fallback to default - Docusaurus customFields should be configured in docusaurus.config.ts
    return 'http://localhost:3001';
  }
  // During SSR/SSG, return placeholder
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

  // OAuth sign in
  async signInWithOAuth(provider: 'google' | 'github', callbackURL?: string) {
    if (typeof window === 'undefined') {
      throw new Error('signInWithOAuth can only be called in browser');
    }

    try {
      const callback = callbackURL || `${window.location.origin}/auth/callback`;
      const response = await fetch(`${this.baseURL}/api/auth/oauth/${provider}`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ callbackURL: callback }),
      });

      const data = await response.json();

      if (!response.ok) {
        return { data: null, error: data };
      }

      // Redirect to OAuth provider
      if (data.url) {
        window.location.href = data.url;
      }

      return { data, error: null };
    } catch (error) {
      console.error('OAuth sign in error:', error);
      return { data: null, error };
    }
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
