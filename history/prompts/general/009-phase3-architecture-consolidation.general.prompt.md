---
id: 009
title: Phase 3 — Architecture Consolidation
stage: refactor
date: 2026-03-17
surface: agent
model: claude-sonnet-4-6
feature: 001-intellistack-platform
branch: 001-intellistack-platform
user: Akhtar
command: "ok now move towards the next phase 3 implementation"
labels: ["phase3","refactor","jwt","error-handling","correlation-id","rate-limiting","router-registry"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/core/auth/jwt_utils.py (NEW)
  - src/core/routes_registry.py (NEW)
  - src/shared/middleware.py
  - src/core/auth/dependencies.py
  - src/main.py
  - src/ai/rag/routes.py
  - src/ai/tutor/routes.py
  - project_docs/03_sequence/PHASE_SEQUENCE.md
tests:
  - All 67 Phase 2 tests re-run and passing after Phase 3 changes
---

## Prompt

"ok now move towards the next phase 3 implementation"

## Response snapshot

Implemented all 5 Phase 3 architecture consolidation tasks:

**3.1 — Shared JWT decode helper (`src/core/auth/jwt_utils.py`)**
Created `decode_bearer_jwt(token, jwks_manager, settings) -> Optional[dict]` as the single source of truth for EdDSA JWT validation. Both the middleware and dependency layer now call this helper instead of each implementing their own decode path. The helper enforces: (1) algorithm check before any network call, (2) key lookup by kid, (3) EdDSA assertion on the JWKS-returned key, (4) PyJWT signature verification. Returns `None` for non-JWT tokens (no parseable header / no kid) to support session-token fallbacks. Raises `HTTPException(401)` for all intentional rejections.

Middleware refactored: keeps its early algorithm check (returns `JSONResponse` with specific `INVALID_TOKEN_ALGORITHM` code for test compatibility), then delegates full validation to `decode_bearer_jwt`. Session-token fallback path preserved intact.

Dependency layer refactored: entire inline JWT decode block (≈60 lines) replaced with a single `await decode_bearer_jwt(...)` call. Removed unused `jwt`, `PyJWK`, `PyJWTError` imports.

**3.2 — Standardised error response shapes (`src/main.py`)**
Added a global `HTTPException` handler that converts all responses to the canonical `{"error": {"code": "<CODE>", "message": "..."}}` envelope. Previously, plain `raise HTTPException(status_code=404, detail="Not found")` would produce `{"detail": "Not found"}` — inconsistent with the `IntelliStackError` shape used by domain exceptions. The new handler inspects the `detail` field:
- Already a dict with `"error"` key → passed through unchanged (prevents double-wrapping `IntelliStackError` responses)
- Plain string → wrapped with a code derived from a `_STATUS_CODE_MAP` (e.g. 401 → `UNAUTHORIZED`, 404 → `NOT_FOUND`)
- Other → stringified and wrapped

Added `HTTPException` to the FastAPI import in `main.py`.

**3.3 — Correlation IDs (`src/shared/middleware.py` + `src/main.py`)**
Added `CorrelationIDMiddleware(BaseHTTPMiddleware)`:
- Reads `X-Request-ID` from incoming request headers; generates `uuid.uuid4()` if absent
- Stores as `request.state.correlation_id` for downstream access
- Injects `X-Request-ID` into every response
- Registered as the outermost middleware (first `add_middleware` call) so it wraps all others
Updated `RequestLoggingMiddleware` to include `correlation_id` in the structured log entry.

**3.4 — User-scoped rate limiting (`src/shared/middleware.py`, AI routes)**
Added `UserScopedRateLimiter(requests, window, prefix)`:
- Keys by authenticated user ID (`request.state.user_id`) when present, falls back to client IP for anonymous requests
- Uses the same Redis sliding-window pattern as existing `RateLimiter` but per-user instead of per-IP+UA
- Raises `HTTPException(429)` when the per-user limit is exceeded

Pre-configured instances:
- `ai_chat_rate_limit = UserScopedRateLimiter(20, 60, "ai_chat_rl")` — 20 req/min/user
- `tutor_rate_limit = UserScopedRateLimiter(15, 60, "tutor_rl")` — 15 req/min/user

Wired as `Depends()` on compute-heavy endpoints:
- RAG: `POST /api/v1/ai/rag/query`, `POST /api/v1/ai/rag/query/stream`
- Tutor: `POST /api/v1/ai/tutor/conversations/{id}/messages`, `POST /api/v1/ai/tutor/debugging-help`, `POST /api/v1/ai/tutor/code-review`

**3.5 — Router registry (`src/core/routes_registry.py`)**
Created `RouterConfig` dataclass and `register_all_routers(app)` function. All 12 routers and their mount prefixes are declared in one place (Tier A: bare-path routers that main.py prefixes with `/api/v1`; Tier B: full-path routers with empty prefix). `main.py` now calls `register_all_routers(app)` instead of 12 separate `include_router` calls. All router imports moved out of `main.py` into the registry module.

## Outcome

- ✅ Impact: JWT decode is DRY (single helper); all HTTP errors use standard envelope; every request/response carries X-Request-ID; AI endpoints have per-user rate limits; all routers registered from one registry
- 🧪 Tests: 67/67 Phase 2 tests still pass — zero regressions from Phase 3 refactoring
- 📁 Files: 2 new source files, 5 modified source files, PHASE_SEQUENCE.md updated
- 🔁 Next prompts: Phase 4 — Production Hardening (security scan, load test, connection pool tuning, observability, final docs)
- 🧠 Reflection: The middleware algorithm check must remain inline (returning JSONResponse directly) rather than going through decode_bearer_jwt, because the specific INVALID_TOKEN_ALGORITHM error code in the response body is asserted by Phase 2 tests. The global HTTPException handler would map it to a generic UNAUTHORIZED code. Design lesson: when middleware needs a specific structured error body, inline the early-exit rather than delegating to a helper that raises a generic exception.

## Evaluation notes (flywheel)

- Failure modes observed: None — all 67 tests passed on first run after Phase 3 changes
- Graders run and results (PASS/FAIL): pytest 67/67 PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Phase 4.1 — run bandit security scan on src/ and address any HIGH-severity findings
