# Implementation Tasks: Docusaurus Authentication Migration & Onboarding

**Branch**: `002-docusaurus-auth-migration` | **Date**: 2026-02-25 | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Task Format

```
- [ ] [TaskID] [Priority] [Story] Description with file path
```

**Priority**: P1 (Critical), P2 (Important), P3 (Nice-to-have)
**Story**: US1 (User Story 1), US2 (User Story 2), US3 (User Story 3), US4 (User Story 4)

---

## User Story 1: Student Authentication & Onboarding (P1)

### Database Schema & Migration

- [x] [T001] [P1] [US1] Create Alembic migration to add onboarding columns to users table (email_verified, onboarding_completed, current_stage, role, preferences) with idempotent checks - `intellistack/backend/alembic/versions/20260225_add_onboarding_columns.py`

- [x] [T002] [P1] [US1] Add database indexes for onboarding_completed and current_stage columns in migration - `intellistack/backend/alembic/versions/20260225_add_onboarding_columns.py`

- [x] [T003] [P1] [US1] Add check constraints for current_stage (1-5) and role (student/instructor/admin) in migration - `intellistack/backend/alembic/versions/20260225_add_onboarding_columns.py`

- [x] [T004] [P1] [US1] Run Alembic migration and verify schema changes in PostgreSQL database - `intellistack/backend/`

**Acceptance**: Users table has all required columns, indexes created, constraints enforced, migration is idempotent

---

### Better Auth Server Configuration

- [x] [T005] [P1] [US1] Update Better Auth configuration with email/password authentication (minPasswordLength: 8, requireEmailVerification: false) - `intellistack/auth-server/src/auth.ts`

- [x] [T006] [P1] [US1] Configure Better Auth session settings (expiresIn: 24h, updateAgeSession: 1h) - `intellistack/auth-server/src/auth.ts`

- [x] [T007] [P1] [US1] Configure Better Auth cookie settings (SameSite: Lax, Secure in production, path: /) - `intellistack/auth-server/src/auth.ts`

- [x] [T008] [P1] [US1] Configure Google OAuth provider with client ID, secret, and redirect URI - `intellistack/auth-server/src/auth.ts`

**Acceptance**: Better Auth configured with correct authentication methods, session management, and OAuth provider

---

### Onboarding API Endpoints

- [x] [T009] [P1] [US1] Create onboarding routes file with Express router - `intellistack/auth-server/src/routes/onboarding.ts`

- [x] [T010] [P1] [US1] Implement GET /api/auth/onboarding/status endpoint to return onboarding completion status and preferences - `intellistack/auth-server/src/routes/onboarding.ts`

- [x] [T011] [P1] [US1] Implement POST /api/auth/onboarding/step endpoint to save step data to users.preferences JSON field - `intellistack/auth-server/src/routes/onboarding.ts`

- [x] [T012] [P1] [US1] Implement POST /api/auth/onboarding/complete endpoint to set onboarding_completed=true after all steps - `intellistack/auth-server/src/routes/onboarding.ts`

- [x] [T013] [P1] [US1] Add validation logic for each onboarding step (basic_info, education, interests, additional) - `intellistack/auth-server/src/routes/onboarding.ts`

- [x] [T014] [P1] [US1] Register onboarding routes in Express app at /api/auth/onboarding - `intellistack/auth-server/src/index.ts`

**Acceptance**: All onboarding endpoints functional, validation working, data persisted to database

---

### Docusaurus Better Auth Client

- [x] [T015] [P1] [US1] Create Better Auth client with lazy singleton pattern and Proxy for SSR compatibility - `intellistack/content/src/lib/auth.ts`

- [x] [T016] [P1] [US1] Configure Better Auth client with baseURL pointing to auth server - `intellistack/content/src/lib/auth.ts`

- [x] [T017] [P1] [US1] Export auth client methods (signIn, signUp, signOut, useSession) - `intellistack/content/src/lib/auth.ts`

**Acceptance**: Auth client initialized correctly, works in browser, handles SSR gracefully

---

### Docusaurus Authentication Context

- [x] [T018] [P1] [US1] Create AuthContext with React Context API for session state management - `intellistack/content/src/contexts/AuthContext.tsx`

- [x] [T019] [P1] [US1] Implement AuthProvider component with session loading and refresh logic - `intellistack/content/src/contexts/AuthContext.tsx`

- [x] [T020] [P1] [US1] Export useAuth hook for consuming authentication state in components - `intellistack/content/src/contexts/AuthContext.tsx`

- [x] [T021] [P1] [US1] Wrap Docusaurus app with AuthProvider in Root theme component - `intellistack/content/src/theme/Root.tsx`

**Acceptance**: Auth context provides session state to all components, updates on login/logout

---

### Authentication Pages

- [x] [T022] [P1] [US1] Create login page with email/password form and Google OAuth button - `intellistack/content/src/pages/auth/login.tsx`

- [x] [T023] [P1] [US1] Create signup page with email/password form and Google OAuth button - `intellistack/content/src/pages/auth/signup.tsx`

- [x] [T024] [P1] [US1] Create OAuth callback page to handle Google redirect and session creation - `intellistack/content/src/pages/auth/callback.tsx`

- [x] [T025] [P1] [US1] Add form validation and error handling to login/signup pages - `intellistack/content/src/pages/auth/login.tsx`, `intellistack/content/src/pages/auth/signup.tsx`

- [x] [T026] [P1] [US1] Wrap auth pages with BrowserOnly component for SSR compatibility - `intellistack/content/src/pages/auth/login.tsx`, `intellistack/content/src/pages/auth/signup.tsx`

**Acceptance**: Users can sign up, log in with email/password or Google, see validation errors

---

### Onboarding Pages

- [x] [T027] [P1] [US1] Create onboarding Step 1 page (Basic Information) with form fields: full name, preferred language, timezone - `intellistack/content/src/pages/onboarding/step-1.tsx`

- [x] [T028] [P1] [US1] Create onboarding Step 2 page (Educational Background) with form fields: education level, field of study, prior experience - `intellistack/content/src/pages/onboarding/step-2.tsx`

- [x] [T029] [P1] [US1] Create onboarding Step 3 page (Academic Interests) with form fields: learning goals (multi-select), learning style, topics of interest (multi-select) - `intellistack/content/src/pages/onboarding/step-3.tsx`

- [x] [T030] [P1] [US1] Create onboarding Step 4 page (Additional Details) with optional fields: how_did_you_hear, additional_notes - `intellistack/content/src/pages/onboarding/step-4.tsx`

- [x] [T031] [P1] [US1] Implement step indicator component showing current step (1 → 2 → 3 → 4) - `intellistack/content/src/components/onboarding/StepIndicator.tsx`

- [x] [T032] [P1] [US1] Add step indicator to all onboarding pages - `intellistack/content/src/pages/onboarding/step-*.tsx`

- [x] [T033] [P1] [US1] Implement form validation for each step with inline error messages - `intellistack/content/src/pages/onboarding/step-*.tsx`

- [x] [T034] [P1] [US1] Implement "Next" button handler to save step data via POST /api/auth/onboarding/step - `intellistack/content/src/pages/onboarding/step-1.tsx`, `step-2.tsx`, `step-3.tsx`

- [x] [T035] [P1] [US1] Implement "Complete" button handler to save step data and call POST /api/auth/onboarding/complete - `intellistack/content/src/pages/onboarding/step-4.tsx`

- [x] [T036] [P1] [US1] Implement "Back" button navigation to allow editing previous steps - `intellistack/content/src/pages/onboarding/step-2.tsx`, `step-3.tsx`, `step-4.tsx`

- [x] [T037] [P1] [US1] Add redirect logic to /stage-1/intro after onboarding completion - `intellistack/content/src/pages/onboarding/step-4.tsx`

**Acceptance**: All 4 onboarding steps functional, validation working, data saved on step completion, redirect to book content after completion

---

### Protected Routes

- [x] [T038] [P1] [US1] Create ProtectedRoute component with client-side authentication check - `intellistack/content/src/components/ProtectedRoute.tsx`

- [x] [T039] [P1] [US1] Add onboarding completion check to ProtectedRoute (redirect to /onboarding/step-1 if incomplete) - `intellistack/content/src/components/ProtectedRoute.tsx`

- [x] [T040] [P1] [US1] Add redirect to /auth/login with returnUrl parameter if unauthenticated - `intellistack/content/src/components/ProtectedRoute.tsx`

- [x] [T041] [P1] [US1] Wrap DocPage Layout with ProtectedRoute to protect all book content - `intellistack/content/src/theme/DocPage/Layout/index.tsx`

**Acceptance**: Unauthenticated users redirected to login, authenticated users with incomplete onboarding redirected to onboarding, completed users access content

---

### Custom Navbar

- [x] [T042] [P1] [US1] Create AuthNavbarItem component showing Login/Signup buttons when unauthenticated - `intellistack/content/src/components/AuthNavbarItem.tsx`

- [x] [T043] [P1] [US1] Add User Menu dropdown to AuthNavbarItem showing user name and Logout button when authenticated - `intellistack/content/src/components/AuthNavbarItem.tsx`

- [x] [T044] [P1] [US1] Swizzle NavbarItem/ComponentTypes to register custom AuthNavbarItem - `intellistack/content/src/theme/NavbarItem/ComponentTypes.tsx`

- [x] [T045] [P1] [US1] Update Docusaurus config to add AuthNavbarItem to navbar - `intellistack/content/docusaurus.config.ts`

**Acceptance**: Navbar shows Login/Signup for unauthenticated users, User Menu for authenticated users

---

## User Story 2: Simplified Next.js Navigation (P2)

### Remove Authentication Code

- [x] [T046] [P2] [US2] Delete Better Auth client file from Next.js - `intellistack/frontend/src/lib/auth.ts`

- [x] [T047] [P2] [US2] Delete AuthContext from Next.js - `intellistack/frontend/src/contexts/AuthContext.tsx`

- [x] [T048] [P2] [US2] Delete UserMenu component from Next.js - `intellistack/frontend/src/components/UserMenu.tsx`

- [x] [T049] [P2] [US2] Delete ProtectedRoute component from Next.js - `intellistack/frontend/src/components/ProtectedRoute.tsx`

- [x] [T050] [P2] [US2] Delete auth pages directory from Next.js - `intellistack/frontend/src/app/auth/`

- [x] [T051] [P2] [US2] Delete authentication middleware from Next.js - `intellistack/frontend/src/middleware.ts`

- [x] [T052] [P2] [US2] Delete authentication API routes from Next.js - `intellistack/frontend/src/app/api/auth/`

**Acceptance**: No authentication-related code remains in Next.js codebase

---

### Update Next.js Navigation

- [x] [T053] [P2] [US2] Update Header component to show only: Login, Book, Home, Community (Coming Soon), AI Tutor (Coming Soon) - `intellistack/frontend/src/components/layout/Header.tsx`

- [x] [T054] [P2] [US2] Configure Login link to redirect to ${DOCUSAURUS_URL}/auth/login - `intellistack/frontend/src/components/layout/Header.tsx`

- [x] [T055] [P2] [US2] Configure Book link to redirect to ${DOCUSAURUS_URL}/stage-1/intro - `intellistack/frontend/src/components/layout/Header.tsx`

- [x] [T056] [P2] [US2] Add DOCUSAURUS_URL environment variable to Next.js .env files - `intellistack/frontend/.env.local`, `.env.production`

**Acceptance**: Next.js navigation shows only specified links, all links redirect correctly to Docusaurus

---

## User Story 3: Docusaurus Routing & Deployment (P1)

### Docusaurus Configuration

- [x] [T057] [P1] [US3] Set baseUrl to '/AINativeBook/' in Docusaurus config - `intellistack/content/docusaurus.config.ts`

- [x] [T058] [P1] [US3] Set routeBasePath to '/' in docs preset config - `intellistack/content/docusaurus.config.ts`

- [x] [T059] [P1] [US3] Set url to 'http://localhost:3005' for development, 'https://saramali15792.github.io' for production - `intellistack/content/docusaurus.config.ts`

- [x] [T060] [P1] [US3] Set trailingSlash to false in Docusaurus config - `intellistack/content/docusaurus.config.ts`

- [x] [T061] [P1] [US3] Add customFields for BETTER_AUTH_URL in Docusaurus config - `intellistack/content/docusaurus.config.ts`

- [x] [T062] [P1] [US3] Configure webpack aliases for Better Auth client imports - `intellistack/content/docusaurus.config.ts`

**Acceptance**: Docusaurus config has correct baseUrl, routeBasePath, url, and trailingSlash settings

---

### Routing Verification

- [x] [T063] [P1] [US3] Test navigation to http://localhost:3005/AINativeBook/ shows homepage without 404 - Manual test ✅ HTTP 200

- [x] [T064] [P1] [US3] Test internal navigation links (Stage 1, Stage 2, etc.) work without 404 - Manual test ✅ All stages return HTTP 200

- [ ] [T065] [P1] [US3] Test redirect from Next.js "Book" button lands on valid Docusaurus page - Manual test (requires Next.js running)

- [x] [T066] [P1] [US3] Test all auth pages (/auth/login, /auth/signup, /auth/callback) are accessible - Manual test ✅ All return HTTP 200

- [x] [T067] [P1] [US3] Test all onboarding pages (/onboarding/step-1 through step-4) are accessible - Manual test ✅ All return HTTP 200

**Acceptance**: All Docusaurus routes accessible, no 404 errors, redirects from Next.js work correctly

---

## User Story 4: Session & Database Integrity (P1)

### Database Verification

- [ ] [T068] [P1] [US4] Verify users table has all required columns with correct types and constraints - Manual database query

- [ ] [T069] [P1] [US4] Verify sessions table exists with correct schema - Manual database query

- [ ] [T070] [P1] [US4] Verify oauth_accounts table exists with correct schema - Manual database query

- [ ] [T071] [P1] [US4] Verify indexes created on users.email, sessions.token, sessions.user_id - Manual database query

**Acceptance**: All database tables have correct schema, indexes, and constraints

---

### Session Management Testing

- [x] [T072] [P1] [US4] Test user signup creates record in users table with correct default values - Manual test + database verification ✅ Verified

- [x] [T073] [P1] [US4] Test user login creates session record in sessions table with valid token and expiration - Manual test + database verification ✅ Verified

- [x] [T074] [P1] [US4] Test session cookie is set with correct attributes (HttpOnly, Secure in prod, SameSite=Lax) - Browser DevTools inspection ✅ Verified

- [ ] [T075] [P1] [US4] Test session persists across browser close/reopen within 24 hours - Manual test

- [ ] [T076] [P1] [US4] Test session expires after 24 hours and redirects to login - Manual test (or time manipulation)

- [x] [T077] [P1] [US4] Test logout revokes session and clears cookie - Manual test + database verification ✅ Verified

**Acceptance**: Sessions created correctly, persisted in database, cookies set properly, expiration works

---

### OAuth Integration Testing

- [ ] [T078] [P1] [US4] Test Google OAuth flow creates user record and session - Manual test + database verification

- [ ] [T079] [P1] [US4] Test Google OAuth creates oauth_accounts record linking provider to user - Manual test + database verification

- [ ] [T080] [P1] [US4] Test OAuth account linking when email matches existing user - Manual test + database verification

- [ ] [T081] [P1] [US4] Test OAuth callback redirects to onboarding if incomplete, book content if complete - Manual test

**Acceptance**: OAuth flow works end-to-end, accounts linked correctly, redirects work

---

### Onboarding Data Persistence

- [x] [T082] [P1] [US4] Test Step 1 completion saves basic_info to users.preferences JSON field - Manual test + database verification ✅ Verified

- [x] [T083] [P1] [US4] Test Step 2 completion saves education to users.preferences JSON field - Manual test + database verification ✅ Verified

- [x] [T084] [P1] [US4] Test Step 3 completion saves interests to users.preferences JSON field - Manual test + database verification ✅ Verified

- [x] [T085] [P1] [US4] Test Step 4 completion saves additional to users.preferences JSON field - Manual test + database verification ✅ Verified

- [x] [T086] [P1] [US4] Test onboarding completion sets onboarding_completed=true in database - Manual test + database verification ✅ Verified

- [ ] [T087] [P1] [US4] Test incomplete onboarding step data is lost if user closes browser mid-step - Manual test

**Acceptance**: Onboarding data saved correctly to database, onboarding_completed flag set after Step 4

---

### Environment Configuration

- [x] [T088] [P1] [US4] Verify BETTER_AUTH_URL environment variable set correctly in auth server - `intellistack/auth-server/.env` ✅ Verified

- [x] [T089] [P1] [US4] Verify BETTER_AUTH_SECRET environment variable set in auth server - `intellistack/auth-server/.env` ✅ Verified

- [x] [T090] [P1] [US4] Verify DATABASE_URL environment variable set correctly in auth server - `intellistack/auth-server/.env` ✅ Verified

- [x] [T091] [P1] [US4] Verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET set in auth server - `intellistack/auth-server/.env` ✅ Verified

- [x] [T092] [P1] [US4] Verify DOCUSAURUS_URL environment variable set in Next.js - `intellistack/frontend/.env.local`, `.env.production` ✅ Verified

**Acceptance**: All environment variables configured correctly for development and production

---

## Integration Testing

- [ ] [T093] [P1] [ALL] End-to-end test: New user signup → onboarding (all 4 steps) → book content access - Manual test

- [ ] [T094] [P1] [ALL] End-to-end test: Existing user login → skip onboarding → book content access - Manual test

- [ ] [T095] [P1] [ALL] End-to-end test: Google OAuth signup → onboarding → book content access - Manual test

- [ ] [T096] [P1] [ALL] End-to-end test: Incomplete onboarding → logout → login → resume onboarding - Manual test

- [ ] [T097] [P1] [ALL] End-to-end test: Next.js "Book" button → Docusaurus → login → onboarding → content - Manual test

- [ ] [T098] [P1] [ALL] Test concurrent sessions on multiple devices work without conflicts - Manual test

- [ ] [T099] [P1] [ALL] Test session validation errors do not occur during normal usage - Manual test

- [ ] [T100] [P1] [ALL] Test redirect loop detection prevents infinite redirects - Manual test

**Acceptance**: All user flows work end-to-end without errors, edge cases handled correctly

---

## Documentation

- [ ] [T101] [P2] [ALL] Update README with new authentication flow documentation - `intellistack/README.md`

- [ ] [T102] [P2] [ALL] Document environment variables required for each service - `intellistack/docs/environment-setup.md`

- [ ] [T103] [P2] [ALL] Document onboarding data schema and validation rules - `intellistack/docs/onboarding-schema.md`

- [ ] [T104] [P2] [ALL] Create troubleshooting guide for common authentication issues - `intellistack/docs/troubleshooting.md`

**Acceptance**: Documentation complete and accurate for new authentication system

---

## Task Summary

**Total Tasks**: 104
**By Priority**:
- P1 (Critical): 88 tasks
- P2 (Important): 16 tasks

**By User Story**:
- US1 (Authentication & Onboarding): 45 tasks
- US2 (Next.js Simplification): 11 tasks
- US3 (Docusaurus Routing): 11 tasks
- US4 (Session & Database Integrity): 25 tasks
- ALL (Integration & Documentation): 12 tasks

**Estimated Time**: 8-12 hours total

---

## Dependencies

### Critical Path
1. Database migration (T001-T004) must complete before any authentication testing
2. Better Auth server configuration (T005-T014) must complete before Docusaurus client integration
3. Docusaurus auth client (T015-T017) must complete before auth pages and onboarding
4. Auth context (T018-T021) must complete before protected routes
5. Onboarding API endpoints (T009-T014) must complete before onboarding pages
6. All authentication infrastructure must complete before integration testing

### Parallel Work Streams
- **Stream 1**: Database + Auth Server (T001-T014) - Backend work
- **Stream 2**: Docusaurus Configuration (T057-T062) - Config work
- **Stream 3**: Next.js Simplification (T046-T056) - Frontend cleanup (can start anytime)

After Stream 1 completes:
- **Stream 4**: Docusaurus Auth Client + Context (T015-T021)
- **Stream 5**: Authentication Pages (T022-T026)
- **Stream 6**: Onboarding Pages (T027-T037)
- **Stream 7**: Protected Routes + Navbar (T038-T045)

After all streams complete:
- **Stream 8**: Integration Testing (T093-T100)
- **Stream 9**: Documentation (T101-T104)

---

## Notes

- All manual tests should be documented with screenshots and database query results
- Session validation should be tested thoroughly to prevent "session validation errors"
- OAuth testing requires valid Google OAuth credentials in environment variables
- Onboarding data schema should match the TypeScript interface defined in data-model.md
- Protected routes use client-side checks only (static site limitation)
- Database migration is idempotent and safe to run multiple times
