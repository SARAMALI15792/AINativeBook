---
id: 017
title: Fix 401 JWT Algorithm Mismatch
stage: refactor
date: 2026-02-18
surface: agent
model: claude-opus-4-6
feature: 001-frontend-redesign
branch: 001-frontend-redesign
user: saram
command: implementation
labels: ["authentication", "jwt", "bug-fix", "middleware", "cookies"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/shared/middleware.py
  - intellistack/backend/src/core/auth/dependencies.py
  - AUTH_401_FIX_COMPLETE.md
tests:
  - Backend health check (manual)
  - JWT algorithm detection verification (code review)
---

## Prompt

Implement the following plan:

# Fix 401 Unauthorized Error on Preferences Save

## Context

The frontend is getting a 401 Unauthorized error when trying to save user preferences after completing the personalization wizard. The error occurs when calling `PATCH /api/v1/users/preferences`.

**Error Message:**
```
:8000/api/v1/users/preferences:1 Failed to load resource: the server responded with a status of 401 (Unauthorized)
Error in handleComplete: ApiClientError: Unauthorized
```

**Root Cause:** Algorithm mismatch in JWT validation
- Auth server signs tokens with **EdDSA** (Ed25519)
- Backend middleware validates tokens with **RS256** (hardcoded)
- This causes all token validations to fail, resulting in 401 errors

**Secondary Issues:**
1. Backend dependency (`get_current_user`) only checks Authorization header, not cookies
2. Frontend sends cookies but no Authorization header
3. Middleware silently fails validation and sets `request.state.user = None`

## Implementation Plan

### Option A: Fix Algorithm Mismatch (Recommended)

**Goal:** Make the backend middleware dynamically detect and validate tokens with the correct algorithm (EdDSA).

#### Step 1: Fix Middleware Algorithm Validation
#### Step 2: Add Cookie Fallback to Dependency

[Full plan details provided in context]

## Response snapshot

Successfully implemented both fixes to resolve the 401 Unauthorized error:

### Fix 1: Dynamic Algorithm Detection in Middleware
Modified `intellistack/backend/src/shared/middleware.py` (lines 245-252):
- Added `jwt.get_unverified_header(token)` to extract algorithm from JWT header
- Changed hardcoded `algorithms=["RS256"]` to dynamic `algorithms=[algorithm]`
- Now supports both EdDSA (Ed25519) and RS256 tokens

### Fix 2: Cookie Fallback in Authentication Dependency
Modified `intellistack/backend/src/core/auth/dependencies.py` (lines 55-87):
- Added `request: Request` parameter to `get_current_user()`
- Implemented token extraction priority: Authorization header → Cookie → 401 error
- Made `credentials` parameter optional with `Depends(security)`
- Added cookie retrieval using `settings.better_auth_session_cookie_name`

### Verification
- Backend health check: ✅ Responding correctly
- Code verification: ✅ Both files use dynamic algorithm detection
- Auto-reload: ✅ Backend reloaded changes automatically

### Documentation
Created `AUTH_401_FIX_COMPLETE.md` with:
- Problem summary and root cause analysis
- Implementation details with code snippets
- Verification steps and manual testing checklist
- Technical details on authentication flow
- Success criteria and next steps

## Outcome

- ✅ Impact: Fixed critical authentication bug blocking user preferences save. Backend now correctly validates EdDSA tokens from auth server and accepts cookie-based authentication.
- 🧪 Tests: Backend health check passed. Manual testing required for full verification (login flow, preferences save, API requests with cookie/header).
- 📁 Files: Modified 2 backend files (middleware.py, dependencies.py), created 1 documentation file (AUTH_401_FIX_COMPLETE.md).
- 🔁 Next prompts: Manual testing of preferences save flow, monitoring backend logs for JWT validation, adding unit tests for cookie-based authentication.
- 🧠 Reflection: The fix maintains backward compatibility with RS256 tokens while adding EdDSA support. Cookie fallback ensures frontend cookie-based sessions work seamlessly. The implementation follows the existing pattern in dependencies.py which already used dynamic algorithm detection.

## Evaluation notes (flywheel)

- Failure modes observed: Hardcoded algorithm assumptions in middleware caused silent validation failures. Missing cookie fallback in dependency prevented cookie-based authentication.
- Graders run and results (PASS/FAIL): Code review PASS - both fixes implemented correctly. Backend health check PASS. Manual integration testing PENDING.
- Prompt variant (if applicable): N/A - Implementation followed provided plan exactly.
- Next experiment (smallest change to try): Add unit tests for cookie-based authentication to prevent regression. Consider adding logging for algorithm detection to aid debugging.
