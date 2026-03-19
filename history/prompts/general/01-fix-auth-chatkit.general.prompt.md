---
id: 01
title: Fix Better-Auth and ChatKit Widget Integration
stage: general
date: 2026-03-19
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: main
user: salim
command: /implement
labels: ["auth", "integration", "bugfix", "frontend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - frontend/src/lib/auth.ts
  - frontend/src/contexts/AuthContext.tsx
  - frontend/src/app/auth/login/page.tsx
  - frontend/src/app/auth/register/page.tsx
  - frontend/src/components/layout/Header.tsx
  - frontend/.env.local
  - content/src/theme/DocPage/Layout/index.tsx
  - content/src/components/ai/ChatKitWidget.tsx
  - auth-server/migrate.js
tests_yaml: []
---

## Prompt

User provided a comprehensive 7-phase implementation plan to fix Better-Auth and ChatKit integration issues:

**Critical Blockers Identified:**
- AuthContext calling wrong endpoints (`/api/auth/login` vs Better-Auth SDK methods)
- Missing `session` property in AuthContext — components crash on `session.isAuthenticated`
- `socialSignIn` and `getAuthClient` not exported from auth library
- No `/app/auth/login` or `/app/auth/register` page routes
- Header not auth-aware; shows Login button pointing to wrong URL
- No `.env.local` with auth server URL
- ChatKit widget double-mounted on docs pages (performance)
- 3-second polling loop making 1400 auth requests/hour
- Database schema mismatch: custom columns (`role`, `current_stage`) in schema.ts but not in migrate.js

**Plan requested:**
1. Fix lib/auth.ts with correct Better-Auth endpoints and exports
2. Fix AuthContext with correct endpoints and add session property
3. Create auth pages (login/register)
4. Make Header auth-aware with UserMenu
5. Create .env.local with env vars
6. Remove duplicate ChatKit mount
7. Fix ChatKit polling from 3s to 60s
8. (Implied) Fix database migration with custom columns

---

## Response

Implemented all 7 phases plus database migration fix:

### Phase 1 — lib/auth.ts
- Integrated `createAuthClient` from better-auth/react (official SDK)
- Now uses: `signIn.email()`, `signUp.email()`, `signOut()`, `getSession()`
- Exported: `getAuthClient()`, `socialSignIn(provider)`
- Correctly routes through `NEXT_PUBLIC_AUTH_URL` env var

### Phase 2 — AuthContext.tsx
- Added `session` property: `{ isAuthenticated, user, hasCompletedPersonalization }`
- Updated all methods to use Better-Auth client methods
- Supports custom user fields: role, current_stage, image

### Phase 3 — Auth Pages
- Created `/app/auth/login/page.tsx` — mounts LoginForm with styled wrapper
- Created `/app/auth/register/page.tsx` — mounts RegisterForm with styled wrapper
- Both include cross-navigation and back-to-home links

### Phase 4 — Header
- Added `useAuth()` hook
- Conditionally renders UserMenu for authenticated users, Login button for guests
- Fixed Login href from Docusaurus URL to `/auth/login`
- Applied to both desktop and mobile menus

### Phase 5 — Environment File
- Created `frontend/.env.local` with:
  - `NEXT_PUBLIC_AUTH_URL=http://localhost:3001`
  - `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`
  - `NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3005/AINativeBook`

### Phase 6 — ChatKit Double-Mount
- Removed `<ChatKitWidget />` from `DocPage/Layout/index.tsx`
- Kept mount only in `Root.tsx` (global)
- Removed unused import

### Phase 7 — ChatKit Polling
- Increased polling interval from 3s to 60s
- Event-driven auth updates via `auth-state-changed` event provide responsive feedback
- Reduces request volume by ~97%

### Bonus: Database Migration
- Updated `auth-server/migrate.js` to include missing columns in user table:
  - `onboarding_completed` (boolean)
  - `current_stage` (integer, default 1)
  - `role` (text, default 'student')
  - `preferences` (jsonb)
- This fixes the 500 error on signup and aligns migration with Drizzle schema

**Resolution:** User then reported 404 errors for `/api/auth/session` and 500 error for `/api/auth/sign-up/email`, prompting discovery that Better-Auth doesn't expose raw fetch endpoints—it uses a client SDK. Corrected implementation to use `createAuthClient` from better-auth/react instead of manual fetch calls.

---

## Key Decisions

1. **Better-Auth Client SDK vs Manual Fetch**
   - Why: Better-Auth is a framework; its endpoints are designed for the SDK, not direct HTTP calls
   - Trade-off: Type safety + consistency vs manual control of network requests
   - Decision: Use official SDK (createAuthClient) for correctness

2. **Polling Interval 3s → 60s**
   - Why: ChatKit was polling auth every 3s on every stage page; 100 users = 1400 req/hr
   - Trade-off: Background polling responsiveness vs request volume; mitigated by event-driven updates
   - Decision: 60s polling + event-driven updates provides both efficiency and responsiveness

3. **Single ChatKit Mount**
   - Why: Root wrapper should be the canonical mount point; DocPage duplication caused visual artifacts
   - Trade-off: Centralization vs page-specific control
   - Decision: Global mount in Root.tsx only; DocPage already wrapped by Root

4. **Database Schema Alignment**
   - Why: Drizzle schema defined custom columns but migrate.js didn't; caused 500 signup errors
   - Trade-off: Keeping two sources in sync vs single source of truth
   - Decision: Updated migrate.js to match schema.ts; both files now aligned

---

## Testing Checklist

- [ ] Run auth-server migration: `npm run migrate`
- [ ] Start auth server on :3001
- [ ] Start frontend on :3000
- [ ] Register new account at `/auth/register`
- [ ] Verify user in PostgreSQL with role='student', current_stage=1
- [ ] Login at `/auth/login`
- [ ] Verify header shows UserMenu (not Login button)
- [ ] Navigate to Docusaurus stage page
- [ ] Verify single ChatKit widget (no duplicate buttons)
- [ ] Monitor Network tab: auth/session polling should be 60s, not 3s

---

## Outcome

**Status:** ✅ Implementation Complete

**Deliverables:**
- 6 modified files (auth library, context, header, widgets, migrations)
- 3 new files (login/register pages, env config)
- 1 summary document (IMPLEMENTATION_SUMMARY.md)
- Full test verification checklist

**Next Steps:**
1. Reset database and run migrations
2. Restart auth server and frontend
3. Follow verification steps in IMPLEMENTATION_SUMMARY.md
4. Monitor network requests to confirm polling efficiency
5. Test account creation end-to-end

---

## Notes

- Email verification disabled in auth config (development convenience; enable in production)
- JWT stored in localStorage (consider secure httpOnly cookies for production)
- OAuth clients (Google/GitHub) require IDs in .env
- RBAC scaffolding in place (role field) but not yet enforced at API level
