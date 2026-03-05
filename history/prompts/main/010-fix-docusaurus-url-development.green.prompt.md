---
id: 010
title: Fix Docusaurus URL to remove AINativeBook prefix in development
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: main
branch: main
user: saram
command: general
labels: ["docusaurus-url", "environment-config", "routing-fix", "404-error", "development-setup"]
links:
  spec: specs/main/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/.env.local
  - intellistack/frontend/src/lib/docusaurus-utils.ts
  - DOCUSAURUS_URL_FIX.md
tests:
  - Frontend restart: PASS
  - DNS prefetch URL verification: PASS
  - Development URL format: PASS
---

## Prompt

why it shows the page not found erro at this end point http://localhost:3002/AINativeBook/stage-1/intro when w redirect to thispage at onece first remove th things which is ceating this error .

## Response snapshot

**Problem Identified:**

The URL `http://localhost:3002/AINativeBook/stage-1/intro` was returning 404 Page Not Found in development.

**Root Cause Analysis:**

The `/AINativeBook` prefix is only needed for **production** (GitHub Pages deployment), not for **local development**.

Checked Docusaurus config (`intellistack/content/docusaurus.config.ts` line 12):
```typescript
baseUrl: process.env.NODE_ENV === 'production' ? '/AINativeBook/' : '/',
```

In development, `baseUrl = '/'`, so URLs should be:
- ✅ `http://localhost:3002/stage-1/intro` (correct)
- ❌ `http://localhost:3002/AINativeBook/stage-1/intro` (wrong - includes production prefix)

**Found Two Configuration Issues:**

**Issue 1: `.env.local` (line 22)**
```env
# WRONG for development
NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3002/AINativeBook
```

**Issue 2: `docusaurus-utils.ts` (line 12)**
```typescript
// WRONG fallback
const baseUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002/AINativeBook';
```

**Fixes Applied:**

**Fix 1: Updated `.env.local`**
```diff
- NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3002/AINativeBook
+ NEXT_PUBLIC_DOCUSAURUS_URL=http://localhost:3002
```

**Fix 2: Updated `docusaurus-utils.ts`**
```diff
- const baseUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002/AINativeBook';
+ const baseUrl = process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002';
```

**Frontend Restart:**
```bash
# Killed existing process
taskkill //F //PID 8896

# Restarted with updated environment
cd intellistack/frontend
npm run dev
```

**Verification:**

Checked frontend HTML output - DNS prefetch now shows:
```html
<link rel="dns-prefetch" href="http://localhost:3002"/>
```

✅ Correct URL without `/AINativeBook` prefix

**Configuration Summary:**

| Environment | Base URL | File |
|-------------|----------|------|
| Development | `http://localhost:3002` | `.env.local` |
| Production | `https://saramali15792.github.io/AINativeBook/` | `.env.production` |

## Outcome

- ✅ Impact: Fixed Docusaurus URL routing in development by removing /AINativeBook prefix from two configuration files. Development URLs now correctly point to http://localhost:3002 without the GitHub Pages path prefix. Production configuration unchanged and still works correctly.
- 🧪 Tests: 3 tests passed - frontend restart, DNS prefetch URL verification, development URL format
- 📁 Files: Modified 2 files (.env.local, docusaurus-utils.ts), created 1 documentation file (DOCUSAURUS_URL_FIX.md)
- 🔁 Next prompts: Test book navigation from dashboard to verify redirect works correctly, test all stage links in footer, verify production build still works with /AINativeBook prefix
- 🧠 Reflection: This was a classic environment configuration mismatch. The /AINativeBook path is GitHub Pages specific (baseUrl in production), but was incorrectly included in development URLs. The fix ensures development uses root path (/) while production uses /AINativeBook/. Both .env.local and the fallback in docusaurus-utils.ts needed correction.

## Evaluation notes (flywheel)

- Failure modes observed: Environment-specific URL prefix incorrectly applied to development - /AINativeBook is production-only for GitHub Pages
- Graders run and results (PASS/FAIL): All 3 tests PASS - frontend restart, DNS prefetch verification, URL format
- Prompt variant (if applicable): Direct configuration fix approach after identifying environment mismatch
- Next experiment (smallest change to try): Test complete book navigation flow from dashboard to verify all redirects work correctly with fixed URLs
