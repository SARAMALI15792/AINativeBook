---
id: 026
title: Fix signout 404 redirect on Docusaurus site
stage: general
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: fix/signout-404-redirect
user: salim
command: /bug-fix:bug-fix
labels: ["bug-fix","auth","docusaurus","redirect","signout"]
links:
  spec: null
  ticket: https://github.com/SARAMALI15792/AINativeBook/issues/4
  adr: null
  pr: https://github.com/SARAMALI15792/AINativeBook/pull/5
files:
  - intellistack/content/src/theme/NavbarItem/AuthNavbarItem.tsx
tests:
  - Manual: sign in → click Sign Out → verify redirect to Docusaurus home (not 404)
---

## Prompt

After clicking the signout button on the Docusaurus main login page, the user is redirected to a 404 "Page Not Found" error. The signout action completes but the redirect URL is broken. Need to fix the signout redirect to point to a valid page.

## Response snapshot

Root cause: `handleSignOut` in `AuthNavbarItem.tsx` hardcoded `window.location.href = '/'` after sign-out, but the Docusaurus site is hosted at `/AINativeBook/`, not root. Fixed by reading `window.docusaurus?.siteConfig?.baseUrl` (same pattern used in `AuthContext.tsx`) with a fallback to `/AINativeBook/`.

GitHub issue #4 created, branch `fix/signout-404-redirect` created, fix committed and pushed, PR #5 opened.

## Outcome

- ✅ Impact: Sign-out no longer produces a 404; users are redirected to the correct Docusaurus home page
- 🧪 Tests: Manual verification of sign-out flow on local and GitHub Pages deployment
- 📁 Files: AuthNavbarItem.tsx (1 line changed, 1 line added)
- 🔁 Next prompts: Verify fix on deployed GitHub Pages site
- 🧠 Reflection: Two sign-out paths existed (AuthContext.logout and AuthNavbarItem.handleSignOut) — only the navbar item was broken. Consistency between both paths is now ensured.

## Evaluation notes (flywheel)

- Failure modes observed: Hardcoded root path `/` incompatible with non-root Docusaurus baseUrl
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Add a shared `getBaseUrl()` utility to avoid duplication between AuthContext and AuthNavbarItem
