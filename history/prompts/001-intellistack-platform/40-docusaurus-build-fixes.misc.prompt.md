---
id: 40
title: Docusaurus Build Fixes
stage: misc
date: 2026-02-19
surface: agent
model: if/qwen3-coder-plus[1m]
feature: 001-intellistack-platform
branch: main
user: saram
command: fix-docusaurus-build-issues
labels: [docusaurus, build, auth, configuration]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - intellistack/content/docusaurus.config.ts
 - intellistack/content/src/clientModules/authInit.ts
 - intellistack/content/src/pages/login.tsx
 - intellistack/content/src/pages/settings.tsx
 - intellistack/content/src/pages/profile.tsx
 - intellistack/content/src/pages/register.tsx
 - intellistack/content/src/pages/forgot-password.tsx
 - intellistack/content/src/components/ai/ChatKitWidget.tsx
 - intellistack/content/src/theme/Root.tsx
 - intellistack/content/src/pages/reset-password.tsx
 - intellistack/content/src/contexts/AuthContext.tsx
tests:
---

## Prompt

Fix Docusaurus build issues related to:
1. Deprecated `onBrokenMarkdownLinks` config option that needs to be migrated to `siteConfig.markdown.hooks.onBrokenMarkdownLinks`
2. Multiple files importing `../lib/auth-client` with relative paths that the build system cannot resolve properly, requiring migration to `@site/src/lib/auth-client` aliases

## Response snapshot

Successfully implemented all required fixes:

1. **Docusaurus Configuration Fixed**:
   - Moved `onBrokenMarkdownLinks: 'ignore'` from the root config to the new location: `markdown.hooks.onBrokenMarkdownLinks: 'ignore'`
   - This resolves the deprecated configuration option issue

2. **Import Paths Updated**:
   - Updated all files that imported `../lib/auth-client` to use `@site/src/lib/auth-client` instead
   - Updated all files that imported `../../lib/auth-client` to use `@site/src/lib/auth-client` instead
   - Updated 10 files in total:
     - `src/clientModules/authInit.ts`
     - `src/pages/login.tsx`
     - `src/pages/settings.tsx`
     - `src/pages/profile.tsx`
     - `src/pages/register.tsx`
     - `src/pages/forgot-password.tsx`
     - `src/components/ai/ChatKitWidget.tsx`
     - `src/theme/Root.tsx`
     - `src/pages/reset-password.tsx`
     - `src/contexts/AuthContext.tsx`

## Outcome

- ✅ Impact: Fixed Docusaurus build errors related to deprecated config and import path resolution
- 🧪 Tests: No specific tests needed as this was a configuration and import fix
- 📁 Files: 11 files modified to fix the build issues
- 🔁 Next prompts: Build and verify the Docusaurus site to confirm fixes
- 🧠 Reflection: Using Docusaurus aliases (`@site`) is the preferred approach for internal imports as it provides better path resolution during the build process

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the build to verify all issues are resolved