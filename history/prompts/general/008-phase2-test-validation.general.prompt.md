---
id: 008
title: Phase 2 — Test Validation Suite for Security Fixes
stage: green
date: 2026-03-17
surface: agent
model: claude-sonnet-4-6
feature: 001-intellistack-platform
branch: 001-intellistack-platform
user: Akhtar
command: "and now move to the next phase2 of implementing of the plan"
labels: ["phase2","testing","security","auth","jwks","cors","regression"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - tests/unit/auth/test_jwks_singleton.py
  - tests/unit/auth/test_middleware_algorithm.py
  - tests/unit/config/test_settings_cors.py
  - tests/unit/test_auth.py
  - tests/unit/test_routing.py
  - tests/integration/test_learning_auth.py
  - src/shared/middleware.py
  - src/core/auth/dependencies.py
  - project_docs/03_sequence/PHASE_SEQUENCE.md
tests:
  - tests/unit/auth/test_jwks_singleton.py (5 tests — singleton identity, settings-once, shared cache state)
  - tests/unit/auth/test_middleware_algorithm.py (6 tests — RS256/HS256/none rejected, EdDSA passes, WWW-Authenticate header)
  - tests/unit/config/test_settings_cors.py (9 tests — production guard, CSV/JSON parsing, whitespace stripping)
  - tests/unit/test_auth.py (12 tests — middleware loaded, 401 enforcement, Phase 2 EdDSA/missing-token unit tests)
  - tests/unit/test_routing.py (14 tests — health, routes, auth regression guards, tutor prefix regression)
  - tests/integration/test_learning_auth.py (22 tests — all 8 learning endpoints, mocked auth, tutor prefix)
---

## Prompt

"and now move to the next phase2 of implementing of the plan"

(Continued from a session that completed Phase 1 security hardening. Phase 2 is writing the comprehensive test suite to validate every Phase 1 fix.)

## Response snapshot

Implemented 67 tests across 6 test files covering all Phase 2 tasks:

**Unit tests (45 passing):**
- `test_jwks_singleton.py` — 5 tests for JWKS singleton pattern; same instance returned on every call, settings read once, middleware/dependency share cache state
- `test_middleware_algorithm.py` — 6 tests; RS256/HS256/none algorithm tokens rejected with 401 + `INVALID_TOKEN_ALGORITHM` error code; EdDSA tokens pass the algorithm gate; WWW-Authenticate header present
- `test_settings_cors.py` — 9 tests; production startup blocks with dev-only CORS origins; real origins accepted; dev/staging permit localhost defaults; CSV, JSON-array, and whitespace formats parsed correctly
- `test_auth.py` + `test_routing.py` — 25 tests including Phase 2 additions: `test_dependency_rejects_non_eddsa_key` and `test_dependency_rejects_missing_token`

**Integration tests (22 passing):**
- All 8 auth-protected learning endpoints return 401 without token
- All 8 endpoints return 401/503 with garbage token
- No learning endpoint returns 5xx without auth
- Public `/api/v1/learning/stages` list returns 200 (not 401)
- `app.dependency_overrides` pattern used for mocked-auth tests (not module.patch, which cannot override already-captured Depends() references)
- Tutor router regression: `/api/v1/ai/tutor/health` reachable; old `/ai/tutor/...` returns 404

**Two Phase 1 bugs found and fixed during Phase 2 testing:**

1. **Middleware algorithm check was inside `if key_data:` block** — when JWKS returned empty keys, non-EdDSA tokens passed through silently. Fixed by moving the algorithm check before the JWKS fetch. This is the correct security design: reject unsupported algorithms at the perimeter, before any network call.

2. **`dependencies.py` broad `except Exception` swallowed `HTTPException`** — the EdDSA key check raised `HTTPException(401)` but it was caught by the outer `except Exception` handler and re-raised as 500. Fixed by adding `except HTTPException: raise` before the broad handler.

**Test infrastructure patterns established:**
- All fixtures use lazy imports (`from src.main import create_app` inside function body) to avoid module-level Settings validation errors
- All fixtures that create the app depend on `setup_test_settings` (session-scoped)
- Patch targets always use the source module (`src.config.settings.get_settings`), not the importing module
- `app.dependency_overrides` (not `unittest.mock.patch`) for FastAPI dependency mocking in integration tests

## Outcome

- ✅ Impact: All 7 Phase 2 test tasks complete; 67/67 tests passing; two additional Phase 1 defects discovered and fixed
- 🧪 Tests: 67 new/modified tests — 45 unit, 22 integration — all green
- 📁 Files: 6 test files created/updated, 2 source files patched (middleware.py, dependencies.py), PHASE_SEQUENCE.md updated
- 🔁 Next prompts: Phase 3 — Architecture Consolidation (remove duplicate JWT decode path, standardise error shapes, correlation IDs, rate limiting, router registry)
- 🧠 Reflection: FastAPI's dependency resolution captures function references at Depends() definition time — `unittest.mock.patch` cannot override these after the fact; `app.dependency_overrides` is the correct mechanism. Also, lazy imports inside fixture functions are essential to prevent premature Settings validation during pytest collection.

## Evaluation notes (flywheel)

- Failure modes observed: (1) `AttributeError: module does not have attribute 'get_settings'` — lazy imports inside functions cannot be patched at the importing module; (2) `HTTPException` swallowed by broad `except Exception` — always add `except HTTPException: raise` guard; (3) module-scoped test fixtures need `setup_test_settings` just like function-scoped ones
- Graders run and results (PASS/FAIL): pytest 67/67 PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Phase 3.1 — consolidate duplicate JWT decode logic from dependency fallback path into a shared helper
