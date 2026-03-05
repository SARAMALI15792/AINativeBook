# Better Auth Integration in Docusaurus: Technical Documentation

**Date:** 2026-02-26
**Project:** IntelliStack Platform
**Purpose:** Technical decisions and implementation patterns for Better Auth authentication in Docusaurus v3.x

---

## Table of Contents

1. [Better Auth Client Integration in Docusaurus](#1-better-auth-client-integration-in-docusaurus)
2. [Docusaurus Custom Pages for Auth](#2-docusaurus-custom-pages-for-auth)
3. [Docusaurus Custom Navbar Components](#3-docusaurus-custom-navbar-components)
4. [Protected Routes in Docusaurus](#4-protected-routes-in-docusaurus)
5. [Cross-Origin Session Management](#5-cross-origin-session-management)
6. [Production Deployment Considerations](#6-production-deployment-considerations)

---

## 1. Better Auth Client Integration in Docusaurus

### 1.1 Overview

Better Auth is a framework-agnostic authentication library for TypeScript. Integrating it with Docusaurus requires careful handling of SSR/SSG constraints and client-side initialization.

### 1.2 Client Module Initialization

**Pattern: Lazy Singleton with Proxy**

```typescript
// src/lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

/**
 * Get Better-Auth URL from Docusaurus customFields
 * Docusaurus client-side does NOT have process.env access
 */
const getBetterAuthUrl = (): string => {
  if (typeof window !== 'undefined') {
    const docusaurus = (window as any).__DOCUSAURUS__;
    const url = docusaurus?.siteConfig?.customFields?.betterAuthUrl;
    if (url) return url as string;
  }
  return 'http://localhost:3001'; // Development fallback
};

/**
 * Lazy singleton pattern - client created on first access
 */
let _authClient: ReturnType<typeof createAuthClient> | null = null;

export function getAuthClient() {
  if (!_authClient) {
    _authClient = createAuthClient({
      baseURL: getBetterAuthUrl(),
      basePath: '/api/auth',
      plugins: [jwtClient()],
      fetchOptions: {
        credentials: 'include', // Critical for cross-origin cookies
        customFetchImpl: async (url: RequestInfo | URL, init?: RequestInit) => {
          try {
            return await fetch(url, { ...init, credentials: 'include' });
          } catch {
            // Auth server unreachable - return synthetic 503
            return new Response(
              JSON.stringify({ error: 'Auth server unreachable' }),
              {
                status: 503,
                headers: { 'Content-Type': 'application/json' },
              }
            );
          }
        },
      },
    });
  }
  return _authClient;
}

/**
 * Proxy for safe module-scope imports
 * Prevents "Cannot access before initialization" errors
 */
export const authClient = new Proxy({} as ReturnType<typeof createAuthClient>, {
  get(_target, prop) {
    return (getAuthClient() as any)[prop];
  },
});

// Export convenience methods
export const signIn = (...args: any[]) => getAuthClient().signIn(...args);
export const signUp = (...args: any[]) => getAuthClient().signUp(...args);
export const signOut = (...args: any[]) => getAuthClient().signOut(...args);
export const useSession = (...args: any[]) => getAuthClient().useSession(...args);
```

**Key Decisions:**

1. **Lazy Initialization**: Client created on first access, not at module load time
2. **Proxy Pattern**: Allows safe module-scope imports without initialization errors
3. **Custom Fetch**: Graceful degradation when auth server is unreachable
4. **Credentials Include**: Essential for cross-origin cookie sharing

### 1.3 Webpack Configuration

**Pattern: Custom Plugin with Resolve Aliases**

```typescript
// docusaurus.config.ts
import path from 'path';

const config: Config = {
  plugins: [
    function (context, options) {
      return {
        name: 'custom-webpack-config',
        configureWebpack(config, isServer, utils) {
          return {
            resolve: {
              alias: {
                '@site': path.resolve(__dirname),
              },
              extensions: ['.ts', '.tsx', '.js', '.jsx', '.json'],
              modules: [
                path.resolve(__dirname, 'src'),
                'node_modules'
              ],
            },
          };
        },
      };
    },
  ],
};
```

**Why This Matters:**
- Ensures TypeScript files are resolved correctly
- Provides clean import paths (`@site/...`)
- No additional loaders needed for Better Auth (it's pure TypeScript)

### 1.4 Client Module Registration

**Pattern: ExecutionEnvironment Guard**

```typescript
// src/clientModules/authInit.ts
import ExecutionEnvironment from '@docusaurus/ExecutionEnvironment';

// Only run on client side
if (ExecutionEnvironment.canUseDOM) {
  import('../lib/auth-client')
    .then(async ({ getAuthClient }) => {
      try {
        const client = getAuthClient();
        await client.getSession(); // Warm up session cache
      } catch {
        // Silent fail - auth server unreachable
      }
    })
    .catch(() => {
      // Module load failed - silent
    });
}

/**
 * Called on route change - can refresh auth state
 */
export function onRouteDidUpdate({ location, previousLocation }) {
  if (location.pathname !== previousLocation?.pathname) {
    // Optional: refresh session on route change
  }
}
```

**Register in docusaurus.config.ts:**

```typescript
const config: Config = {
  clientModules: [
    './src/clientModules/authInit.ts',
  ],
  customFields: {
    betterAuthUrl: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
  },
};
```

**Key Decisions:**

1. **ExecutionEnvironment.canUseDOM**: Prevents SSR execution
2. **Dynamic Import**: Ensures client-only code doesn't break SSR
3. **Silent Failures**: Auth unavailability doesn't crash the site
4. **Session Warming**: Pre-loads session on initial page load

---

## 2. Docusaurus Custom Pages for Auth

### 2.1 Page Structure

Docusaurus automatically routes files in `src/pages/` directory:

```
src/pages/
├── login.tsx           → /login
├── register.tsx        → /register
├── forgot-password.tsx → /forgot-password
├── reset-password.tsx  → /reset-password
├── profile.tsx         → /profile
└── settings.tsx        → /settings
```

### 2.2 Auth Page Pattern

**Pattern: Layout Wrapper + Dynamic Import**

```typescript
// src/pages/login.tsx
import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useHistory, useLocation } from '@docusaurus/router';

export default function LoginPage(): JSX.Element {
  const history = useHistory();
  const location = useLocation();
  const [authClient, setAuthClient] = useState<any>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Dynamic import of auth client (client-side only)
  useEffect(() => {
    import('../lib/auth-client').then((mod) => {
      setAuthClient(mod.authClient);

      // Check if already logged in
      mod.authClient.getSession().then((result) => {
        if (result.data?.user) {
          history.push('/stage-1/intro'); // Redirect if authenticated
        }
      });
    });
  }, []);

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!authClient) return;

    setError(null);
    setIsLoading(true);

    try {
      const result = await authClient.signIn.email({
        email,
        password,
      });

      if (result.error) {
        setError(result.error.message || 'Invalid email or password');
        return;
      }

      // Dispatch auth state change event
      window.dispatchEvent(new Event('auth-state-changed'));

      // Redirect to return URL or default
      const params = new URLSearchParams(location.search);
      const returnUrl = params.get('returnUrl') || '/stage-1/intro';
      history.push(returnUrl);
    } catch (err: any) {
      setError(err.message || 'An error occurred during login');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to IntelliStack">
      <div className="auth-container">
        <form onSubmit={handleEmailLogin}>
          {/* Form fields */}
        </form>
      </div>
    </Layout>
  );
}
```

**Key Decisions:**

1. **Layout Wrapper**: Uses `@theme/Layout` for consistent navbar/footer
2. **Dynamic Import**: Auth client loaded client-side only
3. **useHistory/useLocation**: Docusaurus router hooks for navigation
4. **Return URL Support**: Preserves intended destination after login
5. **Auth State Events**: Custom events for cross-component communication

### 2.3 OAuth Flow Handling

```typescript
const handleOAuthLogin = async (provider: 'google' | 'github') => {
  if (!authClient) return;

  try {
    await authClient.signIn.social({
      provider,
      callbackURL: window.location.origin + '/stage-1/intro',
    });

    // OAuth redirects to provider, then back to callbackURL
    // Better Auth handles the callback automatically
  } catch (err: any) {
    setError(err.message || `Failed to sign in with ${provider}`);
  }
};
```

**OAuth Callback Flow:**
1. User clicks "Sign in with Google"
2. Better Auth redirects to Google OAuth
3. Google redirects back to `{BETTER_AUTH_URL}/api/auth/callback/google`
4. Better Auth sets session cookie and redirects to `callbackURL`
5. User lands on Docusaurus with active session

---

## 3. Docusaurus Custom Navbar Components

### 3.1 Component Registration

**Pattern: Swizzle ComponentTypes**

```typescript
// src/theme/NavbarItem/ComponentTypes.tsx
import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import AuthNavbarItem from './AuthNavbarItem';

export default {
  ...ComponentTypes,
  'custom-authNavbarItem': AuthNavbarItem,
};
```

**Register in docusaurus.config.ts:**

```typescript
const config: Config = {
  themeConfig: {
    navbar: {
      items: [
        {
          type: 'custom-authNavbarItem',
          position: 'right',
        },
      ],
    },
  },
};
```

### 3.2 Auth-Aware Navbar Component

**Pattern: BrowserOnly + Context Hook**

```typescript
// src/theme/NavbarItem/AuthNavbarItem.tsx
import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useAuth } from '../../contexts/AuthContext';

function AuthNavbarItemContent(): JSX.Element {
  const { user, loading, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  if (loading) {
    return <span className="loading-dot">...</span>;
  }

  if (user) {
    return (
      <div className="user-dropdown">
        <button className="user-button">
          {user.image ? (
            <img src={user.image} alt={user.name} />
          ) : (
            <span>{user.name[0]}</span>
          )}
          <span>{user.name}</span>
        </button>

        {isDropdownOpen && (
          <div className="dropdown-menu">
            <Link to="/profile">Profile</Link>
            <Link to="/settings">Settings</Link>
            <button onClick={logout}>Sign Out</button>
          </div>
        )}
      </div>
    );
  }

  return <Link to="/login">Sign In</Link>;
}

export default function AuthNavbarItem(): JSX.Element {
  return (
    <BrowserOnly fallback={<span>...</span>}>
      {() => <AuthNavbarItemContent />}
    </BrowserOnly>
  );
}
```

**Key Decisions:**

1. **BrowserOnly Wrapper**: Prevents SSR hydration mismatches
2. **Context Hook**: Centralized auth state management
3. **Fallback UI**: Shows loading state during SSR
4. **Dropdown Pattern**: Standard user menu with profile/settings/logout

### 3.3 Auth Context Provider

**Pattern: Root Wrapper with Event Listeners**

```typescript
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';

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
      const mod = await import('../lib/auth-client');
      const client = mod.getAuthClient();
      const result = await client.getSession();

      if (result?.data?.user) {
        setUser(result.data.user);
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

    // Listen for auth state changes
    const handleAuthChange = () => loadSession();
    window.addEventListener('auth-state-changed', handleAuthChange);
    return () => window.removeEventListener('auth-state-changed', handleAuthChange);
  }, []);

  const logout = async () => {
    const mod = await import('../lib/auth-client');
    await mod.getAuthClient().signOut();
    setUser(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, loading, logout, refreshSession: loadSession }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
```

**Register in Root:**

```typescript
// src/theme/Root.tsx
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
```

**Key Decisions:**

1. **Custom Events**: `auth-state-changed` for cross-component sync
2. **Dynamic Import**: Auth client loaded only when needed
3. **Root Provider**: Wraps entire app for global auth state
4. **Error Handling**: Graceful degradation on auth failures

---

## 4. Protected Routes in Docusaurus

### 4.1 Protected Route Component

**Pattern: useEffect Redirect + Loading State**

```typescript
// src/components/ProtectedRoute.tsx
import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLocation, useNavigate } from '@docusaurus/router';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
}

export default function ProtectedRoute({
  children,
  requireAuth = true
}: ProtectedRouteProps) {
  const { user, loading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading && requireAuth && !user) {
      // Redirect to login with return URL
      const returnUrl = encodeURIComponent(location.pathname + location.search);
      navigate(`/login?returnUrl=${returnUrl}`);
    }
  }, [user, loading, requireAuth, navigate, location]);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '400px'
      }}>
        <div className="spinner" />
      </div>
    );
  }

  if (requireAuth && !user) {
    return null; // Will redirect in useEffect
  }

  return <>{children}</>;
}
```

**Usage in Pages:**

```typescript
// src/pages/profile.tsx
import React from 'react';
import Layout from '@theme/Layout';
import ProtectedRoute from '../components/ProtectedRoute';

export default function ProfilePage() {
  return (
    <Layout>
      <ProtectedRoute>
        <div>Protected profile content</div>
      </ProtectedRoute>
    </Layout>
  );
}
```

### 4.2 Doc Page Protection

**Pattern: Swizzle DocPage Layout**

```typescript
// src/theme/DocPage/Layout/index.tsx
import React from 'react';
import Layout from '@theme-original/DocPage/Layout';
import { useAuth } from '../../../contexts/AuthContext';
import { useLocation, useNavigate } from '@docusaurus/router';

export default function DocPageLayout(props) {
  const { user, loading } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  // Check if current doc requires authentication
  const requiresAuth = location.pathname.startsWith('/stage-');

  React.useEffect(() => {
    if (!loading && requiresAuth && !user) {
      const returnUrl = encodeURIComponent(location.pathname);
      navigate(`/login?returnUrl=${returnUrl}`);
    }
  }, [user, loading, requiresAuth, navigate, location]);

  if (loading && requiresAuth) {
    return <div className="loading-spinner" />;
  }

  if (requiresAuth && !user) {
    return null; // Redirecting
  }

  return <Layout {...props} />;
}
```

**Key Decisions:**

1. **useEffect Redirect**: Client-side navigation (no server-side redirects)
2. **Return URL Preservation**: Users land on intended page after login
3. **Loading States**: Prevents flash of protected content
4. **Null Return**: Clean UI during redirect
5. **Path-Based Protection**: Stage content requires authentication

### 4.3 SSR/SSG Considerations

**Important:** Docusaurus pre-renders pages at build time. Protected routes must:

1. **Never render protected content during SSR**
2. **Always check auth state client-side**
3. **Show loading state until auth is verified**
4. **Use `BrowserOnly` for auth-dependent UI**

```typescript
import BrowserOnly from '@docusaurus/BrowserOnly';

function ProtectedContent() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => {
        const { user } = useAuth();
        return user ? <SecretData /> : <Redirect to="/login" />;
      }}
    </BrowserOnly>
  );
}
```

---

## 5. Cross-Origin Session Management

### 5.1 Cookie Configuration

**Server-Side (Better Auth):**

```typescript
// auth-server/src/auth.ts
export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL,
  trustedOrigins: [
    'http://localhost:3005',  // Docusaurus dev
    'https://yourdomain.com', // Production
  ],

  advanced: {
    defaultCookieAttributes: {
      sameSite: process.env.NODE_ENV === 'production' ? 'none' : 'lax',
      secure: process.env.NODE_ENV === 'production',
      path: '/',
      domain: undefined, // Let browser set domain
    },
  },

  session: {
    cookieCache: {
      enabled: true,
      maxAge: 5 * 60, // 5 minutes
    },
  },
});
```

**Key Decisions:**

1. **SameSite=None (Production)**: Required for cross-origin cookies
2. **SameSite=Lax (Development)**: Works with localhost different ports
3. **Secure=true (Production)**: Required with SameSite=None
4. **trustedOrigins**: Whitelist for CORS
5. **cookieCache**: Reduces database lookups

### 5.2 Same-Domain Different-Path Deployment

**Scenario:** Auth server at `/` and Docusaurus at `/AINativeBook/`

```typescript
// docusaurus.config.ts
const config: Config = {
  url: 'https://yourdomain.com',
  baseUrl: '/AINativeBook/',

  customFields: {
    betterAuthUrl: 'https://yourdomain.com', // Root domain
  },
};
```

**Cookie Configuration:**

```typescript
// auth-server/src/auth.ts
export const auth = betterAuth({
  baseURL: 'https://yourdomain.com',

  advanced: {
    defaultCookieAttributes: {
      path: '/', // Cookie available to all paths
      domain: 'yourdomain.com', // Explicit domain
      sameSite: 'lax', // Same domain = Lax works
      secure: true,
    },
  },
});
```

**Key Decisions:**

1. **Path=/**: Cookie accessible from both `/` and `/AINativeBook/`
2. **Explicit Domain**: Ensures cookie sharing across paths
3. **SameSite=Lax**: Sufficient for same-domain different paths
4. **baseURL Points to Root**: Auth endpoints at domain root

### 5.3 Cross-Subdomain Deployment

**Scenario:** Auth at `auth.example.com`, Docusaurus at `docs.example.com`

```typescript
// auth-server/src/auth.ts
export const auth = betterAuth({
  baseURL: 'https://auth.example.com',

  advanced: {
    crossSubDomainCookies: {
      enabled: true,
      domain: '.example.com', // Leading dot for subdomains
    },
  },

  trustedOrigins: [
    'https://docs.example.com',
    'https://app.example.com',
  ],
});
```

**Key Decisions:**

1. **crossSubDomainCookies**: Better Auth feature for subdomain sharing
2. **Domain=.example.com**: Leading dot shares across subdomains
3. **SameSite=Lax**: Works with cross-subdomain (same site)
4. **trustedOrigins**: Whitelist all subdomains

### 5.4 Session Validation Pattern

**Client-Side:**

```typescript
// src/lib/auth-client.ts
export async function validateSession(): Promise<boolean> {
  try {
    const client = getAuthClient();
    const result = await client.getSession();
    return !!result?.data?.user;
  } catch {
    return false;
  }
}

// Usage in components
useEffect(() => {
  validateSession().then(isValid => {
    if (!isValid) {
      navigate('/login');
    }
  });
}, []);
```

**Session Refresh:**

```typescript
// Automatic refresh on route change
export function onRouteDidUpdate({ location }) {
  import('./lib/auth-client').then(async (mod) => {
    const client = mod.getAuthClient();
    await client.getSession(); // Refreshes session cache
  });
}
```

### 5.5 JWT Token for Backend API

**Pattern: Exchange Session for JWT**

```typescript
// src/lib/auth-client.ts
export async function getJwtToken(): Promise<string | null> {
  try {
    const client = getAuthClient();
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

// Usage in API calls
async function fetchProtectedData() {
  const token = await getJwtToken();

  const response = await fetch('https://api.example.com/data', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  return response.json();
}
```

**Key Decisions:**

1. **Session Cookie ≠ JWT**: Better Auth uses opaque session IDs
2. **JWT Plugin**: Generates JWTs signed with EdDSA (Ed25519)
3. **Token Endpoint**: `/api/auth/token` exchanges session for JWT
4. **Backend Validation**: FastAPI validates JWT signature via JWKS

---

## 6. Production Deployment Considerations

### 6.1 Environment Variables

**Docusaurus (build-time only):**

```bash
# .env
BETTER_AUTH_URL=https://auth.yourdomain.com
BACKEND_URL=https://api.yourdomain.com
NODE_ENV=production
```

**Access in Config:**

```typescript
// docusaurus.config.ts
const config: Config = {
  customFields: {
    betterAuthUrl: process.env.BETTER_AUTH_URL,
    backendUrl: process.env.BACKEND_URL,
  },
};
```

**Important:** Docusaurus bakes env vars into the build. Client-side code reads from `window.__DOCUSAURUS__`, not `process.env`.

### 6.2 CORS Configuration

**Auth Server:**

```typescript
// auth-server/src/index.ts
import cors from 'cors';

app.use(cors({
  origin: [
    'https://yourdomain.com',
    'https://docs.yourdomain.com',
  ],
  credentials: true, // Allow cookies
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));
```

### 6.3 Security Headers

**Docusaurus Static Hosting (Netlify/Vercel):**

```toml
# netlify.toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=()"
```

### 6.4 Build Optimization

**Webpack Bundle Analysis:**

```bash
npm run build -- --bundle-analyzer
```

**Code Splitting:**

```typescript
// Dynamic imports for auth client
const AuthClient = React.lazy(() => import('../lib/auth-client'));

function LoginPage() {
  return (
    <React.Suspense fallback={<Loading />}>
      <AuthClient />
    </React.Suspense>
  );
}
```

### 6.5 Monitoring & Error Tracking

**Session Validation Errors:**

```typescript
// src/lib/auth-client.ts
export async function getSession() {
  try {
    const client = getAuthClient();
    const result = await client.getSession();
    return result;
  } catch (error) {
    // Log to monitoring service
    console.error('Session validation failed:', error);

    // Optional: Send to Sentry/DataDog
    // Sentry.captureException(error);

    return null;
  }
}
```

---

## Summary of Key Patterns

### ✅ Recommended Approaches

1. **Lazy Singleton + Proxy**: Safe module-scope auth client imports
2. **BrowserOnly Wrapper**: Prevents SSR hydration mismatches
3. **ExecutionEnvironment Guards**: Client-only code execution
4. **Custom Events**: Cross-component auth state synchronization
5. **Dynamic Imports**: Auth client loaded only when needed
6. **useEffect Redirects**: Client-side navigation for protected routes
7. **Return URL Preservation**: Seamless post-login experience
8. **Credentials Include**: Essential for cross-origin cookies
9. **SameSite=None + Secure**: Production cross-origin requirements
10. **JWT Exchange**: Backend API authentication via token endpoint

### ❌ Anti-Patterns to Avoid

1. **Direct process.env in Client Code**: Use `window.__DOCUSAURUS__` instead
2. **SSR Auth Checks**: Always check auth client-side
3. **Synchronous Auth Client Creation**: Use lazy initialization
4. **Hardcoded URLs**: Use customFields for environment-specific URLs
5. **Missing BrowserOnly**: Causes hydration mismatches
6. **SameSite=Strict**: Breaks OAuth flows
7. **Missing Credentials**: Cookies won't be sent cross-origin
8. **Blocking Auth Failures**: Silent degradation is better

---

## Implementation Checklist

- [ ] Install Better Auth: `npm install better-auth`
- [ ] Create auth client with lazy singleton pattern
- [ ] Register client module in `docusaurus.config.ts`
- [ ] Add customFields for auth/backend URLs
- [ ] Configure webpack resolve aliases
- [ ] Create AuthContext provider
- [ ] Wrap app in Root.tsx with AuthProvider
- [ ] Create custom AuthNavbarItem component
- [ ] Register custom navbar component type
- [ ] Create login/register pages in `src/pages/`
- [ ] Implement ProtectedRoute component
- [ ] Swizzle DocPage layout for protected docs
- [ ] Configure Better Auth server with correct cookies
- [ ] Set up CORS and trustedOrigins
- [ ] Test cross-origin session sharing
- [ ] Implement JWT token exchange for backend
- [ ] Add error handling and monitoring
- [ ] Test OAuth flows (Google/GitHub)
- [ ] Verify SSR/SSG compatibility
- [ ] Deploy and test in production

---

## References

- **Better Auth Docs**: https://www.better-auth.com/docs
- **Docusaurus Docs**: https://docusaurus.io/docs
- **Better Auth GitHub**: https://github.com/better-auth/better-auth
- **Docusaurus Swizzling**: https://docusaurus.io/docs/swizzling
- **React Router (Docusaurus)**: https://docusaurus.io/docs/advanced/routing

---

**Document Version:** 1.0
**Last Updated:** 2026-02-26
**Maintained By:** IntelliStack Platform Team
