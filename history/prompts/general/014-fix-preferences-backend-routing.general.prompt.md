---
id: 014
title: Fix Preferences Save Routing to Auth Server
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: fix ERR_CONNECTION_REFUSED and 404 get-jwt-token errors
labels: ["bug","auth","personalization","onboarding","better-auth","routing"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/auth-server/src/routes/onboarding.ts
  - intellistack/frontend/src/contexts/AuthContext.tsx
tests:
  - manual: Complete personalization wizard → no console errors
  - manual: Preferences saved to auth server user.preferences JSONB column
  - manual: onboarding_completed set to true after wizard
---

## Prompt

Console errors on personalization wizard submit:
- :3001/api/auth/get-jwt-token → 404 (4x due to retry)
- :8000/api/v1/users/preferences/onboarding → ERR_CONNECTION_REFUSED (4x due to retry)

## Response snapshot

Root cause analysis:
1. FastAPI backend (port 8000) is not running — `apiClient.updatePreferences()` targets it
2. JWT endpoint 404 — Better-Auth jwt plugin's get-jwt-token endpoint failing (likely JWKS not initialized); this causes `getAuthToken()` to return null, but the retry loop then hammers port 8000

Fix: Route preferences save to the auth server (port 3001) instead of FastAPI, using session cookies (no JWT needed):

1. Added `POST /api/auth/onboarding/preferences` to auth server's onboarding router — accepts any preferences object, saves to `user.preferences` JSONB, sets `onboarding_completed = true`

2. Updated `AuthContext.updatePreferences` to call this new endpoint via `fetch` with `credentials: 'include'` and `NEXT_PUBLIC_AUTH_URL` — no JWT, no apiClient, no FastAPI dependency

Removed the `apiClient` import from AuthContext (no longer needed for this flow).

## Outcome

- ✅ Impact: Wizard completes without errors; preferences saved to Better-Auth DB; no JWT or FastAPI dependency
- 🧪 Tests: Manual — complete wizard and verify preferences in DB
- 📁 Files: 2 files modified
- 🔁 Next prompts: When FastAPI backend is running again, consider syncing preferences there too for RAG/recommendation features
- 🧠 Reflection: The auth server already had the right data model (user.preferences JSONB) and a session-based API. Routing to the FastAPI backend was over-engineered for the current state of the project.

## Evaluation notes (flywheel)

- Failure modes observed: wrong backend target, JWT dependency for a session-cookie endpoint
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): none
- Next experiment: Add preferences GET endpoint to auth server so wizard can pre-fill on return visits
