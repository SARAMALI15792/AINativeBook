---
description: "Task breakdown for Better-Auth OIDC Server + ChatKit AI Tutor integration"
---

# Tasks: Better-Auth OIDC Server + ChatKit AI Tutor

**Input**: Design documents from `/specs/002-better-auth-chatkit/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓
**Feature Branch**: `002-better-auth-chatkit`
**Date**: 2026-02-11

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Task can run in parallel (different files/services, no dependencies)
- **[Story]**: User story label (US1-US6) — used for Phase 3+ tasks only
- Include exact file paths in all descriptions

---

## Phase 1: Setup & Project Structure

**Purpose**: Create foundational directories, configuration, and Docker orchestration

- [ ] T001 Create `intellistack/auth-server/` directory structure with `src/`, `migrations/` folders
- [ ] T002 [P] Create `intellistack/auth-server/package.json` with Better-Auth, Express, Drizzle, TypeScript dependencies
- [ ] T003 [P] Create `intellistack/auth-server/tsconfig.json` with strict TypeScript config
- [ ] T004 [P] Create `intellistack/auth-server/Dockerfile` for Node.js 20+ auth server
- [ ] T005 [P] Update `docker-compose.yml` to add auth-server service (port 3001, depends on postgres)
- [ ] T006 Create `.env.example` for auth server (DATABASE_URL, BETTER_AUTH_SECRET, OAuth credentials, email provider)
- [ ] T007 [P] Create `.env.example` additions for FastAPI backend (BETTER_AUTH_URL, BETTER_AUTH_JWKS_URL)
- [ ] T008 [P] Create `.env.example` additions for Next.js frontend (NEXT_PUBLIC_BETTER_AUTH_URL)

---

## Phase 2: Foundational Infrastructure (BLOCKING — Auth System Core)

**Purpose**: Build the auth server skeleton and database foundation. **⚠️ CRITICAL**: Blocks all user stories.

### Database & Migrations
- [ ] T009 Create Alembic migration in `intellistack/backend/alembic/versions/` for ChatKit tables (chatkit_thread, chatkit_thread_item, chatkit_rate_limit, ai_usage_metric, auth_event_log)
- [ ] T010 Run `python -m alembic upgrade head` to apply ChatKit schema to PostgreSQL

### Better-Auth Server Setup
- [ ] T011 Create `intellistack/auth-server/src/index.ts` with Express app entry point (middleware, CORS, error handling)
- [ ] T012 [P] Create `intellistack/auth-server/src/db.ts` with Drizzle PostgreSQL adapter connected to Neon
- [ ] T013 [P] Create `intellistack/auth-server/src/auth.ts` with Better-Auth config (minimal: JWT plugin + OIDC Provider plugin + Admin plugin)
- [ ] T014 [P] Create `intellistack/auth-server/src/email.ts` with Resend API email handler (verification, password reset templates)
- [ ] T015 [P] Create `intellistack/auth-server/src/hooks.ts` with auth event logging hooks (login_success, login_failed, register, logout, password_reset, oauth_link, oauth_unlink)
- [ ] T016 Run `cd intellistack/auth-server && npx better-auth migrate` to create Better-Auth tables (user, session, account, verification, jwks, oauth_application)

### FastAPI Backend Auth Integration
- [ ] T017 Create `intellistack/backend/src/core/auth/jwks.py` with JWKS manager (fetch from auth server, cache 5min, fallback to last-known-good keys)
- [ ] T018 Create `intellistack/backend/src/core/auth/dependencies.py` with:
  - `AuthenticatedUser` dataclass (id, email, name, role, email_verified)
  - `get_current_user(request: Request) → AuthenticatedUser` dependency (extract Bearer token, verify RS256 via JWKS)
  - `require_role(*roles: str)` dependency factory for role checks
  - `require_verified_email(user: AuthenticatedUser)` dependency for email verification
- [ ] T019 Update `intellistack/backend/src/shared/middleware.py` to remove old BetterAuthSessionMiddleware and replace with JWKS-based JWT validation
- [ ] T020 Update `intellistack/backend/src/config/settings.py` to add `BETTER_AUTH_URL` and `BETTER_AUTH_JWKS_URL` from environment
- [ ] T021 Update `intellistack/backend/requirements.txt` to add PyJWT, jwcrypto; remove python-jose
- [ ] T022 Delete old auth code files:
  - `intellistack/backend/src/core/auth/routes.py` (v1)
  - `intellistack/backend/src/core/auth/routes_v2.py` (v2)
  - `intellistack/backend/src/core/auth/service.py` (v1)
  - `intellistack/backend/src/core/auth/service_v2.py` (v2)
  - `intellistack/backend/src/core/auth/adapter.py`
  - `intellistack/backend/src/core/auth/better_auth_config.py`

### Frontend Auth Scaffold
- [ ] T023 Update `intellistack/frontend/package.json` to add `@better-auth/react`, `better-auth` (same version as auth server)
- [ ] T024 Create `intellistack/frontend/src/lib/auth-client.ts` with Better-Auth React client configured to point to BETTER_AUTH_URL

**Checkpoint**: Foundation ready. Auth server endpoints respond, JWKS endpoint accessible, FastAPI can validate JWTs, frontend has auth client configured.

---

## Phase 3: User Story 1 - Email/Password Registration and Login (Priority: P1) 🎯 MVP

**Goal**: Users can register with email/password, verify email, log in, and maintain sessions.

**Independent Test**: Can register new account with valid password → receive verification email → click verification link → log in → refresh page (session persists) → log out. All credentials enforced server-side.

**Acceptance Scenarios from Spec**:
1. Valid registration creates account and sends verification email
2. Verified email + correct credentials log in successfully
3. Session persists across browser refresh
4. 5 failed logins lock account for 30 minutes
5. Sign out invalidates session

### Implementation for User Story 1

- [ ] T025 Configure Better-Auth email/password in `intellistack/auth-server/src/auth.ts`:
  - Password strength: 12+ chars, uppercase, lowercase, number, special char (FR-001)
  - Email verification enabled (FR-002)
  - Account lockout: 5 failed attempts → 30min cooldown (FR-007)
- [ ] T026 [P] [US1] Implement `POST /api/auth/sign-up/email` endpoint in auth server (returns user + session with JWT)
- [ ] T027 [P] [US1] Implement `POST /api/auth/sign-in/email` endpoint in auth server (validates credentials, returns JWT)
- [ ] T028 [P] [US1] Implement `POST /api/auth/sign-out` endpoint in auth server (invalidates session)
- [ ] T029 [P] [US1] Implement `GET /api/auth/get-session` endpoint in auth server (returns current user + session)
- [ ] T030 [P] [US1] Implement email verification token flow in auth server (send verification link, verify token)
- [ ] T031 [US1] Update `intellistack/frontend/src/hooks/useAuth.ts` to use Better-Auth hooks:
  - `useSession()` for session state
  - `authClient.signUp.email()`
  - `authClient.signIn.email()`
  - `authClient.signOut()`
- [ ] T032 [US1] Refactor `intellistack/frontend/src/app/(auth)/register/page.tsx`:
  - Use `signUp.email()` from Better-Auth
  - Display PasswordStrengthMeter (12+ chars requirement)
  - Show verification email prompt
- [ ] T033 [US1] Refactor `intellistack/frontend/src/app/(auth)/login/page.tsx`:
  - Use `signIn.email()` from Better-Auth
  - Show account lockout message after 5 failed attempts
- [ ] T034 [US1] Update `intellistack/frontend/src/components/auth/AuthGuard.tsx` to use `useSession()` from Better-Auth
- [ ] T035 [US1] Update `intellistack/frontend/src/middleware.ts` to use correct Better-Auth session cookie name (`better-auth.session_token`)
- [ ] T036 [US1] Add `auth_event_log` table population for registration/login events in auth server hooks (FR-028)

**Checkpoint**: Email/password auth fully functional. Users can register, verify email, log in, session persists, account lockout works.

---

## Phase 4: User Story 2 - OAuth Social Login (Priority: P1)

**Goal**: Users can sign in with Google or GitHub, accounts auto-link on email match.

**Independent Test**: Click "Sign in with Google" → complete OAuth consent → arrive at dashboard with Google profile data. Repeat with GitHub. Link email+OAuth accounts.

**Acceptance Scenarios from Spec**:
1. OAuth redirect to Google/GitHub consent
2. First-time OAuth user creates account with provider profile data
3. Returning OAuth user signs in to existing account
4. Account linking: email-only user + OAuth with same email → linked
5. GitHub OAuth works identically to Google

### Implementation for User Story 2

- [ ] T037 Configure Google OAuth in `intellistack/auth-server/src/auth.ts` (clientId, clientSecret from env)
- [ ] T038 [P] [US2] Configure GitHub OAuth in `intellistack/auth-server/src/auth.ts` (clientId, clientSecret from env)
- [ ] T039 [P] [US2] Implement `POST /api/auth/sign-in/social` endpoint in auth server (returns OAuth URL for redirect)
- [ ] T040 [P] [US2] Implement `GET /api/auth/callback/{provider}` endpoint in auth server (OAuth callback, create/link user, set session)
- [ ] T041 [US2] Add account linking logic in auth server (match by email, merge accounts if email verified on both)
- [ ] T042 [US2] Update `intellistack/frontend/src/components/auth/SocialLoginButtons.tsx`:
  - Google button: calls `authClient.signIn.social('google')`
  - GitHub button: calls `authClient.signIn.social('github')`
- [ ] T043 [US2] Update `intellistack/frontend/src/app/(auth)/login/page.tsx` to include OAuth buttons
- [ ] T044 [US2] Implement PKCE for public client flows in Better-Auth config (FR-006)
- [ ] T045 [US2] Add oauth_link/oauth_unlink events to auth_event_log via hooks (FR-028)

**Checkpoint**: OAuth login fully functional. Google and GitHub logins work, accounts link on email match, user profile data populated.

---

## Phase 5: User Story 5 - Password Recovery (Priority: P3)

**Goal**: Users can reset forgotten passwords via email link (1-hour expiry).

**Independent Test**: Request reset from forgot-password page → receive email with link → click link → set new password → log in with new password.

**Acceptance Scenarios from Spec**:
1. Password reset email sent with secure time-limited link
2. Valid reset link + new valid password → password updated
3. Expired reset link (>1h) shows clear message
4. Non-registered email → same "check your email" message (no enumeration)

### Implementation for User Story 5

- [ ] T046 [P] [US5] Implement `POST /api/auth/forget-password` endpoint in auth server (send reset email, no enumeration)
- [ ] T047 [P] [US5] Implement `POST /api/auth/reset-password` endpoint in auth server (validate token 1h expiry, update password)
- [ ] T048 [US5] Create forgot-password page `intellistack/frontend/src/app/(auth)/forgot-password/page.tsx`:
  - Email input
  - Call `authClient.forgetPassword()`
  - Show "check your email" message
- [ ] T049 [US5] Create reset-password page `intellistack/frontend/src/app/(auth)/reset-password/page.tsx`:
  - Extract token from URL query param
  - New password input with PasswordStrengthMeter
  - Call `authClient.resetPassword(token, newPassword)`
  - Show success/error messages
- [ ] T050 [US5] Add password_reset events to auth_event_log (FR-028)

**Checkpoint**: Password recovery fully functional. Users can reset forgotten passwords securely.

---

## Phase 6: User Story 6 - Role-Based Access Control (Priority: P3)

**Goal**: Role assignment (student/instructor/admin) with JWT claims and API enforcement.

**Independent Test**: Admin assigns instructor role to user → user gains access to content creation features on next page load.

**Acceptance Scenarios from Spec**:
1. Admin assigns "instructor" role → student gets creation tools
2. Instructor cannot access admin-only features (403)
3. Student cannot access instructor content routes (redirect)
4. Role change takes effect in current session (no re-login)

### Implementation for User Story 6

- [ ] T051 Enable Admin plugin in Better-Auth config with roles: student (default), instructor, admin (FR-009)
- [ ] T052 [P] [US6] Implement admin API endpoint for role assignment in FastAPI `intellistack/backend/src/core/admin/` (POST to assign role, requires admin role)
- [ ] T053 [US6] Update `intellistack/frontend/src/components/auth/AuthGuard.tsx` to check role and redirect based on permissions
- [ ] T054 [US6] Verify role claims included in JWT tokens issued by Better-Auth (FR-009)
- [ ] T055 [US6] Add role change events to auth_event_log (FR-028)

**Checkpoint**: Role-based access control functional. Admins can assign roles, enforcement working in FastAPI and frontend.

---

## Phase 7: Data Migration (Priority: High — Blocking user access)

**Goal**: Migrate existing users from old auth tables to Better-Auth schema without data loss (big-bang cutover).

**Acceptance Scenarios from Spec**:
- SC-008: Zero user data lost during migration
- All existing users can log in with current passwords
- OAuth-linked accounts still work
- Role assignments preserved

### Implementation for Phase 7

- [ ] T056 Create pre-migration backup script `intellistack/auth-server/migrations/backup.sh` (backup Neon database)
- [ ] T057 [P] Create data migration script `intellistack/auth-server/migrations/migrate-data.ts`:
  - Read existing users → insert into Better-Auth `user` table (preserve UUIDs)
  - Move password hashes → `account` table (provider_id='credential')
  - Move OAuth accounts → `account` table with provider mapping
  - Move active sessions → `session` table (drop expired)
  - Move historical login attempts → `auth_event_log`
  - Flatten user_role → user.role field
- [ ] T058 [P] Create validation script `intellistack/auth-server/migrations/validate-migration.ts`:
  - For each migrated user, verify authentication works with current password
  - Verify OAuth links still resolve correctly
  - Verify role assignments preserved
- [ ] T059 Create rollback script `intellistack/auth-server/migrations/rollback.sh` (restore from backup)
- [ ] T060 Run migration on staging database first, validate, document findings
- [ ] T061 Create database backup (production)
- [ ] T062 Run migration script on production database
- [ ] T063 Run validation script post-migration
- [ ] T064 Verify all FastAPI routes still work with migrated user data
- [ ] T065 Update all existing route handlers in FastAPI to use new `get_current_user` dependency (replaces old auth dependency)

**Checkpoint**: All existing users migrated successfully. Production auth fully switched to Better-Auth.

---

## Phase 8: ChatKit Backend - Server, Store, and Agent (Priority: P2)

**Goal**: ChatKit Python server integrated into FastAPI with persistent threads and RAG-augmented Socratic tutor.

**Depends on**: Phase 2 (JWKS validation), Phase 7 (data migration complete)

**Accepts**: FR-018, FR-019, FR-020, FR-021, FR-024, FR-027

### SQLAlchemy Models & Database
- [ ] T066 Create `intellistack/backend/src/ai/chatkit/models.py` with SQLAlchemy async models:
  - `ChatKitThread`: id, user_id, title, course_id, lesson_stage, status, metadata, created_at, updated_at, enrollment_ended_at
  - `ChatKitThreadItem`: id, thread_id, type, role, content, metadata, created_at
  - `ChatKitRateLimit`: id, user_id, message_count, window_start, updated_at
  - `AIUsageMetric`: id, user_id, date, message_count, total_response_time_ms, error_count, created_at

### ChatKit Store Implementation
- [ ] T067 Create `intellistack/backend/src/ai/chatkit/store.py` with `PostgresChatKitStore` extending ChatKit's Store base class:
  - `create_thread(user_id, metadata) → Thread`
  - `load_thread(thread_id) → Thread`
  - `load_thread_items(thread_id, limit) → list[ThreadItem]`
  - `save_thread_item(thread_id, item) → ThreadItem`
  - `delete_thread(thread_id)`
  - `list_threads(user_id, limit) → list[Thread]`
  - Include retention: delete threads where `enrollment_ended_at + 30 days < NOW()`

### Context & Rate Limiting
- [ ] T068 [P] Create `intellistack/backend/src/ai/chatkit/context.py` with `RequestContext` dataclass:
  - user_id, user_email, user_name, user_role, user_stage
  - page_url, page_title, page_headings, selected_text
  - course_id, lesson_stage
- [ ] T069 [P] Create `intellistack/backend/src/ai/chatkit/rate_limiter.py` with rate limit checker:
  - Check/increment message count per user per 24h rolling window (20 msg/day student limit)
  - Exempt instructors/admins (unlimited)
  - Return remaining count + reset time (FR-027)

### AI Tutor Agent
- [ ] T070 Create `intellistack/backend/src/ai/chatkit/agent.py` with Socratic tutor agent:
  - Extend existing `ai/tutor/agents.py` or create new agent using OpenAI Agents SDK
  - System prompt: Socratic teaching method (guiding questions before answers)
  - RAG tool: search Qdrant with stage-based access control (only unlocked stages)
  - Use existing `ai/rag/retrieval.py` HybridRetriever for content search
  - Use existing `ai/tutor/guardrails.py` for Socratic guardrails

### ChatKit Server & Routes
- [ ] T071 Create `intellistack/backend/src/ai/chatkit/server.py` with `IntelliStackChatKitServer` extending ChatKitServer:
  - `respond(thread, input_message, context)` method:
    - Authenticate user via JWT
    - Check rate limit (20 msg/day for students, FR-027)
    - Extract RequestContext from headers + metadata
    - Run RAG retrieval with stage-based access (FR-020)
    - Run Socratic agent
    - Yield streaming ThreadStreamEvents (SSE)
    - Track usage metrics (FR-029)
- [ ] T072 Create `intellistack/backend/src/ai/chatkit/routes.py` with single endpoint:
  - `POST /api/v1/chatkit` — ChatKit protocol handler
  - Requires JWT + email verified (FR-024)
  - Handles: thread create, message send, history load, thread list, thread delete
  - Returns SSE stream for message send operations
  - Include rate limit response headers (X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)
- [ ] T073 Mount ChatKit routes in `intellistack/backend/src/main.py`
- [ ] T074 Update `intellistack/backend/requirements.txt` to add `chatkit` and any missing dependencies

### Logging & Observability
- [ ] T075 Populate `auth_event_log` for all ChatKit operations (message send, thread create, rate limit hits)
- [ ] T076 Populate `ai_usage_metric` daily aggregation (message_count, response_time_ms, error_count per user)

**Checkpoint**: ChatKit backend fully functional. Threads persist, AI responds with streaming SSE, rate limiting enforced, stage-based access control working.

---

## Phase 9: ChatKit Frontend - Widget, Context Injection, Thread Management (Priority: P2)

**Goal**: ChatKit React widget on lesson pages with text selection, context injection, thread management.

**Depends on**: Phase 2 (auth client), Phase 8 (ChatKit backend)

**Accepts**: FR-014, FR-015, FR-016, FR-017

### ChatKit Widget Component
- [ ] T077 Create `intellistack/frontend/src/components/ai/ChatKitWidget.tsx`:
  - Import `useChatKit` from `@openai/chatkit-react`
  - Configure API endpoint: `/api/v1/chatkit`
  - Custom `fetch` override that:
    - Injects JWT Bearer token from Better-Auth session
    - Injects headers: X-User-Id, X-User-Role, X-User-Stage
    - Injects metadata: pageContext (url, title, headings, selectedText)
  - Handle `onError` (show toast)
  - Handle `onResponseStart` / `onResponseEnd` (loading state)
  - Handle rate limit error 429 (show "daily limit reached" message with reset time)

### Text Selection Feature
- [ ] T078 Create `intellistack/frontend/src/components/ai/TextSelectionAsk.tsx`:
  - Detect text selection on lesson content areas (query selector for lesson page)
  - Show floating "Ask AI" button on selection (position near selected text)
  - On click: open ChatKit widget with:
    - Selected text as pre-filled query
    - Page context (URL, title, headings)
    - Metadata highlighting selected text (FR-017)

### Thread Management
- [ ] T079 Create `intellistack/frontend/src/components/ai/ThreadList.tsx`:
  - List user's threads (ordered by last activity desc)
  - Show thread title and timestamp for each
  - Click to load thread history into ChatKit widget
  - "New Thread" button to create fresh conversation
  - Delete thread option

### Lesson Page Integration
- [ ] T080 Integrate ChatKitWidget into lesson page `intellistack/frontend/src/app/(dashboard)/learn/[stageId]/[contentId]/page.tsx`:
  - Render ChatKitWidget in a slide-out panel or fixed sidebar
  - Pass page context (extract from page data: URL, title, headings, content summary)
  - Only render for authenticated users with verified email (check `useSession()`)
  - Show loading skeleton while widget initializes
- [ ] T081 Integrate TextSelectionAsk into lesson page (wrap lesson content with text selection detection)
- [ ] T082 Add context injection middleware in `intellistack/frontend/src/lib/auth-client.ts`:
  - Override fetch to inject page context headers
  - Extract user identity from Better-Auth session
  - Extract current stage from user profile

### Error Handling & UX
- [ ] T083 Handle rate limit errors in ChatKitWidget:
  - Display "You've reached your daily message limit (20/20). Resets in Xh Ym."
  - Show reset time from response header (X-RateLimit-Reset)
- [ ] T084 Handle auth server downtime gracefully:
  - Show "Chat temporarily unavailable" message if backend returns 503
  - Suggest user try again later
- [ ] T085 Show "Email verification required to use AI tutor" for unverified users

**Checkpoint**: ChatKit frontend fully functional. Chat widget loads on lesson pages, text selection works, thread management functional, all context injected correctly.

---

## Phase 10: Observability & Monitoring (Priority: Medium)

**Goal**: Auth event logging, AI usage metrics, edge case handling, production readiness.

**Depends on**: All previous phases

### Auth Event Logging
- [ ] T086 Verify auth_event_log populated for all auth events:
  - login_success, login_failed (with failure reason), register, logout, password_reset, oauth_link, oauth_unlink
  - Each entry: timestamp, user_id (or attempted email), email, ip_address, user_agent, details (JSONB)
- [ ] T087 [P] Create admin API endpoint to query auth events: `GET /api/v1/admin/auth-events` (requires admin)
- [ ] T088 [P] Create audit log view/export for compliance

### AI Usage Metrics
- [ ] T089 Implement ai_usage_metric aggregation in ChatKit server:
  - Daily message count, average response time, error rate per user
  - Aggregate on each message send (increment counters in ai_usage_metric table)
- [ ] T090 [P] Create admin API endpoint to query usage metrics: `GET /api/v1/admin/ai-usage` (requires admin)
- [ ] T091 [P] Create dashboard view for usage analytics (admin-only)

### Edge Cases & Degradation
- [ ] T092 Handle auth server down:
  - Frontend checks auth server health
  - Show "login unavailable" message if auth server unreachable
  - Users with valid cached sessions can continue
  - Graceful degradation in status page
- [ ] T093 [P] Handle Qdrant unreachable:
  - AI tutor falls back to base knowledge (no RAG augmentation)
  - Show notice: "Search results may be limited"
- [ ] T094 [P] Handle connection loss mid-conversation:
  - Save messages server-side immediately
  - Resume conversation on reconnect without message loss
- [ ] T095 [P] Handle JWKS unreachable:
  - FastAPI uses cached keys (5min TTL)
  - Log warning on cache fallback
  - If no cached keys exist: return 503 with Retry-After header

### Thread Retention & Cleanup
- [ ] T096 Create cron job to delete expired threads:
  - Delete threads where `enrollment_ended_at + 30 days < NOW()`
  - Run daily (e.g., 2 AM UTC)
  - Log deletion count
- [ ] T097 [P] Create manual thread cleanup endpoint for admins: `DELETE /api/v1/admin/chatkit/cleanup` (requires admin)

### Docker Compose Health Checks
- [ ] T098 Add health checks to docker-compose.yml:
  - Auth server: GET `/.well-known/openid-configuration`
  - FastAPI backend: GET `/health`
  - PostgreSQL: pg_isready
  - Set intervals, timeouts, retry counts
- [ ] T099 [P] Update CORS configuration for three-service architecture:
  - Auth server CORS: allow frontend URL
  - FastAPI CORS: allow frontend URL + auth server (for JWKS fetch)
  - Frontend middleware: validate origins

### Integration Test
- [ ] T100 Create end-to-end integration test `intellistack/tests/e2e/test_full_flow.py`:
  - Registration → email verification → OAuth → lesson access → AI chat → thread persistence → logout
  - Use Playwright or similar for frontend steps
  - Verify all success criteria (SC-001 through SC-010) pass

**Checkpoint**: Production ready. Observability complete, edge cases handled, health checks configured, full integration test passing.

---

## Phase 11: Polish & Documentation

**Purpose**: Final refinement, documentation, and cleanup

- [ ] T101 [P] Update README.md with Better-Auth + ChatKit architecture overview
- [ ] T102 [P] Create deployment guide: `intellistack/docs/DEPLOYMENT.md` (env vars, secrets, scaling)
- [ ] T103 [P] Create troubleshooting guide: `intellistack/docs/TROUBLESHOOTING.md` (common issues, auth server down, JWKS failures)
- [ ] T104 [P] Create API documentation: `intellistack/docs/API.md` (auth endpoints, ChatKit endpoints, contracts)
- [ ] T105 Update `intellistack/backend/DATABASE_SETUP.md` with ChatKit table schema
- [ ] T106 Update `intellistack/backend/RUN_BACKEND.bat` to include BETTER_AUTH_URL setup
- [ ] T107 Update `intellistack/frontend/RUN_FRONTEND.bat` to include NEXT_PUBLIC_BETTER_AUTH_URL setup
- [ ] T108 [P] Code cleanup: remove unused imports, dead code from old auth system
- [ ] T109 [P] Security audit: verify no hardcoded secrets, all credentials via env
- [ ] T110 Run `/sp.specify`, `/sp.analyze` to validate feature completeness against spec

**Checkpoint**: Feature complete, documented, and ready for production release.

---

## Phase Dependencies & Execution Order

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational (Auth Server Core, JWKS Validation, DB Schema)
    │
    ├──────────────────────────────────┬──────────────────┬──────────────────┐
    ▼                                  ▼                  ▼                  ▼
Phase 3: US1 (Email/Password)     Phase 4: US2 (OAuth)  Phase 5: US5 (Password Recovery)  Phase 6: US6 (RBAC)
    │                                  │                  │                  │
    └──────────────────────────────────┼──────────────────┼──────────────────┘
                                       ▼
                              Phase 7: Data Migration
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
            Phase 8: ChatKit Backend  (after migration)
                    │
                    ▼
            Phase 9: ChatKit Frontend
                    │
                    ▼
            Phase 10: Observability & Polish
                    │
                    ▼
            Phase 11: Final Polish & Documentation
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 7 → Phase 8 → Phase 9 → Phase 10 → Phase 11

**Parallel Tracks After Phase 2**:
- **Auth Track**: Phase 3 → Phase 4 → Phase 5 → Phase 6 (can proceed in parallel with Migration)
- **Migration Track**: Phase 7 (depends on Phase 3 completion)
- **ChatKit Track**: Phase 8 → Phase 9 (depends on Phase 7)
- **All converge at Phase 10**

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)
1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational ✓
3. Complete Phase 3: US1 (Email/Password) ✓
4. Complete Phase 4: US2 (OAuth) ✓
5. **STOP and VALIDATE**: Both stories work, auth flows complete
6. Deploy/demo email + OAuth auth (MVP!)

### Incremental Delivery
1. Foundation → US1 + US2 → migrate data → validate all users can log in
2. Add US5 (Password Recovery) → test independently
3. Add US6 (RBAC) → test role enforcement
4. Add ChatKit Backend + Frontend → test AI tutor independent of auth
5. Add Observability → production ready

### Parallel Team Strategy (if multiple developers)
1. **Developer A**: Phase 1 + Phase 2 (Setup + Foundational) — **CRITICAL PATH**
2. After Phase 2 complete:
   - **Developer B**: Phase 3 + Phase 4 (US1 + US2 email/OAuth)
   - **Developer C**: Phase 7 (Data Migration) — can start after Phase 3
   - **Developer D**: Phase 8 (ChatKit Backend) — depends on Phase 7
3. After Phase 7:
   - **Developer E**: Phase 9 (ChatKit Frontend) — depends on Phase 8
4. All merge at Phase 10 (Observability)

---

## Task Labeling Reference

**[P]** = Parallelizable task (different files/services, no blocking dependencies)

**[US1-US6]** = User story mapping:
- US1 = Email/Password Registration and Login
- US2 = OAuth Social Login
- US5 = Password Recovery
- US6 = Role-Based Access Control
- (US3, US4 = Chat-related, handled in Phases 8-9 instead of separate phases)

**No label** = Setup, Foundational, or cross-cutting task

---

## File Path Conventions

### Auth Server (New)
- `intellistack/auth-server/src/index.ts` — Express entry
- `intellistack/auth-server/src/auth.ts` — Better-Auth config
- `intellistack/auth-server/src/db.ts` — Drizzle adapter
- `intellistack/auth-server/src/email.ts` — Email handler
- `intellistack/auth-server/src/hooks.ts` — Auth hooks
- `intellistack/auth-server/migrations/migrate-data.ts` — Data migration

### FastAPI Backend (Updated)
- `intellistack/backend/src/core/auth/jwks.py` — JWKS manager (NEW)
- `intellistack/backend/src/core/auth/dependencies.py` — Auth dependencies (NEW)
- `intellistack/backend/src/shared/middleware.py` — JWT validation (UPDATED)
- `intellistack/backend/src/config/settings.py` — Auth URL config (UPDATED)
- `intellistack/backend/src/ai/chatkit/server.py` — ChatKit server (NEW)
- `intellistack/backend/src/ai/chatkit/store.py` — ChatKit store (NEW)
- `intellistack/backend/src/ai/chatkit/context.py` — Request context (NEW)
- `intellistack/backend/src/ai/chatkit/rate_limiter.py` — Rate limiting (NEW)
- `intellistack/backend/src/ai/chatkit/agent.py` — Socratic agent (NEW)
- `intellistack/backend/src/ai/chatkit/routes.py` — ChatKit endpoints (NEW)
- `intellistack/backend/src/ai/chatkit/models.py` — SQLAlchemy models (NEW)

### Next.js Frontend (Updated)
- `intellistack/frontend/src/lib/auth-client.ts` — Better-Auth client (UPDATED)
- `intellistack/frontend/src/hooks/useAuth.ts` — Auth hooks (UPDATED)
- `intellistack/frontend/src/components/auth/AuthProvider.tsx` — Session provider (UPDATED)
- `intellistack/frontend/src/components/auth/AuthGuard.tsx` — Auth guard (UPDATED)
- `intellistack/frontend/src/app/(auth)/login/page.tsx` — Login page (UPDATED)
- `intellistack/frontend/src/app/(auth)/register/page.tsx` — Register page (UPDATED)
- `intellistack/frontend/src/app/(auth)/forgot-password/page.tsx` — Forgot password (NEW)
- `intellistack/frontend/src/app/(auth)/reset-password/page.tsx` — Reset password (NEW)
- `intellistack/frontend/src/components/ai/ChatKitWidget.tsx` — Chat widget (NEW)
- `intellistack/frontend/src/components/ai/TextSelectionAsk.tsx` — Text selection (NEW)
- `intellistack/frontend/src/components/ai/ThreadList.tsx` — Thread management (NEW)

### Database
- `intellistack/backend/alembic/versions/` — Alembic migrations for ChatKit + auth_event_log tables

### Configuration
- `docker-compose.yml` — Add auth-server service
- `.env.example` — Auth server env vars
- `quickstart.md` — Already exists; verified steps in this plan

---

## Success Metrics & Acceptance Criteria

All tasks must satisfy:

1. **Code Review**: All file paths explicit, no vague descriptions
2. **Testability**: Each task independently verifiable before next task
3. **Dependency Clarity**: Dependencies marked, no circular dependencies
4. **Checkpoint Validation**: Each checkpoint phase independently testable
5. **No Scope Creep**: Tasks focus on stated requirements, no extra features

---

## Notes

- Each task is specific enough for an LLM or developer to complete without additional context
- Phases are sequenced to enable independent testing at checkpoints
- Use [P] markers to identify tasks that can run in parallel
- User stories are independently testable increments
- All file paths are absolute and updated from design documents
- Alembic migration required for new tables (handled in Phase 2)
- No hardcoded secrets; all credentials via environment variables
