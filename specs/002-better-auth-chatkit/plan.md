# Implementation Plan: Better-Auth OIDC Server + ChatKit AI Tutor

**Branch**: `002-better-auth-chatkit` | **Date**: 2026-02-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-better-auth-chatkit/spec.md`

## Summary

Implement a standalone Better-Auth OIDC server (Node.js) with RS256/JWKS token signing, OAuth social login (Google/GitHub), and email verification, replacing the current custom Python auth system. Integrate OpenAI ChatKit (React frontend + Python server) into the existing FastAPI backend for a persistent AI tutor with Socratic teaching, context injection, stage-based RAG, and rate limiting. Migrate all existing user data via a one-time big-bang cutover script.

## Technical Context

**Language/Version**: TypeScript 5.3+ (auth server, frontend), Python 3.11+ (FastAPI backend, ChatKit server)
**Primary Dependencies**: Better-Auth (Node.js OIDC), @openai/chatkit-react (frontend), chatkit Python SDK (backend), FastAPI, SQLAlchemy 2.0 async
**Storage**: PostgreSQL (Neon) — shared by auth server and FastAPI backend
**Testing**: Vitest (auth server), pytest + pytest-asyncio (backend), Playwright (E2E)
**Target Platform**: Web (Docker containers: auth-server, backend, frontend)
**Project Type**: Web application (3 services: auth server, API backend, frontend)
**Performance Goals**: <2s AI response start (SC-005), <1s thread history load (SC-006), <10s OAuth login (SC-002), 500 concurrent users (SC-007)
**Constraints**: 20 msg/day student rate limit (FR-027), 6h access token / 7d refresh token (FR-011), RS256 signing only
**Scale/Scope**: 500 concurrent users, ~7 new database tables, 3 API contracts, 1 data migration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution template is not yet filled in for this project. Proceeding with standard SDD principles:

- [x] **Smallest viable change**: Each phase delivers independently testable functionality
- [x] **No invented APIs**: All contracts derived from spec FRs and ChatKit/Better-Auth official SDKs
- [x] **No hardcoded secrets**: All credentials via `.env` files
- [x] **Test coverage**: Each phase includes acceptance test criteria
- [x] **Security**: RS256 signing, PKCE, bcrypt passwords, HTTP-only cookies, rate limiting

## Project Structure

### Documentation (this feature)

```text
specs/002-better-auth-chatkit/
├── plan.md              # This file
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── auth-server-api.md
│   ├── chatkit-api.md
│   └── fastapi-auth-middleware.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
intellistack/
├── auth-server/                    # NEW: Better-Auth Node.js OIDC server
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── src/
│   │   ├── index.ts               # Express server entry point
│   │   ├── auth.ts                # Better-Auth config (OIDC, JWT, admin, social)
│   │   ├── db.ts                  # Drizzle adapter for PostgreSQL
│   │   ├── email.ts               # Resend/SMTP email handler
│   │   └── hooks.ts               # Auth event logging hooks (FR-028)
│   └── migrations/
│       └── migrate-data.ts        # Data migration script (FR-025)
│
├── backend/                        # EXISTING: FastAPI backend (modified)
│   ├── src/
│   │   ├── main.py                # Mount ChatKit endpoint, update auth middleware
│   │   ├── shared/
│   │   │   ├── middleware.py      # REPLACE: JWKS-based JWT validation
│   │   │   └── database.py       # Add ChatKit tables
│   │   ├── core/auth/
│   │   │   ├── jwks.py            # NEW: JWKS fetcher + cache manager
│   │   │   ├── dependencies.py    # NEW: get_current_user, require_role, require_verified
│   │   │   ├── models.py          # UPDATE: remove old auth models, add auth_event_log
│   │   │   └── (remove v1/v2 routes, service, adapter, better_auth_config)
│   │   ├── ai/chatkit/            # NEW: ChatKit integration
│   │   │   ├── __init__.py
│   │   │   ├── server.py          # IntelliStackChatKitServer (extends ChatKitServer)
│   │   │   ├── store.py           # PostgresChatKitStore (thread/item persistence)
│   │   │   ├── context.py         # RequestContext with user + page context
│   │   │   ├── rate_limiter.py    # 20 msg/day student rate limiter
│   │   │   ├── agent.py           # AI tutor agent (Socratic, RAG-augmented)
│   │   │   ├── models.py          # SQLAlchemy models: chatkit_thread, chatkit_thread_item, etc.
│   │   │   └── routes.py          # /api/v1/chatkit POST endpoint
│   │   └── ai/tutor/             # EXISTING: keep guardrails, modify agent integration
│   └── requirements.txt           # Add: chatkit, PyJWT, jwcrypto
│
├── frontend/                       # EXISTING: Next.js (modified)
│   ├── src/
│   │   ├── lib/
│   │   │   └── auth-client.ts     # REPLACE: use createAuthClient from better-auth/react
│   │   ├── middleware.ts          # UPDATE: use Better-Auth session cookie name
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx       # REFACTOR: use Better-Auth signIn
│   │   │   │   ├── register/page.tsx    # REFACTOR: use Better-Auth signUp
│   │   │   │   ├── forgot-password/     # REFACTOR: use Better-Auth forgetPassword
│   │   │   │   └── reset-password/      # REFACTOR: use Better-Auth resetPassword
│   │   │   └── (dashboard)/
│   │   │       └── learn/[stageId]/[contentId]/
│   │   │           └── page.tsx         # ADD: ChatKit widget integration
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── AuthProvider.tsx      # REPLACE: use Better-Auth session provider
│   │   │   │   └── AuthGuard.tsx        # UPDATE: use useSession from Better-Auth
│   │   │   └── ai/
│   │   │       ├── ChatKitWidget.tsx     # NEW: ChatKit <ChatKit /> wrapper
│   │   │       ├── TextSelectionAsk.tsx  # NEW: text selection → chat query
│   │   │       └── ThreadList.tsx        # NEW: conversation thread sidebar
│   │   └── hooks/
│   │       └── useAuth.ts              # REPLACE: use Better-Auth hooks
│   └── package.json               # Add: @openai/chatkit-react
```

**Structure Decision**: Web application with 3 services. The auth server is a new standalone Node.js service. The ChatKit server is integrated into the existing FastAPI process (not separate). The frontend remains a single Next.js app.

---

## Implementation Phases

### Phase 1: Better-Auth OIDC Server Setup
> **Goal**: Standalone auth server running with OIDC discovery, JWKS, email/password auth.
> **Depends on**: Nothing (greenfield)
> **Delivers**: FR-001, FR-004, FR-005, FR-010

**Steps**:
1. Scaffold `intellistack/auth-server/` with `package.json`, `tsconfig.json`, Express entry point
2. Configure Better-Auth with:
   - Drizzle adapter pointing to Neon PostgreSQL
   - JWT plugin with RS256 signing and `/.well-known/jwks.json`
   - OIDC Provider plugin with discovery endpoint
   - Email/password enabled with password strength validation (12+ chars, mixed case, number, special)
3. Create Dockerfile for the auth server
4. Add to `docker-compose.yml` as a new service
5. Run `npx better-auth migrate` to create auth tables in the database
6. Verify: OIDC discovery responds, JWKS returns valid RSA keys, registration creates user with hashed password

**Acceptance**:
- `GET /.well-known/openid-configuration` returns valid OIDC discovery document
- `GET /.well-known/jwks.json` returns at least one RS256 public key
- `POST /api/auth/sign-up/email` creates user and returns session

---

### Phase 2: Social Login + Email Verification + Account Security
> **Goal**: Complete authentication feature set: OAuth, email verification, lockout, password reset.
> **Depends on**: Phase 1
> **Delivers**: FR-002, FR-003, FR-006, FR-007, FR-008, FR-009, FR-026

**Steps**:
1. Configure Google and GitHub social providers in Better-Auth config
2. Enable PKCE for all public client flows (FR-006)
3. Configure email verification:
   - Set up Resend API (or SMTP fallback) email handler
   - Verification email template with token link
   - Unverified users: limited access (browse dashboard/courses, no lessons or AI tutor)
4. Configure account lockout: 5 failed attempts → 30-minute cooldown (FR-007)
5. Configure password reset flow: token email → 1-hour expiry → reset page (FR-008)
6. Configure Admin plugin with roles: student (default), instructor, admin (FR-009)
7. Implement auth event logging hooks for all auth events (FR-028)

**Acceptance**:
- OAuth flow for Google and GitHub completes end-to-end
- Unverified email users cannot access lesson content (403)
- 5 failed logins locks account, 6th attempt shows lockout message
- Password reset email sent with valid token, reset completes successfully
- `auth_event_log` table populated for all auth events

---

### Phase 3: FastAPI JWKS Integration + Auth Middleware Replacement
> **Goal**: FastAPI validates Better-Auth JWTs using JWKS, replacing the current cookie-based auth.
> **Depends on**: Phase 1 (JWKS endpoint must exist)
> **Delivers**: FR-004, FR-005, FR-011, FR-022

**Steps**:
1. Create `core/auth/jwks.py`: JWKS manager with 5-min cache, fallback to last-known-good keys, 503 on total failure
2. Create `core/auth/dependencies.py`:
   - `get_current_user`: extract Bearer token → verify RS256 via JWKS → return AuthenticatedUser
   - `require_role(*roles)`: check user.role against allowed roles
   - `require_verified_email`: check user.email_verified claim
3. Update `shared/middleware.py`: remove `BetterAuthSessionMiddleware`, add JWKS-based auth
4. Update all existing route dependencies to use new `get_current_user` instead of old auth
5. Remove old auth code: `routes.py`, `routes_v2.py`, `service.py`, `service_v2.py`, `adapter.py`, `better_auth_config.py`
6. Update `requirements.txt`: add `PyJWT`, `jwcrypto`; remove `python-jose`
7. Add `BETTER_AUTH_URL` and `BETTER_AUTH_JWKS_URL` to settings.py

**Acceptance**:
- FastAPI rejects requests without valid Bearer token (401)
- FastAPI rejects requests with expired tokens (401)
- FastAPI correctly extracts role from JWT claims
- JWKS cache works: second request doesn't fetch from auth server
- Fallback keys work: temporarily stopping auth server doesn't break existing sessions

---

### Phase 4: Data Migration
> **Goal**: Migrate all existing users, sessions, OAuth links to Better-Auth schema.
> **Depends on**: Phase 1 (Better-Auth tables must exist), Phase 3 (new auth middleware ready)
> **Delivers**: FR-025

**Steps**:
1. Create `auth-server/migrations/migrate-data.ts`:
   - Read existing users → insert into Better-Auth `user` table (preserve UUIDs)
   - Move password hashes → `account` table with `provider_id='credential'`
   - Move OAuth accounts → `account` table with provider mapping
   - Move active sessions → `session` table (drop expired)
   - Move historical login attempts → `auth_event_log` (new table)
   - Flatten user_role → user.role field
2. Create pre-migration backup script
3. Create validation script: for each migrated user, verify they can authenticate
4. Create rollback script: restore from backup if migration fails
5. Run on staging database first, then production

**Acceptance**:
- SC-008: Zero user data lost during migration
- All existing users can log in with their current passwords
- All OAuth-linked accounts still work
- Role assignments preserved

---

### Phase 5: Frontend Auth Refactor
> **Goal**: Replace custom auth client with official Better-Auth React client.
> **Depends on**: Phase 1 (auth server running), Phase 3 (backend validates new tokens)
> **Delivers**: FR-012, FR-013, FR-023

**Steps**:
1. Replace `lib/auth-client.ts`: use `createAuthClient` from `better-auth/react` with admin client plugin
2. Update `hooks/useAuth.ts`: use `authClient.useSession()`, `signIn.email()`, `signUp.email()`, `signIn.social()`, `signOut()`
3. Update `components/auth/AuthProvider.tsx`: proper session provider wrapping
4. Update `components/auth/AuthGuard.tsx`: use `useSession()` from Better-Auth
5. Refactor auth pages:
   - `login/page.tsx`: use `signIn.email()` and `signIn.social('google'|'github')`
   - `register/page.tsx`: use `signUp.email()`, keep PasswordStrengthMeter
   - `forgot-password/page.tsx`: use `authClient.forgetPassword()`
   - `reset-password/page.tsx`: use `authClient.resetPassword()`
6. Fix `middleware.ts`: use correct Better-Auth session cookie name (`better-auth.session_token`)
7. Implement silent token refresh (FR-012): Better-Auth client handles this automatically
8. Implement sign-out (FR-013): `signOut()` clears client session
9. Remove deleted `userStore.ts` references
10. Remove unused packages: `@daveyplate/better-auth-ui`

**Acceptance**:
- All auth pages work with Better-Auth client
- Session persists across browser refresh (SC-003)
- Token auto-refreshes without user interaction
- OAuth login completes in <10s (SC-002)
- Signing out redirects to landing page

---

### Phase 6: ChatKit Backend (Server + Store + Agent)
> **Goal**: ChatKit Python server integrated into FastAPI with persistent threads and RAG-augmented Socratic tutor.
> **Depends on**: Phase 3 (auth middleware for JWT validation)
> **Delivers**: FR-018, FR-019, FR-020, FR-021, FR-024, FR-027

**Steps**:
1. Create SQLAlchemy models in `ai/chatkit/models.py`: `chatkit_thread`, `chatkit_thread_item`, `chatkit_rate_limit`, `ai_usage_metric`
2. Create Alembic migration for new ChatKit tables
3. Implement `ai/chatkit/store.py`: `PostgresChatKitStore` extending ChatKit's `Store` base class
   - `create_thread()`, `load_thread()`, `load_thread_items()`, `save_thread_item()`, `delete_thread()`
   - Include course_id, lesson_stage, user_id in thread metadata
4. Implement `ai/chatkit/context.py`: `RequestContext` dataclass with user identity, page context, role, stage
5. Implement `ai/chatkit/rate_limiter.py`: check/increment message count per user per 24h rolling window; exempt instructors/admins
6. Implement `ai/chatkit/agent.py`: Socratic tutor agent using OpenAI Agents SDK
   - System instructions: Socratic teaching method, guiding questions before answers
   - RAG tool: search Qdrant with stage-based access control (only unlocked stages)
   - Use existing `ai/rag/retrieval.py` HybridRetriever for content search
   - Use existing `ai/tutor/guardrails.py` for Socratic guardrails
7. Implement `ai/chatkit/server.py`: `IntelliStackChatKitServer` extending `ChatKitServer`
   - `respond()`: authenticate → check rate limit → extract context → run agent → stream response
   - Track usage metrics (FR-029)
8. Implement `ai/chatkit/routes.py`: single `POST /api/v1/chatkit` endpoint
9. Mount chatkit route in `main.py`
10. Add `chatkit` to `requirements.txt`

**Acceptance**:
- Threads persist in database and load on return (SC-006: <1s)
- AI responds with streaming SSE (SC-005: <2s to first token)
- RAG search only returns content from unlocked stages (FR-020)
- Rate limit enforced: 21st message returns 429 (FR-027)
- AI uses Socratic method (guiding questions, not direct answers)

---

### Phase 7: ChatKit Frontend (Widget + Context Injection + Thread Management)
> **Goal**: ChatKit React widget on lesson pages with text selection, context injection, thread management.
> **Depends on**: Phase 5 (auth client for JWT), Phase 6 (ChatKit backend endpoint)
> **Delivers**: FR-014, FR-015, FR-016, FR-017

**Steps**:
1. Install `@openai/chatkit-react` in frontend `package.json`
2. Create `components/ai/ChatKitWidget.tsx`:
   - `useChatKit()` with custom `api.url` pointing to `/api/v1/chatkit`
   - Custom `fetch` override injecting JWT Bearer token from Better-Auth session
   - Inject user identity headers: X-User-Id, X-User-Role, X-User-Stage
   - Handle `onError` (show toast), `onResponseStart`/`onResponseEnd` (loading state)
   - Handle rate limit errors (show "daily limit reached" message)
3. Create `components/ai/TextSelectionAsk.tsx`:
   - Detect text selection on lesson content areas (FR-017)
   - Show floating "Ask AI" button on selection
   - On click: open ChatKit widget with selected text as pre-filled query with page context
4. Create `components/ai/ThreadList.tsx`:
   - List user's threads (ordered by last activity)
   - Show thread title and timestamp
   - Click to load thread history
   - "New Thread" button
5. Integrate ChatKit widget into lesson page `learn/[stageId]/[contentId]/page.tsx`:
   - Render ChatKitWidget in a slide-out panel or fixed sidebar
   - Pass page context (URL, title, headings, content summary)
   - Only render for authenticated users with verified email
6. Inject page context into every message via metadata (FR-016)

**Acceptance**:
- Chat widget loads within 3s of lesson page load (SC-004)
- Text selection on lesson content shows "Ask AI" button (SC-010)
- Selected text appears in chat input with context
- Thread list shows previous conversations
- New thread button creates fresh conversation
- Widget only renders for verified, authenticated users

---

### Phase 8: Observability + Polish
> **Goal**: Auth event logging, AI usage metrics, edge case handling, production readiness.
> **Depends on**: All previous phases
> **Delivers**: FR-028, FR-029, edge cases

**Steps**:
1. Verify auth event logging is complete (FR-028):
   - Login success/failure, registration, logout, password reset, OAuth link/unlink
   - Each entry has: timestamp, user_id, email, IP, event_type
2. Implement AI usage metrics aggregation (FR-029):
   - Daily message count, average response time, error rate per user
   - Make metrics queryable via admin API endpoint
3. Handle edge cases from spec:
   - Auth server down: frontend shows "login unavailable" degraded state
   - Qdrant unreachable: AI tutor falls back to base knowledge with notice
   - Connection loss mid-conversation: messages saved server-side, resume on reconnect
   - JWKS unreachable: FastAPI uses cached keys, logs warning
4. Add thread retention cron job: delete threads where `enrollment_ended_at + 30 days < NOW()`
5. Set up Docker Compose health checks for all services
6. Update CORS configuration for three-service architecture
7. Final integration test: full flow from registration → OAuth → lesson → AI chat → thread persistence

**Acceptance**:
- `auth_event_log` captures all auth events with required fields
- `ai_usage_metric` tracks daily usage per user
- Graceful degradation when auth server unreachable
- Thread retention cleanup works correctly
- All success criteria (SC-001 through SC-010) pass

---

## Phase Dependency Graph

```
Phase 1: Auth Server Setup
    │
    ├──────────────────────┐
    ▼                      ▼
Phase 2: Social/Email    Phase 3: FastAPI JWKS
    │                      │
    │                      ├───────────────┐
    │                      ▼               ▼
    │                 Phase 4: Migration  Phase 6: ChatKit Backend
    │                      │               │
    ▼                      ▼               ▼
Phase 5: Frontend Auth ◄──┘          Phase 7: ChatKit Frontend
    │                                      │
    └──────────────┬───────────────────────┘
                   ▼
            Phase 8: Observability + Polish
```

**Critical Path**: Phase 1 → Phase 3 → Phase 6 → Phase 7 → Phase 8

**Parallel Tracks**:
- Track A (Auth): Phase 1 → Phase 2 → Phase 5
- Track B (Integration): Phase 1 → Phase 3 → Phase 4
- Track C (ChatKit): Phase 3 → Phase 6 → Phase 7
- All converge at Phase 8

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected Because |
|----------|------------|--------------------------------------|
| Separate Node.js auth server | Better-Auth is a Node.js library; can't run in Python FastAPI | Keeping custom Python auth doesn't provide OIDC/JWKS/PKCE standards compliance |
| 3-service architecture | Auth (Node.js) + API (Python) + Frontend (Next.js) | Combining auth into Next.js API routes mixes concerns and limits OIDC provider capability |
| ChatKit SDK over custom chat | Production-ready streaming UI, thread management, persistence | Custom chat requires significant UI effort with no advantage over ChatKit's mature implementation |

## Risks

| Risk | Mitigation |
|------|-----------|
| Big-bang migration failure | Backup before migration, staging validation, rollback script ready |
| Better-Auth breaking changes | Pin version in package.json, abstract critical integrations |
| ChatKit SDK immaturity | Pin version, integration tests, fallback to existing RAG chat if critical issues |
| Three-service operational complexity | Docker Compose orchestration, health checks, shared database simplifies data access |

## Follow-ups (Post-Feature)

- MFA via Better-Auth's two-factor plugin (out of scope for this feature)
- Admin UI for user management (currently API-only)
- ChatKit custom widgets for code exercises, interactive quizzes
- Mobile app auth support
