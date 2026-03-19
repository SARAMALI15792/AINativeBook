# Quickstart Guide: Docusaurus Authentication Migration

**Feature**: 002-docusaurus-auth-migration
**Date**: 2026-02-25
**Audience**: Developers implementing this feature

---

## Overview

This guide provides step-by-step instructions for implementing authentication migration from Next.js to Docusaurus with Better Auth, including a 4-step onboarding flow.

**Estimated Time**: 8-12 hours
**Prerequisites**: Better Auth server running, PostgreSQL database accessible, Node.js 18+

---

## Phase 1: Database Migration (30 minutes)

### Step 1: Create Alembic Migration

```bash
cd intellistack/backend
alembic revision -m "add_onboarding_columns"
```

### Step 2: Edit Migration File

Copy the migration code from `data-model.md` into the generated file:
- Add email_verified, onboarding_completed, current_stage, role, preferences columns
- Create indexes
- Add check constraints

### Step 3: Run Migration

```bash
alembic upgrade head
```

### Step 4: Verify Schema

```bash
psql $DATABASE_URL -c "\d users"
```

Expected columns: id, email, password_hash, name, email_verified, onboarding_completed, current_stage, role, preferences, created_at, updated_at

---

## Phase 2: Better Auth Server Configuration (1 hour)

### Step 1: Update Better Auth Configuration

Edit `intellistack/auth-server/src/auth.ts`:

```typescript
export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: 'pg', schema }),
  baseURL: process.env.BETTER_AUTH_URL!,
  basePath: '/api/auth',
  secret: process.env.BETTER_AUTH_SECRET!,

  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Dev only
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },

  session: {
    expiresIn: 24 * 60 * 60, // 24 hours
    updateAgeSession: 60 * 60, // Refresh after 1 hour
  },

  advanced: {
    defaultCookieAttributes: {
      sameSite: process.env.NODE_ENV === 'production' ? 'lax' : 'lax',
      secure: process.env.NODE_ENV === 'production',
      path: '/',
    },
  },

  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
      redirectURI: `${process.env.BETTER_AUTH_URL!}/api/auth/callback/google`,
    },
  },
});
```

### Step 2: Add Onboarding Endpoints

Create `intellistack/auth-server/src/routes/onboarding.ts`:

```typescript
import { Router } from 'express';
import { auth } from '../auth';

const router = Router();

// Get onboarding status
router.get('/status', async (req, res) => {
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) return res.status(401).json({ error: 'UNAUTHORIZED' });

  const user = session.user;
  const preferences = user.preferences || {};

  const completedSteps = [];
  if (preferences.basic_info) completedSteps.push('basic_info');
  if (preferences.education) completedSteps.push('education');
  if (preferences.interests) completedSteps.push('interests');
  if (preferences.additional) completedSteps.push('additional');

  res.json({
    onboarding_completed: user.onboarding_completed,
    current_step: completedSteps.length + 1,
    completed_steps: completedSteps,
    preferences,
  });
});

// Save onboarding step
router.post('/step', async (req, res) => {
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) return res.status(401).json({ error: 'UNAUTHORIZED' });

  const { step, data } = req.body;

  // Validate step data (add validation logic)

  // Update user preferences
  const currentPreferences = session.user.preferences || {};
  const updatedPreferences = {
    ...currentPreferences,
    [step]: data,
  };

  await db.update(users)
    .set({ preferences: updatedPreferences })
    .where(eq(users.id, session.user.id));

  const allStepsComplete =
    updatedPreferences.basic_info &&
    updatedPreferences.education &&
    updatedPreferences.interests &&
    updatedPreferences.additional;

  res.json({
    success: true,
    onboarding_completed: allStepsComplete,
    next_step: getNextStep(step),
  });
});

// Complete onboarding
router.post('/complete', async (req, res) => {
  const session = await auth.api.getSession({ headers: req.headers });
  if (!session) return res.status(401).json({ error: 'UNAUTHORIZED' });

  const preferences = session.user.preferences || {};
  const allStepsComplete =
    preferences.basic_info &&
    preferences.education &&
    preferences.interests &&
    preferences.additional;

  if (!allStepsComplete) {
    return res.status(400).json({
      error: 'INCOMPLETE_ONBOARDING',
      message: 'All onboarding steps must be completed',
    });
  }

  await db.update(users)
    .set({ onboarding_completed: true })
    .where(eq(users.id, session.user.id));

  res.json({ success: true, user: { id: session.user.id, onboarding_completed: true } });
});

export default router;
```

### Step 3: Register Onboarding Routes

Edit `intellistack/auth-server/src/index.ts`:

```typescript
import onboardingRoutes from './routes/onboarding';

app.use('/api/auth/onboarding', onboardingRoutes);
```

### Step 4: Restart Auth Server

```bash
cd intellistack/auth-server
npm run dev
```

---

## Phase 3: Docusaurus Configuration (2 hours)

### Step 1: Update Docusaurus Config

Edit `intellistack/content/docusaurus.config.ts`:

```typescript
export default {
  url: process.env.NODE_ENV === 'production'
    ? 'https://saramali15792.github.io'
    : 'http://localhost:3005',
  baseUrl: '/AINativeBook/',
  trailingSlash: false,

  customFields: {
    betterAuthUrl: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
  },

  clientModules: ['./src/clientModules/authInit.ts'],

  presets: [
    ['classic', {
      docs: {
        routeBasePath: '/',
        sidebarPath: './sidebars.ts',
      },
    }],
  ],

  themeConfig: {
    navbar: {
      items: [
        { type: 'custom-authNavbarItem', position: 'right' },
      ],
    },
  },
};
```

### Step 2: Create Auth Client

Create `intellistack/content/src/lib/auth.ts`:

```typescript
import { ExecutionEnvironment } from '@docusaurus/ExecutionEnvironment';

let authClientInstance = null;

export const getAuthClient = () => {
  if (!ExecutionEnvironment.canUseDOM) return null;

  if (!authClientInstance) {
    const baseURL = process.env.BETTER_AUTH_URL || 'http://localhost:3001';

    authClientInstance = {
      signUp: async (email, password, name) => {
        const res = await fetch(`${baseURL}/api/auth/sign-up/email`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password, name }),
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Signup failed');
        return res.json();
      },

      signIn: async (email, password) => {
        const res = await fetch(`${baseURL}/api/auth/sign-in/email`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
          credentials: 'include',
        });
        if (!res.ok) throw new Error('Login failed');
        return res.json();
      },

      signOut: async () => {
        const res = await fetch(`${baseURL}/api/auth/sign-out`, {
          method: 'POST',
          credentials: 'include',
        });
        return res.json();
      },

      getSession: async () => {
        const res = await fetch(`${baseURL}/api/auth/get-session`, {
          credentials: 'include',
        });
        if (!res.ok) return null;
        return res.json();
      },

      socialSignIn: async (provider) => {
        const res = await fetch(`${baseURL}/api/auth/oauth/${provider}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            callbackURL: `${window.location.origin}/AINativeBook/auth/callback`,
          }),
          credentials: 'include',
        });
        const data = await res.json();
        if (data.url) window.location.href = data.url;
      },
    };
  }

  return authClientInstance;
};
```

### Step 3: Create Auth Context

Create `intellistack/content/src/contexts/AuthContext.tsx`:

```typescript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getAuthClient } from '../lib/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSession = async () => {
      const client = getAuthClient();
      if (!client) return;

      try {
        const session = await client.getSession();
        setUser(session?.user || null);
      } catch (error) {
        console.error('Session load failed:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadSession();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

### Step 4: Wrap Root with AuthProvider

Create `intellistack/content/src/theme/Root.tsx`:

```typescript
import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';

export default function Root({ children }) {
  return <AuthProvider>{children}</AuthProvider>;
}
```

---

## Phase 4: Authentication Pages (2 hours)

### Step 1: Create Login Page

Create `intellistack/content/src/pages/auth/login.tsx`:

```typescript
import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import { getAuthClient } from '@site/src/lib/auth';
import { useHistory } from '@docusaurus/router';

export default function LoginPage() {
  return (
    <Layout title="Login">
      <BrowserOnly fallback={<div>Loading...</div>}>
        {() => <LoginForm />}
      </BrowserOnly>
    </Layout>
  );
}

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const client = getAuthClient();
      const result = await client.signIn(email, password);

      if (!result.user.onboarding_completed) {
        history.push('/onboarding/step-1');
      } else {
        history.push('/stage-1/intro');
      }
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  const handleGoogleLogin = async () => {
    const client = getAuthClient();
    await client.socialSignIn('google');
  };

  return (
    <div style={{ maxWidth: 400, margin: '50px auto', padding: 20 }}>
      <h1>Login</h1>
      {error && <div style={{ color: 'red', marginBottom: 10 }}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ width: '100%', padding: 10, marginBottom: 10 }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: '100%', padding: 10, marginBottom: 10 }}
        />
        <button type="submit" style={{ width: '100%', padding: 10 }}>
          Login
        </button>
      </form>

      <div style={{ margin: '20px 0', textAlign: 'center' }}>OR</div>

      <button onClick={handleGoogleLogin} style={{ width: '100%', padding: 10 }}>
        Login with Google
      </button>

      <p style={{ marginTop: 20, textAlign: 'center' }}>
        Don't have an account? <a href="/auth/signup">Sign up</a>
      </p>
    </div>
  );
}
```

### Step 2: Create Signup Page

Create `intellistack/content/src/pages/auth/signup.tsx` (similar structure to login)

### Step 3: Create OAuth Callback Page

Create `intellistack/content/src/pages/auth/callback.tsx`:

```typescript
import React, { useEffect } from 'react';
import { useHistory } from '@docusaurus/router';
import { getAuthClient } from '@site/src/lib/auth';

export default function OAuthCallback() {
  const history = useHistory();

  useEffect(() => {
    const checkOnboarding = async () => {
      const client = getAuthClient();
      const session = await client.getSession();

      if (!session?.user) {
        history.push('/auth/login?error=oauth_failed');
        return;
      }

      if (!session.user.onboarding_completed) {
        history.push('/onboarding/step-1');
      } else {
        history.push('/stage-1/intro');
      }
    };

    checkOnboarding();
  }, [history]);

  return <div>Completing authentication...</div>;
}
```

---

## Phase 5: Onboarding Pages (3 hours)

### Step 1: Create Onboarding Step 1

Create `intellistack/content/src/pages/onboarding/step-1.tsx`:

```typescript
import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';
import { useHistory } from '@docusaurus/router';

export default function OnboardingStep1() {
  return (
    <Layout title="Onboarding - Step 1">
      <BrowserOnly>{() => <Step1Form />}</BrowserOnly>
    </Layout>
  );
}

function Step1Form() {
  const [fullName, setFullName] = useState('');
  const [language, setLanguage] = useState('en');
  const [timezone, setTimezone] = useState('America/New_York');
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const baseURL = process.env.BETTER_AUTH_URL || 'http://localhost:3001';
    const res = await fetch(`${baseURL}/api/auth/onboarding/step`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        step: 'basic_info',
        data: { full_name: fullName, preferred_language: language, timezone },
      }),
      credentials: 'include',
    });

    if (res.ok) {
      history.push('/onboarding/step-2');
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: '50px auto', padding: 20 }}>
      <div style={{ marginBottom: 30, textAlign: 'center' }}>
        <div style={{ fontSize: 14, color: '#666' }}>
          Step 1 → 2 → 3 → 4
        </div>
      </div>

      <h1>Basic Information</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 20 }}>
          <label>Full Name *</label>
          <input
            type="text"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
            style={{ width: '100%', padding: 10 }}
          />
        </div>

        <div style={{ marginBottom: 20 }}>
          <label>Preferred Language *</label>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            required
            style={{ width: '100%', padding: 10 }}
          >
            <option value="en">English</option>
            <option value="ur">Urdu</option>
          </select>
        </div>

        <div style={{ marginBottom: 20 }}>
          <label>Timezone *</label>
          <select
            value={timezone}
            onChange={(e) => setTimezone(e.target.value)}
            required
            style={{ width: '100%', padding: 10 }}
          >
            <option value="America/New_York">Eastern Time</option>
            <option value="America/Chicago">Central Time</option>
            <option value="America/Denver">Mountain Time</option>
            <option value="America/Los_Angeles">Pacific Time</option>
            <option value="Asia/Karachi">Pakistan Time</option>
          </select>
        </div>

        <button type="submit" style={{ width: '100%', padding: 10 }}>
          Next
        </button>
      </form>
    </div>
  );
}
```

### Step 2: Create Steps 2, 3, 4

Create similar pages for:
- `step-2.tsx` (Educational Background)
- `step-3.tsx` (Academic Interests)
- `step-4.tsx` (Additional Details)

Step 4 should call `/api/auth/onboarding/complete` and redirect to `/stage-1/intro`

---

## Phase 6: Protected Routes (1 hour)

### Step 1: Create ProtectedRoute Component

Create `intellistack/content/src/components/ProtectedRoute.tsx`:

```typescript
import React, { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useHistory } from '@docusaurus/router';

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  const history = useHistory();

  useEffect(() => {
    if (!loading && !user) {
      history.push('/auth/login?returnUrl=' + window.location.pathname);
    } else if (!loading && user && !user.onboarding_completed) {
      history.push('/onboarding/step-1');
    }
  }, [user, loading, history]);

  if (loading) return <div>Loading...</div>;
  if (!user || !user.onboarding_completed) return null;

  return <>{children}</>;
}
```

### Step 2: Swizzle DocPage Layout

```bash
cd intellistack/content
npm run swizzle @docusaurus/theme-classic DocPage/Layout -- --eject
```

### Step 3: Wrap DocPage with ProtectedRoute

Edit `intellistack/content/src/theme/DocPage/Layout/index.tsx`:

```typescript
import ProtectedRoute from '@site/src/components/ProtectedRoute';

export default function DocPageLayout(props) {
  return (
    <ProtectedRoute>
      <OriginalDocPageLayout {...props} />
    </ProtectedRoute>
  );
}
```

---

## Phase 7: Custom Navbar (1 hour)

### Step 1: Swizzle NavbarItem ComponentTypes

```bash
npm run swizzle @docusaurus/theme-classic NavbarItem/ComponentTypes -- --eject
```

### Step 2: Create AuthNavbarItem

Create `intellistack/content/src/components/AuthNavbarItem.tsx`:

```typescript
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useAuth } from '../contexts/AuthContext';
import { getAuthClient } from '../lib/auth';

export default function AuthNavbarItem() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => <AuthNavbarItemInner />}
    </BrowserOnly>
  );
}

function AuthNavbarItemInner() {
  const { user, setUser } = useAuth();

  const handleLogout = async () => {
    const client = getAuthClient();
    await client.signOut();
    setUser(null);
    window.location.href = '/auth/login';
  };

  if (!user) {
    return (
      <>
        <a href="/auth/login" className="navbar__item navbar__link">
          Login
        </a>
        <a href="/auth/signup" className="navbar__item navbar__link">
          Sign Up
        </a>
      </>
    );
  }

  return (
    <div className="navbar__item dropdown dropdown--hoverable">
      <a className="navbar__link">{user.name}</a>
      <ul className="dropdown__menu">
        <li><a href="/profile" className="dropdown__link">Profile</a></li>
        <li><a href="/settings" className="dropdown__link">Settings</a></li>
        <li><button onClick={handleLogout} className="dropdown__link">Logout</button></li>
      </ul>
    </div>
  );
}
```

### Step 3: Register Custom Component

Edit `intellistack/content/src/theme/NavbarItem/ComponentTypes.tsx`:

```typescript
import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import AuthNavbarItem from '@site/src/components/AuthNavbarItem';

export default {
  ...ComponentTypes,
  'custom-authNavbarItem': AuthNavbarItem,
};
```

---

## Phase 8: Next.js Simplification (1 hour)

### Step 1: Remove Auth Files

```bash
cd intellistack/frontend
rm -rf src/lib/auth.ts
rm -rf src/contexts/AuthContext.tsx
rm -rf src/components/UserMenu.tsx
rm -rf src/components/ProtectedRoute.tsx
rm -rf src/app/auth
rm -rf src/middleware.ts
```

### Step 2: Update Header Component

Edit `intellistack/frontend/src/components/layout/Header.tsx`:

```typescript
const navLinks = [
  { label: 'Home', href: '/' },
  {
    label: 'Book',
    href: `${process.env.NEXT_PUBLIC_DOCUSAURUS_URL}/stage-1/intro`,
    external: true
  },
  {
    label: 'Login',
    href: `${process.env.NEXT_PUBLIC_DOCUSAURUS_URL}/auth/login`,
    external: true
  },
  { label: 'Community', href: '#', badge: 'Coming Soon' },
  { label: 'AI Tutor', href: '#', badge: 'Coming Soon' },
];
```

### Step 3: Update Environment Variables

Edit `intellistack/frontend/.env.local`:

```bash
NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3005/AINativeBook
```

---

## Phase 9: Testing (2 hours)

### Test Checklist

**Authentication Flow**:
- [ ] Sign up with email/password creates user
- [ ] Sign in with valid credentials succeeds
- [ ] Sign in with invalid credentials fails
- [ ] Sign out clears session
- [ ] Google OAuth flow completes successfully
- [ ] Session persists after browser close (within 24 hours)

**Onboarding Flow**:
- [ ] Step 1 saves basic info and advances to Step 2
- [ ] Step 2 saves education and advances to Step 3
- [ ] Step 3 saves interests and advances to Step 4
- [ ] Step 4 saves additional details and marks onboarding complete
- [ ] Incomplete onboarding redirects to correct step on login
- [ ] Completed onboarding allows access to book content

**Protected Routes**:
- [ ] Unauthenticated users redirected to login
- [ ] Authenticated users without onboarding redirected to Step 1
- [ ] Authenticated users with onboarding can access all content
- [ ] Direct URL access to protected routes enforces checks

**Routing**:
- [ ] Next.js "Book" link redirects to Docusaurus without 404
- [ ] Next.js "Login" link redirects to Docusaurus auth
- [ ] Docusaurus internal links work correctly
- [ ] No trailing slash issues

**Session Management**:
- [ ] Session cookie set correctly (HttpOnly, Secure in prod, SameSite=Lax)
- [ ] Session validates on protected route access
- [ ] Session expires after 24 hours
- [ ] Multiple concurrent sessions work correctly

---

## Troubleshooting

### Issue: "window is not defined" during build

**Solution**: Wrap client-only code with `BrowserOnly` or `ExecutionEnvironment.canUseDOM` check

### Issue: Session cookie not sent with requests

**Solution**: Ensure `credentials: 'include'` in all fetch calls and CORS configured correctly

### Issue: 404 errors on Docusaurus routes

**Solution**: Verify `baseUrl='/AINativeBook/'` and `routeBasePath='/'` in docusaurus.config.ts

### Issue: OAuth redirect fails

**Solution**: Check `redirectURI` in Better Auth config matches actual callback URL

### Issue: Onboarding data not saving

**Solution**: Verify database migration ran successfully and preferences column exists

---

## Deployment Checklist

**Before Production**:
- [ ] Update environment variables for production URLs
- [ ] Enable email verification (set `requireEmailVerification: true`)
- [ ] Configure production OAuth credentials
- [ ] Set `SameSite=lax` and `Secure=true` for cookies
- [ ] Enable rate limiting on auth endpoints
- [ ] Set up monitoring for auth failures
- [ ] Test OAuth flow with production URLs
- [ ] Verify CORS origins for production domains
- [ ] Run database migration on production database
- [ ] Test session persistence across deployments

---

## Next Steps

After completing this quickstart:
1. Run `/sp.tasks` to generate detailed task breakdown
2. Implement tasks in order (database → auth server → Docusaurus → Next.js)
3. Test each phase before moving to next
4. Create PHR after completing implementation

---

**Quickstart Complete**: 2026-02-25
**Next Command**: `/sp.tasks`
