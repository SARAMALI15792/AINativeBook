---
name: Fix Existing User Personalization Redirect
description: Fixes returning users being incorrectly redirected to /personalization on login by exposing onboarding_completed in the session callback
type: general
stage: green
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: bug fix
labels: ["auth", "session", "onboarding", "bug"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/auth-server/src/auth.ts
  - intellistack/frontend/src/contexts/AuthContext.tsx
tests: []
---

## Prompt

when existing user logout and login it says the again personalize it fix this that issue that why the existing user you are ask to personalize

## Root Cause

Two-part bug:

1. `auth.ts` session callback only added `role` to the session object — `onboarding_completed` and `current_stage` are DB columns but were never exposed through the session callback, so `getSession()` on the frontend always returned `undefined` for these fields.

2. `AuthContext.tsx` computed `hasCompletedPersonalization` from `user?.current_stage > 0` — because `current_stage` was always `undefined`, this evaluated to `false` for every user on every login. `LoginForm.tsx` then redirected all users to `/personalization`.

## Response

**Fix 1 — `auth.ts` session callback:**
Added `onboarding_completed` and `current_stage` to the session callback so they are included in all `getSession()` responses:
```ts
session.user.onboarding_completed = user.onboarding_completed ?? false;
session.user.current_stage = user.current_stage ?? 1;
```

**Fix 2 — `AuthContext.tsx`:**
- Added `onboarding_completed?: boolean` to the `User` interface
- Changed `hasCompletedPersonalization` from `user?.current_stage > 0` to `user?.onboarding_completed ?? false`

This correctly reflects the canonical DB flag set by `POST /api/auth/onboarding/preferences`.
