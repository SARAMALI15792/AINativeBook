// Auth client configuration
export const authClient = {
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3001',
  cookieOptions: {
    domain:
      process.env.NODE_ENV === 'production' ? '.intellistack.com' : 'localhost',
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax' as const,
  },
};

// Helper functions for authentication

export async function signUp(email: string, password: string, name: string) {
  try {
    const response = await fetch(`${authClient.baseURL}/api/auth/sign-up/email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name }),
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || 'Signup failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
}

export async function signIn(email: string, password: string, rememberMe = false) {
  try {
    const response = await fetch(`${authClient.baseURL}/api/auth/sign-in/email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, rememberMe }),
      credentials: 'include',
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || 'Login failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

export async function signOut() {
  try {
    const response = await fetch(`${authClient.baseURL}/api/auth/sign-out`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Logout failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
}

export async function socialSignIn(provider: 'google' | 'github', callbackURL?: string) {
  try {
    // Redirect to OAuth provider
    const redirectUrl = `${authClient.baseURL}/api/auth/oauth/${provider}?callbackURL=${encodeURIComponent(callbackURL || '/dashboard')}`;
    window.location.href = redirectUrl;
  } catch (error) {
    console.error('Social auth error:', error);
    throw error;
  }
}

export async function getSession() {
  try {
    const response = await fetch(`${authClient.baseURL}/api/auth/get-session`, {
      credentials: 'include',
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data?.user || null;
  } catch (error) {
    console.error('Get session error:', error);
    return null;
  }
}

export async function getJwtToken(): Promise<string | null> {
  try {
    const response = await fetch(`${authClient.baseURL}/api/auth/token`, {
      credentials: 'include',
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data?.token || null;
  } catch (error) {
    console.error('Get JWT token error:', error);
    return null;
  }
}

// Export a client object for compatibility
export function getAuthClient() {
  return {
    getJwtToken,
    getSession,
    signIn,
    signOut,
    signUp,
  };
}
