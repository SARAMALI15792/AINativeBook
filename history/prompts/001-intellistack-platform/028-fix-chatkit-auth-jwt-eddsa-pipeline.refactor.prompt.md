---
id: 028
title: Fix ChatKit Auth JWT EdDSA Pipeline
stage: refactor
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: user-prompt
labels: ["auth", "jwt", "eddsa", "chatkit", "better-auth", "bugfix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/lib/auth-client.ts
  - intellistack/content/src/components/ai/ChatKitWidget.tsx
  - intellistack/content/src/pages/profile.tsx
  - intellistack/backend/src/core/auth/dependencies.py
  - intellistack/backend/src/ai/chatkit/routes.py
  - intellistack/auth-server/src/auth.ts
tests:
  - E2E curl test: login -> JWT -> GET /threads -> POST /stream (all PASS)
  - Docusaurus build (PASS, exit code 0)
---

## Prompt

User reported ChatKit widget always shows "Sign in to continue" even after logging in. Asked to check and fix the login issue and verify the RAG pipeline integration.

## Response snapshot

Diagnosed 5 interconnected bugs in the auth pipeline:

1. **Session token vs JWT mismatch**: ChatKitWidget sent `session.session.token` (a plain session ID string) as Bearer token, but the backend expected a JWT. Fixed by adding `jwtClient` plugin to auth-client and using `getJwtToken()` to fetch real JWTs from `/api/auth/token`.

2. **Algorithm mismatch (RS256 vs EdDSA)**: Backend `dependencies.py` hardcoded `algorithms=["RS256"]` but Better-Auth defaults to EdDSA (Ed25519). Fixed by using `PyJWK.from_dict()` to auto-detect the algorithm from the JWKS key data.

3. **Missing JWT client plugin**: Auth-client didn't include the `jwtClient` plugin needed to call `authClient.token()`. Added `jwtClient()` to the plugins array.

4. **Database schema mismatches**: ChatKit tables had UUID columns for `user_id` and `id`, but Better-Auth generates text string IDs. Also missing `lesson_stage`, `status`, and `enrollment_ended_at` columns. Recreated tables with VARCHAR types.

5. **DB query crash on non-UUID user IDs**: The `build_context` function queried Progress/User tables with Better-Auth string IDs, causing asyncpg DataError. Added try/except with rollback and default fallback.

Additional fixes:
- Fixed `list_threads` endpoint creating a broken fake Request object
- Updated auth-server JWT plugin config to correctly declare EdDSA (was misleadingly declaring RS256)
- Fixed `profile.tsx` to use JWT for backend API calls

## Outcome

- ✅ Impact: ChatKit auth pipeline fully working — login, JWT exchange, backend validation, thread CRUD, and streaming all pass E2E tests
- 🧪 Tests: E2E curl tests pass; Docusaurus build succeeds
- 📁 Files: 6 files modified across auth-client, ChatKitWidget, backend auth, chatkit routes, auth-server config
- 🔁 Next prompts: Add real OpenAI API key for AI responses; sync Better-Auth user records with backend users table
- 🧠 Reflection: Better-Auth's default is EdDSA, not RS256 — the JWT plugin config was misleading. Session tokens are NOT JWTs; the `/api/auth/token` endpoint must be used to get JWTs for API calls.

## Evaluation notes (flywheel)

- Failure modes observed: Algorithm mismatch between config and runtime; session token vs JWT confusion; UUID vs text type mismatch between Better-Auth and backend schema
- Graders run and results (PASS/FAIL): E2E curl test PASS, Docusaurus build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider syncing Better-Auth user IDs to backend users table on first login
