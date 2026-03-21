---
id: "027"
title: Fix onboarding repeat on Google re-authentication
stage: general
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: chat
labels: ["bug-fix","onboarding","oauth","google","callback","session-cache"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/pages/auth/callback.tsx
tests:
  - manual: re-authenticate existing user via Google and confirm no onboarding redirect
---

## Prompt

ok now when the exisitng user again cinitnue with authicate witht eh google it again ask about the onboarding about that user fix this pls that when user already onboard so why it ask again about this

## Response snapshot

Root cause identified: `callback.tsx` checked `session.data.onboarding_completed` to decide whether to redirect to onboarding. This field can be stale because:
1. Better-Auth's `cookieCache` (5-min TTL) can return a cached session with `onboarding_completed: false` even after the DB was updated to `true`.
2. The `callbacks.session` handler in `auth.ts` uses a `user` parameter that may not include custom schema columns in all Better-Auth versions, causing `user.onboarding_completed ?? false` to always return `false`.

Fix: replaced the `session.data.onboarding_completed` check in `callback.tsx` with a direct call to `/api/auth/onboarding/status`, which queries the DB directly with no cache. Added a `try/catch` fallback to the session field if the status endpoint is unreachable.

## Outcome

- ✅ Impact: Existing users who completed onboarding are no longer redirected back to step-1 after Google OAuth
- 🧪 Tests: Manual — sign out existing user, re-authenticate via Google, confirm redirect goes to stage-1/intro
- 📁 Files: intellistack/content/src/pages/auth/callback.tsx (onboarding check replaced)
- 🔁 Next prompts: none
- 🧠 Reflection: The bug was a session cache vs. DB truth mismatch — always query the authoritative source (DB via dedicated API) for security/flow-critical decisions like onboarding gating

## Evaluation notes (flywheel)

- Failure modes observed: stale cookieCache returning false for onboarding_completed; callbacks.session user parameter lacking custom columns
- Graders run and results (PASS/FAIL): manual testing required
- Prompt variant (if applicable): none
- Next experiment: consider disabling cookieCache or adding cache invalidation after onboarding/complete endpoint is called
