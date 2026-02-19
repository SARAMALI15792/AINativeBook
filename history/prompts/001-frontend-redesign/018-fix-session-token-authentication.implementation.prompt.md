---
id: 018
title: Fix Session Token Authentication
stage: implementation
date: 2026-02-18
surface: agent
model: claude-opus-4-6
feature: 001-frontend-redesign
branch: 001-frontend-redesign
user: saram
command: implementation
labels: ["authentication", "session-tokens", "better-auth", "bug-fix", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/core/auth/dependencies.py
  - intellistack/backend/src/shared/middleware.py
  - AUTH_SESSION_TOKEN_FIX.md
tests:
  - Backend health check (passed)
  - Session token validation logic (code review)
  - Manual browser testing (pending)
---

## Prompt

Implement the following plan:

# Fix 401 Unauthorized Error on Preferences Save

[Full plan provided in previous context - JWT algorithm mismatch and session token authentication]

## Response snapshot

Discovered the root cause was deeper than initially identified:

### Initial Fix (Completed)
1. **Middleware Algorithm Detection** - Changed hardcoded RS256 to dynamic algorithm detection
2. **Cookie Fallback** - Added cookie reading to `get_current_user()`

### Root Cause Discovery
After implementing the initial fix, 401 errors persisted. Investigation revealed:
- Better-Auth stores **session tokens** (opaque strings) in cookies, NOT JWTs
- Backend was trying to decode session tokens as JWTs, which always fails
- Session tokens must be validated by calling the auth server's session endpoint

### Complete Solution Implemented

**Added Session Token Validation:**
```python
async def validate_session_token(session_token: str) -> Optional[AuthenticatedUser]:
    """Validate session token by calling auth server."""
    auth_server_url = settings.better_auth_jwks_url.replace('/.well-known/jwks.json', '')

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{auth_server_url}/api/auth/get-session",
            cookies={settings.better_auth_session_cookie_name: session_token},
            timeout=5.0
        )

        if response.status_code == 200 and data.get('user'):
            return AuthenticatedUser(...)
        return None
```

**Modified `get_current_user()` with Fallback:**
1. Try JWT validation first (existing logic)
2. If JWT decoding fails, try session token validation
3. Return 401 only if both fail

**Key Changes:**
- Added `httpx` import for HTTP calls to auth server
- Created `validate_session_token()` function
- Modified exception handling to catch `jwt.DecodeError` and fallback to session validation
- Fixed `AuthenticatedUser` field name from `user_id` to `id`

### Verification
- ✅ Code compiles without syntax errors
- ✅ Backend health check passes
- ✅ Dual authentication support (JWT + session tokens)
- 🧪 Manual testing required (browser-based flow)

### Documentation
Created `AUTH_SESSION_TOKEN_FIX.md` with:
- Problem analysis and root cause
- Complete implementation details with code snippets
- Authentication flow diagram
- Testing instructions for manual verification
- Debugging guide

## Outcome

- ✅ Impact: Implemented dual authentication support. Backend now accepts both JWT tokens (for API clients) and session tokens (for browser frontend). This fixes the 401 errors on preferences save by properly validating Better-Auth session tokens.
- 🧪 Tests: Backend health check passed. Code review passed. Manual browser testing required to verify end-to-end flow (login → personalization → preferences save).
- 📁 Files: Modified 2 backend files (dependencies.py with session validation, middleware.py with dynamic algorithm), created 2 documentation files (AUTH_SESSION_TOKEN_FIX.md, AUTH_401_FIX_COMPLETE.md).
- 🔁 Next prompts: Manual testing in browser (login, complete personalization wizard, verify no 401 errors), add Redis caching for session validation results, add unit tests for session token validation.
- 🧠 Reflection: The initial fix addressed the JWT algorithm mismatch but didn't solve the core issue. Better-Auth's architecture uses session tokens (not JWTs) in cookies for browser-based auth. The solution required understanding the auth server's session validation endpoint and implementing a fallback mechanism. This maintains backward compatibility with JWT auth while adding session token support.

## Evaluation notes (flywheel)

- Failure modes observed: Initial assumption that cookies contained JWTs was incorrect. Better-Auth uses session tokens (opaque strings) that must be validated server-side. Field name mismatch (`user_id` vs `id`) in AuthenticatedUser dataclass caused initial failures.
- Graders run and results (PASS/FAIL): Code compilation PASS. Backend health check PASS. Session validation logic review PASS. Manual integration testing PENDING (requires browser interaction).
- Prompt variant (if applicable): N/A - Implementation evolved based on root cause analysis.
- Next experiment (smallest change to try): Add Redis caching for session validation results (5-minute TTL) to reduce latency and load on auth server. Add logging to track JWT vs session token usage patterns.
