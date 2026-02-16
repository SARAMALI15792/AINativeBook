---
id: "020"
title: "Fix Signup Flow - CORS, JWKS, JWT, JIT Provisioning"
stage: "refactor"
date: "2026-02-15"
surface: "agent"
model: "minimax-m2.5:cloud"
feature: "001-intellistack-platform"
branch: "main"
user: "saram"
command: "Implement the signup flow fix plan"
labels: [auth, cors, jwt, jwks, jit-provisioning, better-auth]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/auth-server/.env
  - intellistack/auth-server/package.json
  - intellistack/auth-server/src/index.ts
  - intellistack/auth-server/src/auth.ts
  - intellistack/backend/.env
  - intellistack/backend/src/core/users/routes.py
tests: []
---

## Prompt

Implement the following plan:

# Fix Signup Flow - Implementation Plan

## Context

The signup flow is broken due to 6 interconnected issues across the auth server, backend, and frontend. A user currently cannot sign up because: (1) CORS blocks the frontend→auth-server request, (2) the JWKS endpoint returns empty keys so JWT validation fails, (3) the JWT algorithm config is mismatched, and (4) even if auth succeeds, the backend has no user sync mechanism so `/api/v1/users/me` returns 404. This plan fixes all issues in dependency order.

## Execution

1. **Step 1: Fix CORS on auth server** - Add `CORS_ORIGINS=http://localhost:3000,http://localhost:3001` to auth-server .env

2. **Step 2: Fix dev script** - Change dev script from `dotenv -e .env -- tsx watch src/index.ts` to `tsx watch src/index.ts` (dotenv-cli not installed)

3. **Step 3: Fix JWKS endpoint** - Replace empty JWKS handler with proxy to Better-Auth's internal JWKS

4. **Step 4: Fix JWT algorithm** - Remove `crv: 'P-256'` from keyPairConfig in auth.ts

5. **Step 5: Add JIT user provisioning** - Add get_or_create_user helper in backend routes.py

## Files Modified

- `intellistack/auth-server/.env` - Added CORS_ORIGINS
- `intellistack/auth-server/package.json` - Fixed dev script
- `intellistack/auth-server/src/index.ts` - JWKS proxy (already done)
- `intellistack/auth-server/src/auth.ts` - Removed crv (already done)
- `intellistack/backend/.env` - Already had correct CORS (verified)
- `intellistack/backend/src/core/users/routes.py` - Added JIT provisioning

## Response snapshot

Implemented all 5 steps of the signup flow fix:

1. **Step 2** - Fixed dev script in package.json (was already using dotenv in code)
2. **Step 1** - Added CORS_ORIGINS to auth-server .env
3. **Step 3** - JWKS endpoint already had proxy implementation
4. **Step 4** - JWT algorithm already fixed (crv removed)
5. **Step 5** - Added JIT user provisioning with `get_or_create_user()` helper in routes.py, applied to all endpoints (/me, /onboarding, /preferences, /stage)

## Outcome

- ✅ Impact: Fixed signup flow by addressing CORS, JWKS, JWT algorithm, and JIT user provisioning
- 🧪 Tests: None added (verification plan provided in original plan)
- 📁 Files: 4 modified (auth .env, package.json, routes.py), backend .env already correct
- 🔁 Next prompts: Run migrations and verify end-to-end flow
- 🧠 Reflection: Many items were already partially fixed from previous work. The main new change was adding JIT user provisioning to the backend.

## Evaluation notes (flywheel)

- Failure modes observed: None yet - requires verification
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Verify with curl/Postman that JWKS returns keys after better-auth migrate
