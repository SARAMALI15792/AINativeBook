---
id: 003
title: Docusaurus Better-Auth + ChatKit Full Integration
stage: implementation
date: 2026-02-14
surface: agent
model: claude-opus-4-6
feature: 002-better-auth-chatkit
branch: 002-better-auth-chatkit
user: saram
command: implement plan
labels: ["docusaurus", "better-auth", "chatkit", "onboarding", "ai-tutor"]
links:
  spec: specs/002-better-auth-chatkit/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/lib/auth-client.ts
  - intellistack/content/src/clientModules/authInit.ts
  - intellistack/content/src/theme/NavbarItem/ComponentTypes.tsx
  - intellistack/content/src/theme/NavbarItem/AuthNavbarItem.tsx
  - intellistack/content/src/theme/NavbarItem/AuthNavbarItem.module.css
  - intellistack/content/src/pages/login.tsx
  - intellistack/content/src/pages/register.tsx
  - intellistack/content/src/pages/forgot-password.tsx
  - intellistack/content/src/pages/reset-password.tsx
  - intellistack/content/src/pages/profile.tsx
  - intellistack/content/src/pages/settings.tsx
  - intellistack/content/src/pages/auth.module.css
  - intellistack/content/src/pages/onboarding/index.tsx
  - intellistack/content/src/pages/onboarding/onboarding.module.css
  - intellistack/content/src/components/ai/ChatKitWidget.tsx
  - intellistack/content/src/components/ai/ChatKitWidget.module.css
  - intellistack/content/src/components/ai/index.ts
  - intellistack/content/src/theme/DocPage/Layout/index.tsx
  - intellistack/content/docusaurus.config.ts
  - intellistack/content/package.json
  - intellistack/content/src/css/custom.css
  - intellistack/content/.env.example
  - intellistack/backend/src/ai/chatkit/store.py
  - intellistack/backend/src/ai/chatkit/context.py
  - intellistack/backend/src/ai/chatkit/rate_limiter.py
  - intellistack/backend/src/ai/chatkit/agent.py
  - intellistack/backend/src/ai/chatkit/server.py
  - intellistack/backend/src/ai/chatkit/routes.py
  - intellistack/backend/src/ai/chatkit/models.py
  - intellistack/backend/src/ai/chatkit/__init__.py
  - intellistack/backend/src/core/users/__init__.py
  - intellistack/backend/src/core/users/schemas.py
  - intellistack/backend/src/core/users/routes.py
  - intellistack/backend/src/core/auth/models.py
  - intellistack/backend/src/main.py
tests:
  - Manual verification required: auth flow, onboarding, chatkit streaming
---

## Prompt

Implement the following plan: Better-Auth + ChatKit Integration for Docusaurus

The plan includes:
1. Docusaurus Auth Setup (auth client, navbar button, customFields)
2. Multi-Step Onboarding Flow (login, register, 4-step wizard)
3. Theme Swizzle (navbar auth item, DocPage layout wrapper)
4. ChatKit Backend (store, context, rate limiter, agent, server, routes)
5. ChatKit Frontend Widget (floating chat, text selection, thread management)
6. Integration & Polish (user routes, settings page, environment config)

## Response snapshot

Successfully implemented all 6 phases of the Better-Auth + ChatKit integration for the Docusaurus book platform:

### Phase 1: Docusaurus Auth Setup
- Created `auth-client.ts` with Better-Auth React client
- Updated `docusaurus.config.ts` with customFields (betterAuthUrl, backendUrl)
- Added clientModules for auth initialization

### Phase 2: Multi-Step Onboarding
- Login page with email/password and OAuth (Google, GitHub)
- Registration with password strength meter (12+ chars, complexity requirements)
- Forgot/reset password flow with token expiry
- 4-step onboarding wizard: System → Learning → Background → Complete
- Collects: theme, OS, IDE, shell, learning style, pace, goals, experience levels

### Phase 3: Navbar Auth Integration
- Swizzled NavbarItem with custom AuthNavbarItem component
- Shows Sign In button or user dropdown with avatar
- Premium styling with dropdown menu (Profile, Settings, Sign Out)

### Phase 4: ChatKit Backend
- `PostgresChatKitStore`: Thread and message persistence
- `RequestContext`: User identity and page context
- `RateLimiter`: 20 msg/day for students, unlimited for instructors/admins
- `SocraticTutorAgent`: AI tutor with Socratic methodology
- `IntelliStackChatKitServer`: SSE streaming with rate limit handling
- FastAPI routes: `/api/v1/chatkit/*` endpoints

### Phase 5: ChatKit Frontend Widget
- Floating chat button (bottom-right)
- Text selection popup ("Ask AI")
- Thread management sidebar
- SSE streaming with typing indicator
- Rate limit display and error handling
- Welcome state with suggestions

### Phase 6: Integration & Polish
- User routes for profile and onboarding data
- Settings page with theme toggle and notifications
- Environment example files
- Updated User model with preferences fields
- Mounted all routers in main.py

## Outcome

- ✅ Impact: Complete auth and AI tutor integration for Docusaurus platform
- 🧪 Tests: Manual verification required - npm run build, auth flow, chat streaming
- 📁 Files: 35 files created/modified across frontend and backend
- 🔁 Next prompts: Run npm install, test auth flow, verify ChatKit streaming
- 🧠 Reflection: Large multi-phase implementation; all components interconnected

## Evaluation notes (flywheel)

- Failure modes observed: None during implementation
- Graders run and results (PASS/FAIL): Manual verification needed
- Prompt variant (if applicable): Full plan implementation
- Next experiment (smallest change to try): Test with npm run build && npm run start
