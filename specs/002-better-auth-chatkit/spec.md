# Feature Specification: Better-Auth OIDC Server + ChatKit AI Tutor

**Feature Branch**: `002-better-auth-chatkit`
**Created**: 2026-02-11
**Status**: Draft
**Input**: User description: "Create Better-Auth in existing project with ChatKit integration for AI tutor"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Email/Password Registration and Login (Priority: P1)

A new student visits IntelliStack, creates an account with email and password, and gains access to the learning platform. Returning students sign in with their credentials and resume their learning journey. The auth system provides a secure, seamless experience with email verification and session persistence across browser sessions.

**Why this priority**: Authentication is the foundation — no other feature works without users being able to create accounts and sign in. This is the minimum viable auth system.

**Independent Test**: Can be fully tested by registering a new account, verifying email, logging in, refreshing the page (session persists), and logging out. Delivers secure user identity for the entire platform.

**Acceptance Scenarios**:

1. **Given** a visitor on the registration page, **When** they submit valid name, email, and password (meeting strength requirements), **Then** an account is created and a verification email is sent.
2. **Given** a user with a verified email, **When** they enter correct credentials on the login page, **Then** they are authenticated and redirected to the dashboard with a valid session.
3. **Given** a logged-in user who closes and reopens the browser, **When** the session has not expired, **Then** they remain authenticated without re-entering credentials.
4. **Given** a user who enters incorrect credentials 5 times, **When** they attempt a 6th login, **Then** the account is temporarily locked for 30 minutes with a clear message shown.
5. **Given** a logged-in user, **When** they click sign out, **Then** the session is invalidated and they are redirected to the landing page.

---

### User Story 2 - OAuth Social Login (Priority: P1)

Students and instructors can sign in using their existing Google or GitHub accounts, reducing friction for onboarding. First-time OAuth users automatically get an IntelliStack account linked to their social profile. Returning OAuth users are recognized and signed in immediately.

**Why this priority**: Social login significantly reduces signup friction — critical for a learning platform where users want to start learning immediately, not fill out forms.

**Independent Test**: Can be tested by clicking "Sign in with Google," completing the Google consent flow, and verifying the user arrives at the dashboard with their profile populated from Google.

**Acceptance Scenarios**:

1. **Given** a visitor on the login page, **When** they click "Sign in with Google," **Then** they are redirected to Google's OAuth consent screen.
2. **Given** a first-time Google user completing OAuth, **When** the callback is processed, **Then** a new IntelliStack account is created with their Google profile data (name, email, avatar) and they are signed in.
3. **Given** a returning Google user, **When** they complete OAuth, **Then** they are signed in to their existing IntelliStack account.
4. **Given** a user who registered with email, **When** they later sign in with Google using the same email, **Then** the Google account is linked to their existing profile (account merging).
5. **Given** a user on the login page, **When** they click "Sign in with GitHub," **Then** the same flow works identically via GitHub OAuth.

---

### User Story 3 - AI Tutor Chat with Context Awareness (Priority: P2)

While studying a lesson on ROS 2 topics, a student has a question about publisher-subscriber patterns. They highlight a confusing code snippet, click "Ask AI," and an AI tutor chatbot opens with their question pre-filled alongside the lesson context. The AI tutor gives a Socratic-style response, asking guiding questions rather than giving direct answers, helping the student reason through the problem.

**Why this priority**: The AI tutor is the primary differentiator of IntelliStack — it transforms passive content into an interactive learning experience. Depends on auth (Story 1) for user identity.

**Independent Test**: Can be tested by navigating to any lesson page, selecting text, clicking "Ask AI," and verifying the chatbot opens with context from the current lesson and provides a relevant, educational response.

**Acceptance Scenarios**:

1. **Given** a logged-in student viewing a lesson, **When** they open the AI tutor chat widget, **Then** the chatbot loads with knowledge of the current lesson topic and the student's learning stage.
2. **Given** a student who selects text on a lesson page, **When** they click the "Ask about this" button, **Then** the chat opens with the selected text quoted and the AI provides a contextual explanation.
3. **Given** a student chatting with the AI tutor, **When** they ask a question, **Then** the AI responds using a Socratic teaching method — asking guiding questions before providing answers.
4. **Given** a student who has chatted with the AI tutor before, **When** they return to the chat, **Then** their previous conversation history is preserved and accessible.
5. **Given** a student viewing a Stage 3 lesson, **When** the AI tutor searches for supporting content, **Then** it only references materials from stages the student has unlocked (stage-based access control).

---

### User Story 4 - Conversation Persistence and History (Priority: P2)

A student starts a conversation about inverse kinematics on Monday. On Wednesday, they return to continue the same thread. The AI tutor remembers the previous context and can build on earlier explanations. Students can also start new threads for different topics, keeping their learning conversations organized.

**Why this priority**: Persistent conversations are essential for meaningful learning — students need to build on previous discussions, not restart every session.

**Independent Test**: Can be tested by creating a conversation, closing the browser, returning later, and verifying the conversation loads with full history intact.

**Acceptance Scenarios**:

1. **Given** a student who had a conversation yesterday, **When** they open the AI tutor today, **Then** they see their previous threads listed with timestamps.
2. **Given** a student viewing their thread list, **When** they click on a previous thread, **Then** the full conversation history loads with all messages visible.
3. **Given** a student in an active conversation, **When** they click "New Thread," **Then** a fresh conversation starts without losing the previous thread.
4. **Given** a student with multiple threads, **When** they view the thread list, **Then** threads are ordered by most recent activity and each shows a summary/title.

---

### User Story 5 - Password Recovery (Priority: P3)

A student forgets their password and needs to regain access to their account. They request a password reset link via email, receive it, and set a new password. The reset token expires after a limited time for security.

**Why this priority**: Password recovery is important for user retention but less urgent than core auth and the AI tutor experience.

**Independent Test**: Can be tested by requesting a reset from the forgot-password page, checking email for the link, clicking it, setting a new password, and verifying login works with the new password.

**Acceptance Scenarios**:

1. **Given** a user on the forgot-password page, **When** they enter their registered email, **Then** a password reset email is sent with a secure, time-limited link.
2. **Given** a user with a valid reset link, **When** they click the link and enter a new password meeting strength requirements, **Then** their password is updated and they can log in with the new password.
3. **Given** a reset link older than 1 hour, **When** a user clicks it, **Then** they see a clear message that the link has expired with an option to request a new one.
4. **Given** a user who enters a non-registered email on the forgot-password page, **When** they submit, **Then** they see the same "check your email" message (no email enumeration).

---

### User Story 6 - Role-Based Access Control (Priority: P3)

An admin user can manage platform roles — assigning instructor or admin privileges to users. Instructors can create and manage content. Students have access to learning materials based on their stage progression. The system enforces these permissions across both the auth server and the data API.

**Why this priority**: RBAC is necessary for a multi-role platform but can initially use simple role checks before building a full admin UI.

**Independent Test**: Can be tested by logging in as an admin, assigning the instructor role to a user, and verifying the user gains access to content creation features.

**Acceptance Scenarios**:

1. **Given** an admin user, **When** they assign the "instructor" role to a student, **Then** the student gains access to content creation tools on their next page load.
2. **Given** an instructor, **When** they attempt to access admin-only features (e.g., user management), **Then** they are denied with a clear permission error.
3. **Given** a student, **When** they attempt to access instructor content creation routes, **Then** they are redirected to the learning dashboard.
4. **Given** a user's role change, **When** they are currently logged in, **Then** the role change takes effect within their current session (no re-login required).

---

### Edge Cases

- What happens when the auth server (Node.js) is down but the FastAPI backend is up? → The frontend shows a degraded state with a "login unavailable" message; already-authenticated users with valid tokens can continue using the platform.
- What happens when a user tries to sign in with Google using an email that exists but was registered with email/password? → Accounts are linked automatically if the email is verified on both sides.
- What happens when the ChatKit backend can't reach the vector store (Qdrant)? → The AI tutor responds using its base knowledge without RAG augmentation, with a notice that search results may be limited.
- What happens when a student loses connection mid-conversation? → Messages are saved server-side; when connection resumes, the conversation continues from where it left off.
- What happens when the JWKS endpoint is unreachable from the FastAPI resource server? → FastAPI caches the last known valid JWKS keys and serves requests using cached keys, logging a warning. If no cached keys exist, auth-dependent requests return a 503 with a retry-after header.

## Requirements *(mandatory)*

### Functional Requirements

**Authentication Core (Better-Auth Server)**

- **FR-001**: System MUST provide email/password registration with configurable password strength requirements (minimum 12 characters, uppercase, lowercase, number, special character).
- **FR-002**: System MUST verify user email addresses before granting full platform access. Unverified users MAY browse the dashboard and view course listings but MUST NOT access lesson content or the AI tutor until email is verified.
- **FR-003**: System MUST support OAuth 2.1 login via Google and GitHub identity providers.
- **FR-004**: System MUST issue JWT access tokens (signed with RS256 via JWKS) and refresh tokens upon successful authentication.
- **FR-005**: System MUST expose a JWKS endpoint for downstream services to verify tokens without calling the auth server.
- **FR-006**: System MUST implement PKCE (Proof Key for Code Exchange) for all public client authorization flows.
- **FR-007**: System MUST support account lockout after 5 consecutive failed login attempts with a 30-minute cooldown period.
- **FR-008**: System MUST provide a password reset flow with time-limited tokens (1 hour expiry) delivered via email.
- **FR-009**: System MUST support role assignment (student, instructor, admin) with role claims included in JWT tokens.
- **FR-010**: System MUST expose an OIDC discovery endpoint (`/.well-known/openid-configuration`) describing all available endpoints and capabilities.

**Token & Session Management**

- **FR-011**: Access tokens MUST expire after 6 hours. Refresh tokens MUST expire after 7 days.
- **FR-012**: System MUST support silent token refresh — the frontend MUST automatically refresh expired access tokens using refresh tokens without user interaction.
- **FR-013**: System MUST support single sign-out — signing out clears client tokens; the auth server session remains active for SSO across future apps.

**ChatKit AI Tutor**

- **FR-014**: System MUST provide a chat widget accessible from any lesson page, rendered only after the required external script has loaded.
- **FR-015**: System MUST inject authenticated user identity into every chat request via a custom fetch interceptor (user ID, name, email, role).
- **FR-016**: System MUST inject current page context into every chat request (URL, title, headings, lesson stage).
- **FR-017**: System MUST support text selection — users MUST be able to highlight text on a page and send it as a chat query with context.
- **FR-018**: System MUST persist conversations per user in the database, organized as threads with timestamp-ordered messages. Threads MUST be retained while the student is actively enrolled; threads MUST be automatically deleted 30 days after the student completes or leaves the associated course.
- **FR-019**: System MUST load and display conversation history when a user returns to a previous thread.
- **FR-020**: System MUST enforce stage-based access control — the AI tutor's RAG search MUST only retrieve content from stages the student has unlocked.
- **FR-021**: System MUST stream AI responses in real-time (server-sent events) rather than waiting for complete generation.
- **FR-027**: System MUST enforce a rate limit of 20 AI tutor messages per student per 24-hour rolling window. When the limit is reached, the system MUST display a clear "daily limit reached" message with the time until the limit resets. Instructors and admins are exempt from this limit.

**Observability**

- **FR-028**: System MUST log all authentication events: successful logins, failed login attempts (with reason), registrations, logouts, password resets, and OAuth link/unlink operations. Each log entry MUST include timestamp, user identifier (or attempted email), IP address, and event type.
- **FR-029**: System MUST track AI tutor usage metrics per user: message count per day, average response time, and error rate. These metrics MUST be queryable for cost monitoring and usage analysis.

**Integration (Auth + ChatKit + Existing Platform)**

- **FR-022**: The FastAPI backend MUST validate Better-Auth JWT tokens using JWKS public key verification (no direct calls to the auth server per request).
- **FR-023**: The Next.js frontend MUST use the official Better-Auth client library (`@better-auth/react`) for auth operations.
- **FR-024**: The ChatKit server MUST authenticate requests using the same JWT tokens issued by Better-Auth.
- **FR-025**: System MUST migrate existing user data from the current custom auth tables to Better-Auth's schema without data loss. Migration strategy is big bang cutover: a one-time migration script runs, the system switches entirely to Better-Auth, and old auth code is removed. All existing users MUST be able to log in after migration without re-registering.
- **FR-026**: System MUST support email sending for verification and password reset via configurable providers (SMTP or Resend API).

### Key Entities

- **User**: A person with an account on the platform. Has name, email, avatar, role (student/instructor/admin), email verification status, and learning stage. Can have multiple linked OAuth accounts.
- **Session**: An active authentication session tracking the user's login state. Contains user reference, creation time, expiry, and device/IP metadata.
- **OAuth Account**: A link between a user and an external identity provider (Google, GitHub). Contains provider name, provider account ID, and token data.
- **OAuth Application**: A registered client application authorized to use the auth server. Contains client ID, type (public/confidential), redirect URIs, and trust configuration.
- **Thread**: A conversation between a user and the AI tutor. Contains a title, creation timestamp, last activity timestamp, associated course reference, and belongs to one user. Retention: kept while enrolled, deleted 30 days after course completion or departure.
- **Message**: A single message within a thread. Contains role (user/assistant), content text, timestamp, and optional metadata (page context, selected text).
- **Password Reset Token**: A time-limited token for password recovery. Contains token hash, user reference, creation time, expiry, and used status.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration (email/password) and reach the dashboard in under 60 seconds, including email verification.
- **SC-002**: OAuth login (Google/GitHub) completes in under 10 seconds from button click to dashboard arrival.
- **SC-003**: 95% of authenticated page loads validate the user's session without any user-perceptible delay.
- **SC-004**: The AI tutor chat widget loads and is interactive within 3 seconds of a lesson page loading.
- **SC-005**: AI tutor responses begin streaming to the user within 2 seconds of submitting a question.
- **SC-006**: Conversation history loads completely within 1 second when a user opens a previous thread.
- **SC-007**: System supports 500 concurrent authenticated users without service degradation.
- **SC-008**: Zero user data is lost during migration from the existing auth system to Better-Auth.
- **SC-009**: 90% of users who start the password reset flow successfully set a new password and log in.
- **SC-010**: The text selection "Ask AI" feature works on all lesson content areas across desktop browsers.

## Clarifications

### Session 2026-02-11

- Q: What can unverified email users do on the platform? → A: Limited access — can browse dashboard and course listings, but cannot open lessons or use the AI tutor.
- Q: How should the migration from old auth to Better-Auth happen? → A: Big bang cutover — one-time migration script, switch entirely to Better-Auth, remove old auth code.
- Q: How long should AI tutor conversation threads be kept? → A: Until course completion — threads kept while enrolled, deleted 30 days after completing or leaving the course.
- Q: Should the AI tutor have a rate limit per student? → A: 20 messages per day per student; "daily limit reached" message shown when exhausted; instructors and admins exempt.
- Q: Should the system log auth and AI tutor events for monitoring? → A: Log all auth events (login/logout/registration/failures) and AI tutor usage metrics (message counts, response times per user).

## Scope & Boundaries

### In Scope

- Standalone Better-Auth Node.js server with OIDC Provider, PKCE, JWKS, admin plugin
- OAuth 2.1 flows for Google and GitHub
- Email/password auth with verification and password reset
- ChatKit server integration (Python, extends existing FastAPI RAG infrastructure)
- ChatKit frontend widget (React, integrated into Next.js lesson pages)
- JWKS-based token verification in FastAPI (replacing current cookie-based JWT)
- Data migration script from current auth tables to Better-Auth schema
- Role-based access control (student, instructor, admin)

### Out of Scope

- Mobile app authentication (web-only for this feature)
- Multi-factor authentication (MFA) — can be added later via Better-Auth plugin
- Third-party developer OAuth client registration (first-party only)
- AI tutor training/fine-tuning (uses existing OpenAI + RAG infrastructure)
- Payment/billing integration
- Admin UI for user management (API-only for now, UI in a later phase)

## Assumptions

- PostgreSQL (Neon) is the database for both Better-Auth and ChatKit persistence
- The existing Qdrant vector store and RAG pipeline remain unchanged
- OpenAI API is used for AI tutor responses (via existing LangChain/LangGraph setup)
- Email delivery will be configured via SMTP (Gmail) or Resend API
- The Better-Auth server will run as a separate Docker container alongside the FastAPI backend
- The ChatKit Python server will be integrated into the existing FastAPI process (not a separate service)
- Existing frontend auth pages (login, register, forgot-password, reset-password) will be refactored to use the Better-Auth client library

## Dependencies

- **Better-Auth npm package** (`better-auth`) — Node.js auth server
- **@better-auth/react** — Frontend auth hooks
- **OpenAI ChatKit** (`@openai/chatkit`) — Frontend chat widget
- **chatkit Python package** — Backend ChatKit server
- **Existing Qdrant + RAG pipeline** — Content retrieval for AI tutor
- **PostgreSQL (Neon)** — Database for auth and conversation storage
- **Google Cloud Console** — OAuth 2.0 client credentials
- **GitHub Developer Settings** — OAuth app credentials
- **SMTP provider or Resend API** — Email delivery

## Risks

- **Migration risk**: Big bang cutover means all users switch at once — if migration has issues, all logins are affected. Mitigation: run migration on a staging database first, validate all user accounts can authenticate, create a database backup before production migration, and prepare a rollback script.
- **Service coupling**: Adding a separate Node.js auth server increases operational complexity. Mitigation: containerize with Docker Compose, health checks, and shared database.
- **ChatKit dependency**: OpenAI ChatKit is a relatively new framework and may have breaking changes. Mitigation: pin versions, abstract the ChatKit integration behind an interface.
