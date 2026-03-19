'use client';

import { createAuthClient } from 'better-auth/react';
import { jwtClient } from 'better-auth/client/plugins';

const AUTH_URL = typeof window !== 'undefined'
  ? process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3001'
  : 'http://localhost:3001';

/**
 * Lazy-loaded Better-Auth client instance
 * Created on first use to avoid initialization issues
 */
let _authClient: ReturnType<typeof createAuthClient> | null = null;

function getAuthClientInstance() {
  if (!_authClient) {
    _authClient = createAuthClient({
      baseURL: AUTH_URL,
      basePath: '/api/auth',
      plugins: [jwtClient()],
      fetchOptions: {
        credentials: 'include' as RequestCredentials,
      },
    });
  }
  return _authClient;
}

/**
 * Get the Better-Auth client instance
 * Returns the client with methods for signIn, signUp, signOut, getSession
 */
export function getAuthClient() {
  return getAuthClientInstance();
}

/**
 * Trigger OAuth social sign-in flow
 * Uses Better-Auth's built-in OAuth handler
 */
export async function socialSignIn(provider: 'google' | 'github') {
  const client = getAuthClientInstance();
  // Better-Auth has a signIn method that handles OAuth
  return (client as any).signIn.social({
    provider,
    callbackURL: '/',
  });
}

/**
 * Get the current user session
 * Wrapper around Better-Auth's getSession method
 */
export async function getSession() {
  try {
    const client = getAuthClientInstance();
    const result = await (client as any).getSession();
    return result.data;
  } catch (error) {
    console.error('Error fetching session:', error);
    return null;
  }
}

/**
 * Get the JWT token for backend API authentication
 * Exchanges session cookie for JWT via Better-Auth's token endpoint
 */
export async function getJwtToken(): Promise<string | null> {
  try {
    const client = getAuthClientInstance();
    const result = await (client as any).token();

    if (result.error || !result.data?.token) {
      console.warn('Failed to get JWT token:', result.error);
      return null;
    }

    return result.data.token;
  } catch (error) {
    console.error('Error fetching JWT token:', error);
    return null;
  }
}

/**
 * Set the JWT token in storage (for backwards compatibility)
 */
export function setJwtToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
}

/**
 * Clear the JWT token from storage
 */
export function clearJwtToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
}
