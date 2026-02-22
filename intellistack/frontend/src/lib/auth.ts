// Auth client configuration
export const authClient = {
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || '',
  cookieOptions: {
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
      const errorData = await response.json().catch(() => ({}));
      console.error('Login failed:', {
        status: response.status,
        statusText: response.statusText,
        error: errorData,
        url: response.url,
      });
      throw new Error(errorData.message || 'Login failed');
    }

    const data = await response.json();
    console.log('Login successful:', { userId: data.user?.id });
    return data;
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
    // Use absolute Netlify URL for OAuth callback
    const frontendUrl = typeof window !== 'undefined'
      ? window.location.origin
      : 'https://intellistack-frontend.netlify.app';

    const absoluteCallback = callbackURL
      ? `${frontendUrl}${callbackURL.startsWith('/') ? callbackURL : '/' + callbackURL}`
      : `${frontendUrl}/dashboard`;

    // Use Better-Auth's correct OAuth endpoint
    const response = await fetch(`${authClient.baseURL}/api/auth/sign-in/social`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        provider,
        callbackURL: absoluteCallback,
      }),
    });

    if (!response.ok) {
      throw new Error('OAuth initialization failed');
    }

    const data = await response.json();

    // Redirect to OAuth provider
    if (data.url) {
      window.location.href = data.url;
    } else {
      throw new Error('No OAuth URL returned');
    }
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
