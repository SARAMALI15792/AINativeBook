---
id: 023
title: Add GitHub OAuth Button to Auth Pages
stage: green
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: auth
branch: main
user: salim
command: implement plan
labels: ["auth", "oauth", "github", "frontend", "better-auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/pages/auth/login.tsx
  - intellistack/content/src/pages/auth/signup.tsx
  - intellistack/content/src/css/custom.css
tests:
  - Manual: visit /auth/login and verify GitHub button renders
  - Manual: visit /auth/signup and verify GitHub button renders
  - Manual: click GitHub button and verify redirect to GitHub consent
---

## Prompt

Implement the following plan:

# Plan: Add GitHub OAuth Button + Configure All Auth Credentials

## Context

The user wants to enable Google, GitHub, and email/password (credentials) login on the IntelliStack platform. After codebase analysis:

- **Email/password is already fully working**
- **Google OAuth button already exists** on both login/signup pages.
- **GitHub OAuth button is MISSING** — `signInWithGitHub()` is already exported from `lib/auth.ts:181` but never called in the UI.
- **Root blocker:** OAuth credentials (Google & GitHub) are placeholder `xxxx` values in `.env`.

## Response snapshot

Added GitHub OAuth button to both login and signup pages:

1. **login.tsx** — imported `signInWithGitHub`, added `handleGitHubLogin` handler, added GitHub button with Octocat SVG after Google button
2. **signup.tsx** — imported `signInWithGitHub`, added `handleGitHubSignup` handler, added GitHub button with Octocat SVG after Google button
3. **custom.css** — added `.auth-btn-github` class with `#24292e` dark background, white text, hover to `#2c974b` GitHub green

The `.env` file still requires manual credential entry by the user — Google and GitHub OAuth app credentials must be obtained from their respective developer consoles.

## Outcome

- ✅ Impact: GitHub OAuth button now visible on login and signup pages; all three auth methods (email/password, Google, GitHub) have UI entry points
- 🧪 Tests: Manual browser testing required; no unit tests added (UI-only change)
- 📁 Files: 3 files modified (login.tsx, signup.tsx, custom.css)
- 🔁 Next prompts: User must add Google/GitHub credentials to intellistack/auth-server/.env to activate OAuth flows
- 🧠 Reflection: The `signInWithGitHub` function was already exported but unused — a classic "last-mile" wiring issue common in incremental feature development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add loading spinner inside button during redirect
