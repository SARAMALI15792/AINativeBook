/**
 * Better-Auth React Client for Docusaurus
 * Connects to Better-Auth OIDC server for authentication
 */

import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

/**
 * Get Better-Auth URL from Docusaurus customFields
 * Falls back to localhost for development
 *
 * NOTE: Docusaurus client-side does NOT have process.env.
 * We read from window.__DOCUSAURUS__ customFields or use a literal fallback.
 */
const getBetterAuthUrl = (): string => {
  if (typeof window !== 'undefined') {
    const docusaurus = (window as any).__DOCUSAURUS__;
    const url = docusaurus?.siteConfig?.customFields?.betterAuthUrl;
    if (url) return url as string;
  }
  return 'http://localhost:3001';
};

/**
 * Get Backend API URL from Docusaurus customFields
 */
export const getBackendUrl = (): string => {
  if (typeof window !== 'undefined') {
    const docusaurus = (window as any).__DOCUSAURUS__;
    const url = docusaurus?.siteConfig?.customFields?.backendUrl;
    if (url) return url as string;
  }
  return 'http://localhost:8000';
};

/**
 * Better-Auth client instance (lazy singleton)
 *
 * We use a getter so the client is only created when first accessed,
 * avoiding "Cannot access before initialization" during module evaluation.
 */
let _authClient: ReturnType<typeof createAuthClient> | null = null;

export function getAuthClient() {
  if (!_authClient) {
    _authClient = createAuthClient({
      baseURL: getBetterAuthUrl(),
      basePath: '/api/auth',
      plugins: [
        jwtClient(),
      ],
      fetchOptions: {
        credentials: 'include' as RequestCredentials,
        // Wrap fetch so network errors (auth server down) don't throw uncaught exceptions
        customFetchImpl: async (url: RequestInfo | URL, init?: RequestInit) => {
          try {
            // Ensure credentials are always included for cross-port cookie sharing
            return await fetch(url, { ...init, credentials: 'include' });
          } catch {
            // Auth server unreachable — return a synthetic 503 response
            return new Response(JSON.stringify({ error: 'Auth server unreachable' }), {
              status: 503,
              statusText: 'Service Unavailable',
              headers: { 'Content-Type': 'application/json' },
            });
          }
        },
      },
    });
  }
  return _authClient;
}

/**
 * Convenience export — a proxy object that lazily delegates to the real client.
 * Safe to import at module scope; the real client is created on first use.
 */
export const authClient = new Proxy({} as ReturnType<typeof createAuthClient>, {
  get(_target, prop) {
    return (getAuthClient() as any)[prop];
  },
});

// Export commonly used methods (these are functions, so they resolve lazily through the proxy)
export const signIn = (...args: any[]) => (getAuthClient() as any).signIn(...args);
export const signUp = (...args: any[]) => (getAuthClient() as any).signUp(...args);
export const signOut = (...args: any[]) => (getAuthClient() as any).signOut(...args);
export const useSession = (...args: any[]) => (getAuthClient() as any).useSession(...args);
export const getSession = (...args: any[]) => (getAuthClient() as any).getSession(...args);

/**
 * Get a JWT token for authenticating with the backend API.
 *
 * Better-Auth session tokens are NOT JWTs — they are opaque session IDs.
 * The backend validates JWTs signed by the auth server (EdDSA/Ed25519).
 * This function calls the /api/auth/token endpoint to exchange the
 * session cookie for a proper JWT.
 *
 * @returns JWT string or null if not authenticated
 */
export async function getJwtToken(): Promise<string | null> {
  try {
    const client = getAuthClient() as any;
    const { data, error } = await client.token();
    if (error || !data?.token) {
      console.warn('Failed to get JWT token:', error);
      return null;
    }
    return data.token;
  } catch (err) {
    console.warn('getJwtToken error:', err);
    return null;
  }
}

/**
 * Type definitions for user session
 */
export interface UserSession {
  user: {
    id: string;
    email: string;
    name: string | null;
    emailVerified: boolean;
    role: 'student' | 'instructor' | 'admin';
    image?: string | null;
  };
  session: {
    id: string;
    expiresAt: string;
    token: string;
  };
}

/**
 * Type for onboarding preferences
 */
export interface OnboardingPreferences {
  theme: 'light' | 'dark' | 'system';
  os: 'windows' | 'macos' | 'linux' | 'other';
  deviceType: 'desktop' | 'laptop' | 'tablet';
  preferredIde: 'vscode' | 'pycharm' | 'clion' | 'nvim' | 'other';
  shellType: 'bash' | 'zsh' | 'powershell' | 'cmd' | 'fish';
  notifications: {
    email: boolean;
    browser: boolean;
  };
}

export interface LearningPreferences {
  learningStyle: 'visual' | 'reading' | 'hands-on' | 'mixed';
  pacePreference: 'self-paced' | 'structured' | 'intensive';
  goalTimeframe: '3-months' | '6-months' | '1-year' | 'flexible';
  focusAreas: string[];
}

export interface BackgroundLevel {
  programmingExperience: 'none' | 'beginner' | 'intermediate' | 'advanced';
  roboticsExperience: 'none' | 'hobbyist' | 'academic' | 'professional';
  mathBackground: 'basic' | 'calculus' | 'linear-algebra' | 'advanced';
  linuxFamiliarity: 'none' | 'basic' | 'comfortable' | 'expert';
}

/**
 * Check if user has completed onboarding
 */
export const hasCompletedOnboarding = (user: UserSession['user'] | null): boolean => {
  if (!user) return false;
  // Check for onboarding completion flag in user metadata
  // This would be set after completing the onboarding wizard
  return (user as any).onboardingCompleted === true;
};
