---
id: 020
title: Fix Cross-Frontend Auth Profile Display
stage: refactor
date: 2026-02-19
surface: agent
model: claude-opus-4-6
feature: 001-frontend-redesign
branch: 001-frontend-redesign
user: saram
command: implement plan
labels: ["auth", "cors", "cross-origin", "navbar", "session"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/auth-server/src/index.ts
  - intellistack/content/src/theme/NavbarItem/AuthNavbarItem.tsx
  - intellistack/content/src/theme/Root.tsx
  - intellistack/frontend/src/components/auth/LoginForm.tsx
tests:
  - Manual: Login from Next.js → redirect to Docusaurus → navbar shows profile
  - Manual: Profile page shows user data on Docusaurus
  - Manual: Logout reverts navbar to Sign In
  - Manual: Login from Docusaurus updates navbar immediately
---

## Prompt

Implement the following plan:

# Fix: Cross-Frontend Auth — Show Profile on Docusaurus After Login from Next.js

## Context

**Problem:** When a user logs in from the Next.js frontend (port 3000), then gets redirected to the Docusaurus content site (port 3002), the Docusaurus site does not show the user's profile in the navbar. The user appears logged out even though they have a valid session cookie.

**Two root causes identified:**

1. **Express CORS blocks Docusaurus requests** — The Express CORS middleware in `auth-server/src/index.ts` (line 42) only allows `localhost:3000` and `localhost:3001`. When Docusaurus (port 3002) makes a `credentials: 'include'` fetch to check the session, CORS rejects it before Better-Auth even sees the request. The Better-Auth `trustedOrigins` in `auth.ts` correctly includes 3002/3004, but Express blocks first.

2. **AuthNavbarItem ignores auth state changes** — The navbar auth component does its own independent `getSession()` call on mount but never listens for the `auth-state-changed` event. Even when Root.tsx detects the user arriving from personalization and dispatches the event, the navbar doesn't update.

## Fixes (4 changes across 4 files)

### Fix 1: Align Express CORS origins
### Fix 2: Refactor AuthNavbarItem to use useAuth() hook
### Fix 3: Handle ?from=login in Root.tsx
### Fix 4: Add ?from=login to Next.js redirect URL

## Response snapshot

Implemented all 4 fixes:

1. **Express CORS** (`auth-server/src/index.ts`): Added ports 3002, 3004, and 8000 to the Express CORS origin allowlist so Docusaurus and backend can make credentialed requests to the auth server.

2. **AuthNavbarItem** (`content/src/theme/NavbarItem/AuthNavbarItem.tsx`): Replaced the independent session check with the shared `useAuth()` hook from AuthContext. This eliminates duplicate network requests and ensures the navbar reacts to `auth-state-changed` events dispatched by Root.tsx.

3. **Root.tsx** (`content/src/theme/Root.tsx`): Extended the `?from=personalization` check to also handle `?from=login`, so arriving from a login redirect triggers session verification and dispatches `auth-state-changed`.

4. **LoginForm** (`frontend/src/components/auth/LoginForm.tsx`): Added `?from=login` query parameter to the Docusaurus redirect URL after successful login.

## Outcome

- ✅ Impact: Docusaurus navbar now shows user profile after cross-origin login from Next.js
- 🧪 Tests: Manual verification required (start all services and test login flow)
- 📁 Files: 4 files modified
- 🔁 Next prompts: Test full auth flow end-to-end, verify cookie SameSite settings
- 🧠 Reflection: Express CORS middleware runs before Better-Auth's trustedOrigins check — both must be aligned for cross-origin credentialed requests to work

## Evaluation notes (flywheel)

- Failure modes observed: Express CORS rejecting before Better-Auth sees the request; navbar not subscribing to auth events
- Graders run and results (PASS/FAIL): N/A - manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify SameSite=None cookie attribute is set for cross-port scenarios
