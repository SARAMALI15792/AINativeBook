# Research: Docusaurus Authentication Migration & Onboarding

**Feature**: 002-docusaurus-auth-migration
**Date**: 2026-02-25
**Phase**: 0 - Research & Technical Decisions

---

## Overview

This document consolidates research findings for migrating authentication from Next.js to Docusaurus using Better Auth, implementing a 4-step onboarding flow, fixing routing issues, and simplifying the Next.js frontend.

---

## Technical Decisions

### Decision 1: Better Auth Client Integration in Docusaurus

**Decision**: Use lazy singleton pattern with Proxy for Better Auth client initialization in Docusaurus

**Rationale**:
- Docusaurus uses SSR/SSG, requiring careful handling of client-only code
- Lazy initialization prevents "window is not defined" errors during build
- Proxy pattern allows safe module-scope imports without immediate initialization
- Graceful degradation when auth server is unreachable

**Implementation Pattern**:
```typescript
// src/lib/auth.ts
import { ExecutionEnvironment } from '@docusaurus/ExecutionEnvironment';

let authClientInstance = null;

export const getAuthClient = () => {
  if (!ExecutionEnvironment.canUseDOM) return null;

  if (!authClientInstance) {
    authClientInstance = createAuthClient({
      baseURL: process.env.BETTER_AUTH_URL,
      fetchOptions: { credentials: 'include' }
    });
  }

  return authClientInstance;
};
```

**Alternatives Considered**:
- Direct import: Rejected due to SSR build failures
- Dynamic import: Rejected due to complexity and async handling issues
- Global window object: Rejected due to type safety concerns

**References**: Docusaurus ExecutionEnvironment API, Better Auth client documentation

---

### Decision 2: Custom Pages for Authentication in Docusaurus

**Decision**: Use Docusaurus `src/pages/` directory for auth pages with BrowserOnly wrapper

**Rationale**:
- Docusaurus automatically creates routes from `src/pages/` directory
- Pages outside docs structure don't require sidebar configuration
- BrowserOnly wrapper prevents SSR hydration mismatches
- Supports dynamic imports for client-only components

**Implementation Pattern**:
```typescript
// src/pages/auth/login.tsx
import BrowserOnly from '@docusaurus/BrowserOnly';
import Layout from '@theme/Layout';

export default function LoginPage() {
  return (
    <Layout title="Login">
      <BrowserOnly fallback={<div>Loading...</div>}>
        {() => {
          const LoginForm = require('@site/src/components/auth/LoginForm').default;
          return <LoginForm />;
        }}
      </BrowserOnly>
    </Layout>
  );
}
```

**Page Structure**:
- `/auth/login` → `src/pages/auth/login.tsx`
- `/auth/signup` → `src/pages/auth/signup.tsx`
- `/onboarding/step-1` → `src/pages/onboarding/step-1.tsx`
- `/onboarding/step-2` → `src/pages/onboarding/step-2.tsx`
- `/onboarding/step-3` → `src/pages/onboarding/step-3.tsx`
- `/onboarding/step-4` → `src/pages/onboarding/step-4.tsx`

**Alternatives Considered**:
- Swizzling DocPage: Rejected due to complexity and maintenance burden
- External auth app: Rejected due to cross-origin cookie complications
- Plugin-based routing: Rejected due to Docusaurus plugin API limitations

**References**: Docusaurus Pages documentation, BrowserOnly component API

---

### Decision 3: Custom Navbar Components for Auth State

**Decision**: Swizzle NavbarItem/ComponentTypes and register custom AuthNavbarItem component

**Rationale**:
- Docusaurus supports custom navbar item types via ComponentTypes
- Swizzling allows full control over navbar rendering
- AuthContext provider enables centralized auth state management
- Custom events for auth state changes prevent prop drilling

**Implementation Pattern**:
```typescript
// src/theme/NavbarItem/ComponentTypes.tsx
import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import AuthNavbarItem from '@site/src/components/AuthNavbarItem';

export default {
  ...ComponentTypes,
  'custom-authNavbarItem': AuthNavbarItem,
};
```

**Navbar Configuration**:
```typescript
// docusaurus.config.ts
navbar: {
  items: [
    { type: 'custom-authNavbarItem', position: 'right' }
  ]
}
```

**Alternatives Considered**:
- Direct navbar modification: Rejected due to lack of auth state access
- Client module injection: Rejected due to timing issues with navbar render
- CSS-only show/hide: Rejected due to security concerns (content still in DOM)

**References**: Docusaurus Swizzling documentation, NavbarItem ComponentTypes API

---

### Decision 4: Protected Routes Implementation

**Decision**: Use client-side route guards with useEffect-based redirects

**Rationale**:
- Docusaurus is primarily a static site generator (SSR/SSG)
- Server-side auth checks not feasible in static deployment
- Client-side checks provide adequate protection for content access
- useEffect ensures checks run after hydration

**Implementation Pattern**:
```typescript
// src/components/ProtectedRoute.tsx
import { useEffect } from 'react';
import { useAuth } from '@site/src/contexts/AuthContext';
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

**Protection Strategy**:
- Wrap DocPage layout with ProtectedRoute component
- Check authentication status on mount
- Redirect to login if unauthenticated
- Redirect to onboarding if incomplete
- Show loading state during auth check

**Alternatives Considered**:
- Server-side rendering with auth: Rejected due to static deployment model
- Build-time auth checks: Rejected due to dynamic user state
- Service worker auth: Rejected due to complexity and browser support

**References**: Docusaurus Router API, React useEffect patterns

---

### Decision 5: Session Cookie Configuration

**Decision**: Use SameSite=Lax for development, SameSite=None + Secure for production (same-domain deployment)

**Rationale**:
- Production deployment uses same domain with different paths (e.g., intellistack.com and intellistack.com/AINativeBook)
- Same-domain deployment simplifies cookie sharing (no cross-domain issues)
- SameSite=Lax sufficient for same-domain, prevents CSRF
- SameSite=None + Secure required only if cross-origin OAuth redirects
- Development uses localhost with different ports, requires Lax

**Cookie Configuration**:
```typescript
// Better Auth configuration
advanced: {
  defaultCookieAttributes: {
    sameSite: process.env.NODE_ENV === 'production' ? 'lax' : 'lax',
    secure: process.env.NODE_ENV === 'production',
    path: '/',
    domain: undefined, // Same domain, no explicit domain needed
  }
}
```

**Session Validation Pattern**:
```typescript
// Client-side session check
const validateSession = async () => {
  try {
    const response = await fetch(`${AUTH_URL}/api/auth/get-session`, {
      credentials: 'include'
    });
    if (response.ok) {
      const data = await response.json();
      return data.user;
    }
    return null;
  } catch (error) {
    console.error('Session validation failed:', error);
    return null;
  }
};
```

**Alternatives Considered**:
- Cross-subdomain cookies (domain=.intellistack.com): Rejected due to same-domain deployment
- Token-based auth (localStorage): Rejected due to XSS vulnerability and Better Auth cookie-based design
- SameSite=Strict: Rejected due to OAuth redirect breakage

**References**: Better Auth cookie configuration, MDN SameSite documentation

---

### Decision 6: Docusaurus Routing Configuration

**Decision**: Configure baseUrl='/AINativeBook/', routeBasePath='/', trailingSlash=false

**Rationale**:
- GitHub Pages deployment requires baseUrl matching repository name
- routeBasePath='/' serves docs at root of baseUrl (not /docs/)
- trailingSlash=false prevents duplicate URL issues
- Consistent with existing Docusaurus configuration

**Configuration**:
```typescript
// docusaurus.config.ts
export default {
  url: process.env.NODE_ENV === 'production'
    ? 'https://saramali15792.github.io'
    : 'http://localhost:3005',
  baseUrl: '/AINativeBook/',
  trailingSlash: false,

  presets: [
    ['classic', {
      docs: {
        routeBasePath: '/', // Docs at root of baseUrl
        sidebarPath: './sidebars.ts',
      }
    }]
  ]
};
```

**URL Structure**:
- Production: `https://saramali15792.github.io/AINativeBook/stage-1/intro`
- Development: `http://localhost:3005/AINativeBook/stage-1/intro`
- Auth pages: `/AINativeBook/auth/login`
- Onboarding: `/AINativeBook/onboarding/step-1`

**Alternatives Considered**:
- routeBasePath='/docs/': Rejected due to longer URLs and inconsistency
- baseUrl='/': Rejected due to GitHub Pages repository structure
- trailingSlash=true: Rejected due to duplicate content issues

**References**: Docusaurus configuration documentation, GitHub Pages deployment guide

---

### Decision 7: Next.js Simplification Strategy

**Decision**: Remove all authentication code from Next.js, convert to pure marketing site with external redirects

**Rationale**:
- Consolidates authentication in single location (Docusaurus)
- Eliminates code duplication and maintenance burden
- Simplifies Next.js to static marketing pages
- Clear separation of concerns (marketing vs learning platform)

**Removal Checklist**:
- ❌ `lib/auth.ts` - Better Auth client
- ❌ `contexts/AuthContext.tsx` - Auth context provider
- ❌ `components/UserMenu.tsx` - User dropdown
- ❌ `components/ProtectedRoute.tsx` - Route guards
- ❌ `app/auth/*` - Auth pages (login, register, etc.)
- ❌ `middleware.ts` - Auth middleware
- ❌ `app/api/auth/*` - Auth API routes

**Simplified Header**:
```typescript
// components/layout/Header.tsx
const navLinks = [
  { label: 'Home', href: '/' },
  { label: 'Book', href: process.env.NEXT_PUBLIC_DOCUSAURUS_URL + '/stage-1/intro', external: true },
  { label: 'Login', href: process.env.NEXT_PUBLIC_DOCUSAURUS_URL + '/auth/login', external: true },
  { label: 'Community', href: '#', badge: 'Coming Soon' },
  { label: 'AI Tutor', href: '#', badge: 'Coming Soon' },
];
```

**Alternatives Considered**:
- Keep minimal auth for session display: Rejected due to complexity and duplication
- Iframe embedding: Rejected due to security and UX concerns
- Shared auth library: Rejected due to unnecessary abstraction

**References**: Next.js documentation, separation of concerns principles

---

### Decision 8: Onboarding Data Storage

**Decision**: Store onboarding data in users.preferences JSON field with structured schema

**Rationale**:
- Flexible schema allows easy addition of new questions
- No database migrations needed for onboarding changes
- Single JSON field simplifies queries and updates
- Structured format ensures data consistency

**Schema Structure**:
```typescript
interface OnboardingPreferences {
  basic_info: {
    full_name: string;
    preferred_language: 'en' | 'ur';
    timezone: string;
  };
  education: {
    level: 'high_school' | 'undergraduate' | 'graduate' | 'professional';
    field_of_study: string;
    prior_experience: 'none' | 'beginner' | 'intermediate' | 'advanced';
  };
  interests: {
    learning_goals: ('career_change' | 'academic_research' | 'hobby' | 'professional_development')[];
    learning_style: 'visual' | 'reading' | 'hands_on' | 'mixed';
    topics_of_interest: ('ros2' | 'simulation' | 'perception' | 'ai_integration' | 'hardware')[];
  };
  additional: {
    github_username?: string;
    linkedin_url?: string;
    bio?: string;
  };
}
```

**Save Strategy**:
- Save on step completion (clicking "Next" or "Complete")
- No auto-save within steps (clarified in spec)
- Atomic updates to prevent partial data

**Alternatives Considered**:
- Separate onboarding table: Rejected due to unnecessary complexity
- Individual columns: Rejected due to schema rigidity
- NoSQL document store: Rejected due to existing PostgreSQL infrastructure

**References**: PostgreSQL JSON field documentation, TypeScript type safety

---

### Decision 9: Database Migration Strategy

**Decision**: Create Alembic migration to add missing user columns if they don't exist

**Rationale**:
- Existing users table may not have all required columns
- Idempotent migration prevents errors on re-run
- Preserves existing data
- Supports incremental rollout

**Migration Pattern**:
```python
# alembic/versions/YYYYMMDD_add_onboarding_columns.py
def upgrade():
    # Add columns if they don't exist
    op.execute("""
        ALTER TABLE users
        ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS current_stage INTEGER DEFAULT 1,
        ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'student',
        ADD COLUMN IF NOT EXISTS preferences JSONB;
    """)

    # Create indexes
    op.create_index('idx_users_onboarding_completed', 'users', ['onboarding_completed'], if_not_exists=True)
    op.create_index('idx_users_current_stage', 'users', ['current_stage'], if_not_exists=True)

def downgrade():
    # Remove columns
    op.drop_column('users', 'preferences')
    op.drop_column('users', 'role')
    op.drop_column('users', 'current_stage')
    op.drop_column('users', 'onboarding_completed')
    op.drop_column('users', 'email_verified')
```

**Alternatives Considered**:
- Manual SQL scripts: Rejected due to lack of version control
- ORM-only migrations: Rejected due to conditional column creation complexity
- Separate onboarding table: Rejected due to unnecessary joins

**References**: Alembic documentation, PostgreSQL ALTER TABLE IF NOT EXISTS

---

### Decision 10: Environment Variable Management

**Decision**: Use separate .env files for each service with clear naming conventions

**Rationale**:
- Each service (Next.js, Docusaurus, Auth Server, Backend) has different env needs
- Clear prefixes prevent confusion (NEXT_PUBLIC_, BETTER_AUTH_, etc.)
- Supports different values per environment (dev, staging, prod)

**Environment Variables**:

**Auth Server (.env)**:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/intellistack
BETTER_AUTH_SECRET=min-32-chars-secret-key
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_AUDIENCE=intellistack-api
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
CORS_ORIGINS=http://localhost:3000,http://localhost:3005
```

**Docusaurus (.env)**:
```bash
BETTER_AUTH_URL=http://localhost:3001
BACKEND_URL=http://localhost:8000
```

**Next.js (.env.local)**:
```bash
NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3005/AINativeBook
```

**Backend (.env)**:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/intellistack
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_JWKS_URL=http://localhost:3001/.well-known/jwks.json
```

**Alternatives Considered**:
- Single .env file: Rejected due to confusion and security concerns
- Environment-specific files (.env.dev, .env.prod): Rejected due to deployment complexity
- Secrets management service: Deferred to production deployment phase

**References**: Twelve-Factor App methodology, environment variable best practices

---

## Implementation Checklist

### Phase 0: Research ✅
- [x] Better Auth client integration patterns
- [x] Docusaurus custom pages approach
- [x] Custom navbar components strategy
- [x] Protected routes implementation
- [x] Session cookie configuration
- [x] Routing configuration decisions
- [x] Next.js simplification strategy
- [x] Onboarding data storage schema
- [x] Database migration approach
- [x] Environment variable management

### Phase 1: Design (Next)
- [ ] Data model documentation
- [ ] API contracts definition
- [ ] Component architecture
- [ ] Quickstart guide

### Phase 2: Tasks (After Phase 1)
- [ ] Task breakdown with dependencies
- [ ] Acceptance criteria per task
- [ ] Complexity estimates

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SSR/SSG auth check failures | Medium | High | Use client-side checks only, BrowserOnly wrapper |
| Cookie sharing issues | Low | High | Same-domain deployment, proper SameSite config |
| Onboarding data loss | Low | Medium | Save on step completion, clear user messaging |
| OAuth redirect failures | Medium | Medium | Proper callback URL configuration, error handling |
| Session validation errors | Medium | Medium | Graceful degradation, retry logic |
| Routing 404 errors | Low | High | Correct baseUrl/routeBasePath configuration |
| Next.js auth code removal | Low | Low | Thorough testing, gradual rollout |

---

## References

- [Better Auth Documentation](https://better-auth.com)
- [Docusaurus Documentation](https://docusaurus.io)
- [Docusaurus Swizzling Guide](https://docusaurus.io/docs/swizzling)
- [PostgreSQL JSON Functions](https://www.postgresql.org/docs/current/functions-json.html)
- [Alembic Migrations](https://alembic.sqlalchemy.org)
- [MDN SameSite Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

---

**Research Complete**: 2026-02-25
**Next Phase**: Data Model & Contracts (Phase 1)
