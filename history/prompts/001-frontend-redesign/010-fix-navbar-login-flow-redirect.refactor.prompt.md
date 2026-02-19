---
id: "010"
title: Fix Navbar Visibility, Login Flow & Docusaurus Redirect
stage: refactor
date: 2026-02-18
surface: agent
model: claude-opus-4-6
feature: 001-frontend-redesign
branch: 001-frontend-redesign
user: saram
command: implement plan
labels: ["navbar", "login-flow", "redirect", "header", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/app/page.tsx
  - intellistack/frontend/src/components/layout/Header.tsx
  - intellistack/frontend/src/components/auth/LoginForm.tsx
  - intellistack/content/src/pages/login.tsx
  - intellistack/content/src/pages/register.tsx
tests:
  - Manual verification: navbar visible on landing page with correct nav items
  - Manual verification: login redirect flow for first-time vs returning users
  - Manual verification: Docusaurus login redirects to docs content
---

## Prompt

Implement the plan to fix navbar visibility, login flow, and Docusaurus redirect. Three issues: (1) Navbar not visible on landing page, (2) Login always redirects to onboarding, (3) After login should show Docusaurus book.

## Response snapshot

Implemented 5 changes across Next.js frontend and Docusaurus content:

1. **Added Header to landing page** (`page.tsx`) — Imported and added `<Header transparent />` at top of the page component so the navbar is visible overlaying the hero section.

2. **Updated Header nav links** (`Header.tsx`) — Changed `navLinks` to include: Home, Books (external link to Docusaurus), Personalize, Community (Soon badge), AI Tutor (Soon badge). Added `badge` and `external` properties to nav link type. Updated both desktop and mobile menu rendering to support badges (gradient pill) and external links (using `<a>` instead of Next.js `<Link>`).

3. **Fixed LoginForm redirect** (`LoginForm.tsx`) — Replaced `router.push('/')` with a `useEffect` that watches `session.isAuthenticated`. Uses a `justLoggedIn` ref to distinguish between initial mount and actual login. First-time users (no preferences) go to `/personalization`, returning users go to Docusaurus URL via `window.location.href`.

4. **Fixed Docusaurus login** (`login.tsx`) — Removed the `onboardingCompleted` check and `/onboarding` redirect. After email login, redirects to `/docs/stage-1/intro`. Changed OAuth `callbackURL` from `/onboarding` to `/docs/stage-1/intro`.

5. **Fixed Docusaurus register** (`register.tsx`) — Changed OAuth `callbackURL` from `/onboarding` to `/docs/stage-1/intro`.

## Outcome

- ✅ Impact: Navbar now visible on landing page; login flow correctly routes first-time vs returning users; Docusaurus login no longer redirects to non-existent /onboarding page
- 🧪 Tests: Manual verification required — start both frontends and test login flows
- 📁 Files: 5 files modified
- 🔁 Next prompts: Test the full flow end-to-end; consider adding scroll-based header background opacity transition
- 🧠 Reflection: The stale state issue in LoginForm was the trickiest part — useEffect with a ref flag is a clean pattern for reacting to async state updates after an imperative action

## Evaluation notes (flywheel)

- Failure modes observed: Original LoginForm read stale session state within onSubmit; Docusaurus checked non-existent onboardingCompleted session field
- Graders run and results (PASS/FAIL): N/A - manual testing needed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add header background opacity transition on scroll for the transparent landing page header
