# Feature Specification: Docusaurus Authentication Migration & Onboarding

**Feature Branch**: `002-docusaurus-auth-migration`
**Created**: 2026-02-25
**Status**: Draft
**Input**: Migrate authentication from Next.js to Docusaurus with Better Auth, implement multi-step onboarding, fix routing issues, and simplify Next.js frontend

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Authentication & Onboarding (Priority: P1)

A new student visits the IntelliStack platform, clicks "Book" from the Next.js landing page, is redirected to Docusaurus without errors, sees clear Login/Signup options, authenticates using email/password or OAuth (Google), completes a 4-step onboarding form with validation, and is redirected to the main book content ready to start learning.

**Why this priority**: Authentication and onboarding are the gateway to the entire learning experience. Without a working auth flow, students cannot access any content. This is the most critical user journey that must work flawlessly.

**Independent Test**: Can be fully tested by creating a new user account, completing all 4 onboarding steps, and verifying database records are created and session persists. Delivers complete authentication value as a standalone experience.

**Acceptance Scenarios**:

1. **Given** a visitor on the Next.js landing page, **When** they click "Book" in the navigation, **Then** they are redirected to `http://localhost:3005/AINativeBook/` (Docusaurus) without seeing "Page Not Found" errors.

2. **Given** an unauthenticated user on Docusaurus, **When** they view the navigation bar, **Then** they see clearly visible "Login" and "Signup" buttons.

3. **Given** a new user on the Docusaurus signup page, **When** they enter valid email and password and submit, **Then** their account is created in the database and they are redirected to Step 1 of onboarding.

4. **Given** a user on Step 1 of onboarding (Basic Information), **When** they fill in name, preferred language, and timezone and click "Next", **Then** their data is validated and they advance to Step 2.

5. **Given** a user on Step 2 of onboarding (Educational Background), **When** they select education level, field of study, and prior experience and click "Next", **Then** their data is saved and they advance to Step 3.

6. **Given** a user on Step 3 of onboarding (Academic Interests), **When** they select learning goals, preferred learning style, and topics of interest and click "Next", **Then** their data is saved and they advance to Step 4.

7. **Given** a user on Step 4 of onboarding (Additional Details), **When** they provide optional information (GitHub profile, LinkedIn, bio) and click "Complete", **Then** their onboarding_completed flag is set to true and they are redirected to `/stage-1/intro`.

8. **Given** a user who has completed onboarding, **When** they return to Docusaurus, **Then** they are not shown the onboarding flow again and can access book content directly.

9. **Given** a user clicking "Login with Google", **When** they complete OAuth flow, **Then** their session is created, they are redirected to onboarding (if not completed) or book content (if completed).

10. **Given** an authenticated user, **When** they close their browser and return within 24 hours, **Then** their session persists and they remain logged in.

---

### User Story 2 - Simplified Next.js Navigation (Priority: P2)

A visitor on the Next.js landing page sees a clean, simplified navigation with only essential links (Login, Book, and static content), clicks "Login" and is redirected to Docusaurus authentication, or clicks "Book" and is redirected to Docusaurus content, without any authentication logic executing in Next.js.

**Why this priority**: Simplifying the Next.js frontend reduces complexity, eliminates duplicate authentication logic, and creates a clear separation of concerns. This improves maintainability and reduces potential bugs.

**Independent Test**: Can be tested by verifying Next.js navigation contains only specified links, clicking each link redirects correctly, and no authentication API calls are made from Next.js. Delivers simplified frontend independent of Docusaurus implementation.

**Acceptance Scenarios**:

1. **Given** a visitor on the Next.js landing page, **When** they view the navigation bar, **Then** they see only "Login", "Book", and static links (Home, Community, AI Tutor with "Coming Soon" badges).

2. **Given** a visitor on Next.js, **When** they click "Login" in the navigation, **Then** they are redirected to Docusaurus authentication page (`http://localhost:3005/AINativeBook/auth/login`).

3. **Given** a visitor on Next.js, **When** they click "Book" in the navigation, **Then** they are redirected to Docusaurus book content (`http://localhost:3005/AINativeBook/stage-1/intro`).

4. **Given** the Next.js codebase, **When** reviewing authentication-related code, **Then** no Better Auth client code, session management, or protected routes exist in Next.js.

5. **Given** a visitor on Next.js, **When** they interact with the page, **Then** no authentication API calls are made to the auth server from Next.js.

---

### User Story 3 - Docusaurus Routing & Deployment (Priority: P1)

The Docusaurus application is configured with correct baseUrl, routing, and deployment settings so that all internal links work correctly, external redirects from Next.js land on valid pages, and the application can be deployed to GitHub Pages without broken links.

**Why this priority**: Routing issues create a broken user experience and prevent users from accessing content. This must be fixed before any other Docusaurus features can work properly.

**Independent Test**: Can be tested by navigating to all Docusaurus routes, clicking internal links, testing external redirects, and verifying no 404 errors occur. Delivers working navigation independent of authentication.

**Acceptance Scenarios**:

1. **Given** Docusaurus is running locally, **When** a user navigates to `http://localhost:3005/AINativeBook/`, **Then** they see the Docusaurus homepage without 404 errors.

2. **Given** a user on any Docusaurus page, **When** they click internal navigation links (Stage 1, Stage 2, etc.), **Then** they navigate to the correct pages without 404 errors.

3. **Given** Docusaurus is deployed to GitHub Pages, **When** a user visits `https://saramali15792.github.io/AINativeBook/`, **Then** the site loads correctly with all assets and links working.

4. **Given** a user on Next.js, **When** they click "Book" and are redirected to Docusaurus, **Then** they land on a valid page (not 404) and can navigate the book.

5. **Given** Docusaurus configuration, **When** reviewing `docusaurus.config.ts`, **Then** baseUrl is set to `/AINativeBook/`, url is correct for environment, and routeBasePath is `/`.

---

### User Story 4 - Session & Database Integrity (Priority: P1)

Better Auth is properly connected to the PostgreSQL database, sessions are created and persisted correctly, OAuth providers (Google) function without errors, and all user data (authentication + onboarding) is securely stored and linked to the authenticated user.

**Why this priority**: Database and session integrity are foundational to the entire authentication system. Without proper persistence, users cannot maintain sessions or have their data saved.

**Independent Test**: Can be tested by creating accounts, logging in/out, checking database records, testing OAuth flows, and verifying session cookies. Delivers data persistence independent of UI implementation.

**Acceptance Scenarios**:

1. **Given** Better Auth is configured, **When** a user signs up, **Then** a record is created in the `users` table with correct fields (id, email, password_hash, name, email_verified, onboarding_completed, current_stage, role).

2. **Given** a user logs in, **When** authentication succeeds, **Then** a session record is created in the `sessions` table with valid token and expiration.

3. **Given** a user completes onboarding, **When** they submit Step 4, **Then** their preferences are stored in the `users.preferences` JSON field and `onboarding_completed` is set to true.

4. **Given** a user logs in with Google OAuth, **When** OAuth flow completes, **Then** a record is created in `oauth_accounts` table linking provider account to user.

5. **Given** an authenticated user, **When** they make requests to Docusaurus, **Then** their session cookie is sent and validated correctly without "session validation errors".

6. **Given** a user's session expires, **When** they try to access protected content, **Then** they are redirected to login page with appropriate message.

7. **Given** Better Auth configuration, **When** reviewing environment variables, **Then** DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, and OAuth credentials are correctly set.

---

### Edge Cases

- **Incomplete Onboarding**: What happens when a user closes the browser during onboarding?
  - System saves progress only at step completion (clicking "Next" or "Complete"). User resumes from last completed step on next login. Partial field data within an incomplete step is lost.

- **Duplicate Email Registration**: What happens when a user tries to sign up with an existing email?
  - System returns clear error message "Email already registered" and suggests login or password reset.

- **OAuth Account Linking**: What happens when a user signs up with email, then later tries to login with Google using the same email?
  - System automatically links OAuth account to existing user account if email matches and is verified.

- **Session Conflicts**: What happens when a user is logged in on multiple devices?
  - System allows multiple concurrent sessions; each device maintains its own session token.

- **Onboarding Data Validation Failure**: What happens when a user submits invalid data in onboarding steps?
  - System displays inline validation errors, prevents progression to next step, and highlights invalid fields.

- **Redirect Loop**: What happens if authentication redirect logic creates an infinite loop?
  - System implements redirect loop detection (max 3 redirects) and shows error page with manual navigation options.

- **Database Connection Failure**: What happens when Better Auth cannot connect to PostgreSQL?
  - System displays maintenance page, logs error, and prevents authentication attempts until connection is restored.

- **Expired OAuth Tokens**: What happens when a user's OAuth refresh token expires?
  - System prompts user to re-authenticate with OAuth provider; maintains user account but requires new OAuth consent.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Session Management (FR-001 to FR-010)

- **FR-001**: System MUST implement Better Auth within Docusaurus application with email/password and OAuth (Google) authentication methods.

- **FR-002**: System MUST create user records in PostgreSQL database with fields: id (string), email (unique), password_hash, name, email_verified (boolean), onboarding_completed (boolean), current_stage (integer 1-5), role (string, default "student"), preferences (JSON).

- **FR-003**: System MUST create and persist session tokens in database with 24-hour expiration and automatic refresh after 1 hour of activity.

- **FR-004**: System MUST set secure session cookies with appropriate SameSite and Secure flags based on environment (Lax for development, None for production). In production, Next.js and Docusaurus will be deployed on the same domain with different paths (e.g., intellistack.com and intellistack.com/AINativeBook), allowing cookies to be shared without cross-domain complications.

- **FR-005**: System MUST validate session tokens on every protected route request and return 401 Unauthorized if invalid or expired.

- **FR-006**: System MUST support Google OAuth with proper redirect URIs and callback handling.

- **FR-007**: System MUST link OAuth accounts to existing user accounts when email addresses match.

- **FR-008**: System MUST hash passwords using bcrypt or equivalent secure hashing algorithm before storing. Passwords must be at least 8 characters long with no additional complexity requirements (no mandatory uppercase, lowercase, numbers, or special characters).

- **FR-009**: System MUST implement CSRF protection for all authentication endpoints.

- **FR-010**: System MUST log all authentication events (login, logout, signup, OAuth) with timestamp, IP address, and user agent.

#### Onboarding Flow (FR-011 to FR-020)

- **FR-011**: System MUST redirect authenticated users with onboarding_completed=false to Step 1 of onboarding flow when attempting to access any book content routes (/stage-1/*, /stage-2/*, etc.). All book content requires completed onboarding.

- **FR-012**: System MUST display a 4-step onboarding form with clear step indicator showing current step (1 → 2 → 3 → 4). Onboarding is mandatory with no skip option; users must complete all 4 steps before accessing book content.

- **FR-013**: System MUST collect and validate the following data in Step 1 (Basic Information): full name (required), preferred language (required, dropdown: English/Urdu), timezone (required, dropdown).

- **FR-014**: System MUST collect and validate the following data in Step 2 (Educational Background): education level (required, dropdown: High School/Undergraduate/Graduate/Professional), field of study (required, text), prior robotics experience (required, radio: None/Beginner/Intermediate/Advanced).

- **FR-015**: System MUST collect and validate the following data in Step 3 (Academic Interests): learning goals (required, multi-select checkboxes: Career Change/Academic Research/Hobby/Professional Development), preferred learning style (required, radio: Visual/Reading/Hands-on/Mixed), topics of interest (required, multi-select checkboxes: ROS 2/Simulation/Perception/AI Integration/Hardware).

- **FR-016**: System MUST collect optional data in Step 4 (Additional Details): GitHub username (optional, text), LinkedIn profile URL (optional, URL), bio (optional, textarea max 500 chars).

- **FR-017**: System MUST validate each step's data before allowing progression to next step, displaying inline error messages for invalid fields.

- **FR-018**: System MUST save onboarding data to users.preferences JSON field after each step completion (when user clicks "Next" or "Complete"). Partial progress within a step is not persisted; users who close the browser mid-step will lose unsaved field data for that step.

- **FR-019**: System MUST set onboarding_completed=true and redirect user to /stage-1/intro after Step 4 completion.

- **FR-020**: System MUST allow users to navigate backward through onboarding steps to edit previous answers before final submission.

#### Docusaurus Routing & Configuration (FR-021 to FR-028)

- **FR-021**: System MUST configure Docusaurus with baseUrl='/AINativeBook/' for GitHub Pages deployment.

- **FR-022**: System MUST configure Docusaurus with routeBasePath='/' so docs are served at root of baseUrl.

- **FR-023**: System MUST configure Docusaurus with correct url based on environment: 'http://localhost:3005' for development, 'https://saramali15792.github.io' for production.

- **FR-024**: System MUST handle trailing slashes consistently (trailingSlash: false) to prevent duplicate URLs.

- **FR-025**: System MUST configure custom navbar items including Login/Signup buttons (when unauthenticated) or User Menu (when authenticated).

- **FR-026**: System MUST serve authentication pages at /auth/login and /auth/signup within Docusaurus.

- **FR-027**: System MUST serve onboarding pages at /onboarding/step-1, /onboarding/step-2, /onboarding/step-3, /onboarding/step-4 within Docusaurus.

- **FR-028**: System MUST configure webpack aliases and module resolution to support Better Auth client imports in Docusaurus.

#### Next.js Simplification (FR-029 to FR-035)

- **FR-029**: System MUST remove all Better Auth client code from Next.js frontend (lib/auth.ts, contexts/AuthContext.tsx, auth pages).

- **FR-030**: System MUST remove authentication-related components from Next.js (UserMenu, ProtectedRoute, auth forms).

- **FR-031**: System MUST update Next.js Header component to show only: Login (link to Docusaurus), Book (link to Docusaurus), Home, Community (Coming Soon), AI Tutor (Coming Soon).

- **FR-032**: System MUST configure "Login" link to redirect to `${DOCUSAURUS_URL}/auth/login`.

- **FR-033**: System MUST configure "Book" link to redirect to `${DOCUSAURUS_URL}/stage-1/intro`.

- **FR-034**: System MUST remove all authentication middleware from Next.js (middleware.ts).

- **FR-035**: System MUST remove all authentication API routes from Next.js (app/api/auth/*).

#### Database Schema (FR-036 to FR-040)

- **FR-036**: System MUST ensure users table has columns: id (string PK), email (string unique), password_hash (string), name (string), email_verified (boolean default false), onboarding_completed (boolean default false), current_stage (integer default 1), role (string default 'student'), preferences (JSON nullable), created_at (timestamp), updated_at (timestamp).

- **FR-037**: System MUST ensure sessions table has columns: id (string PK), user_id (string FK to users.id), token (string indexed), expires_at (timestamp), created_at (timestamp), revoked_at (timestamp nullable).

- **FR-038**: System MUST ensure oauth_accounts table has columns: id (string PK), user_id (string FK to users.id), provider (string), provider_account_id (string), access_token (text), refresh_token (text), expires_at (timestamp), created_at (timestamp).

- **FR-039**: System MUST create database indexes on: users.email, sessions.token, sessions.user_id, oauth_accounts.user_id, oauth_accounts.provider.

- **FR-040**: System MUST create Alembic migration to add missing columns (email_verified, onboarding_completed, current_stage, role, preferences) to existing users table if they don't exist.

### Key Entities

- **User**: Represents a platform user with authentication credentials, profile information, onboarding status, and learning progress. Key attributes: id, email, name, email_verified, onboarding_completed, current_stage, role, preferences (JSON containing onboarding responses).

- **Session**: Represents an authenticated user session with token, expiration, and device information. Key attributes: id, user_id, token, expires_at, user_agent, ip_address, revoked_at.

- **OAuth Account**: Represents a linked social authentication provider account. Key attributes: id, user_id, provider (google/github), provider_account_id, access_token, refresh_token, expires_at.

- **Onboarding Data**: Stored in users.preferences JSON field, contains: basic_info (name, language, timezone), education (level, field, experience), interests (goals, learning_style, topics), additional (github, linkedin, bio).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can navigate from Next.js to Docusaurus without encountering 404 errors or broken links (100% success rate).

- **SC-002**: Users can complete the full authentication flow (signup or login) and reach the onboarding form within 30 seconds.

- **SC-003**: Users can complete all 4 onboarding steps with validation feedback and reach book content within 3 minutes.

- **SC-004**: Authenticated user sessions persist for 24 hours without requiring re-authentication (unless explicitly logged out).

- **SC-005**: OAuth (Google) authentication completes successfully with proper account linking and session creation (95%+ success rate).

- **SC-006**: Database records are created correctly for all authentication and onboarding events (100% data integrity).

- **SC-007**: Next.js frontend contains zero authentication-related code (verified by code review and absence of auth API calls).

- **SC-008**: Docusaurus navigation displays Login/Signup buttons for unauthenticated users and User Menu for authenticated users (100% visibility).

- **SC-009**: Onboarding step indicator clearly shows current step and progress (verified by user testing with 90%+ comprehension rate).

- **SC-010**: System handles concurrent sessions across multiple devices without conflicts or data loss (tested with 10+ concurrent sessions per user).

---

## Clarifications

### Session 2026-02-25

- Q: Should the system save onboarding progress after each step is completed, or should it also auto-save partial progress within a step (e.g., user fills some fields but doesn't click "Next")? → A: Save only on step completion (clicking "Next" or "Complete") - user loses in-progress data if they close browser mid-step
- Q: Should all book content routes be protected and require completed onboarding, or should some introductory content be accessible to authenticated users who haven't completed onboarding yet? → A: All book content requires completed onboarding - any attempt to access /stage-* routes redirects to onboarding if incomplete
- Q: In production, will Next.js and Docusaurus be on the same domain or different domains/subdomains? → A: Same domain with different paths (e.g., intellistack.com for Next.js, intellistack.com/AINativeBook for Docusaurus)
- Q: Should users be able to skip/exit the onboarding flow and access book content without completing it, or must they complete all 4 steps before accessing any content? → A: Onboarding is mandatory, no skip option - users must complete all 4 steps before accessing book content
- Q: Should passwords require complexity rules (uppercase, lowercase, numbers, special characters), or is a minimum length sufficient? → A: Minimum 8 characters, no complexity requirements - balances security with user experience

---

## Assumptions *(optional)*

- Better Auth server is already running and accessible at configured URL (http://localhost:3001 for development).
- PostgreSQL database is already provisioned and accessible with correct credentials.
- Docusaurus is already set up with basic configuration and content structure.
- Next.js frontend is already deployed and accessible.
- OAuth credentials (Google Client ID/Secret) are already obtained and configured in environment variables.
- Users have modern browsers with JavaScript enabled and cookies allowed.
- Network connectivity is stable for OAuth redirects and API calls.
- Email verification is disabled for development (requireEmailVerification: false in Better Auth config).

---

## Dependencies *(optional)*

- **Better Auth Server**: Must be running and healthy before Docusaurus authentication can function.
- **PostgreSQL Database**: Must be accessible and have correct schema before user registration can work.
- **Docusaurus Build**: Must complete successfully before deployment to GitHub Pages.
- **Environment Variables**: Must be correctly configured in all environments (development, production) for auth URLs, database connections, and OAuth credentials.
- **Alembic Migrations**: Must be run to add missing user table columns before onboarding data can be saved.

---

## Out of Scope *(optional)*

- Email verification flow (disabled for development, can be added later).
- Password reset functionality (existing implementation in auth server, not modified).
- Multi-factor authentication (MFA).
- Social login providers beyond Google (GitHub OAuth exists but not prioritized).
- Admin panel for managing users.
- Analytics tracking for authentication events.
- Rate limiting for authentication endpoints (handled by auth server).
- Internationalization (i18n) for authentication pages (English only initially).
- Mobile-responsive onboarding UI optimization (basic responsiveness only).
- Accessibility (a11y) audit for authentication and onboarding flows.

---

## Notes *(optional)*

- This migration consolidates authentication into a single location (Docusaurus), reducing code duplication and maintenance burden.
- The 4-step onboarding flow collects data needed for personalization features (Phase 10 in project roadmap).
- Onboarding data is stored in a flexible JSON field to allow easy addition of new questions without schema changes.
- The simplified Next.js frontend becomes a pure marketing/landing page with no authentication logic.
- Session management uses Better Auth's built-in session handling with database persistence for reliability.
- OAuth account linking allows users to authenticate with multiple providers while maintaining a single user account.
- The routing fix addresses a known issue where baseUrl and routeBasePath were misconfigured, causing 404 errors on redirects.
