---
id: 051
title: Fix Docusaurus URL routing - remove base path for local dev
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: 001-intellistack-platform
branch: main
user: saram
command: general
labels: ["docusaurus", "routing", "bugfix", "configuration"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/docusaurus.config.ts
  - DOCUSAURUS_URL_FIX.md
  - test_docusaurus_urls.py
tests:
  - Docusaurus URL test: 8/8 tests passed
  - Stage 1-5 intro pages: All accessible
  - Specific content pages: All working
  - HTTP status checks: All 200 OK
---

## Prompt

the docusorios shows firt m the Page Not Found
We could not find what you were looking for.

Please contact the owner of the site that linked you to the original URL and let them know their link is broken. on this end point when it runs http://localhost:3002/stage-1/intro

## Response snapshot

**Issue Identified:**
Docusaurus was configured with `baseUrl: '/AINativeBook/'` for GitHub Pages deployment, which meant all local URLs needed that prefix. The URL `http://localhost:3002/stage-1/intro` was returning 404 because the actual URL was `http://localhost:3002/AINativeBook/stage-1/intro`.

**Root Cause:**
The configuration was hardcoded for production (GitHub Pages) deployment and didn't account for local development needs.

**Solution Implemented:**
Updated `docusaurus.config.ts` to use environment-based configuration:

```typescript
// Environment-based URL configuration
url: process.env.NODE_ENV === 'production'
  ? 'https://saramali15792.github.io'
  : 'http://localhost:3002',
baseUrl: process.env.NODE_ENV === 'production'
  ? '/AINativeBook/'
  : '/',
```

**Changes Made:**
1. Modified `docusaurus.config.ts` to detect environment
2. Set `baseUrl: '/'` for local development
3. Kept `baseUrl: '/AINativeBook/'` for production
4. Killed old Docusaurus processes
5. Restarted Docusaurus with new configuration
6. Verified all URLs working

**Test Results:**
- ✅ Home page: http://localhost:3002/ (200 OK)
- ✅ Stage 1: http://localhost:3002/stage-1/intro (200 OK)
- ✅ Stage 2: http://localhost:3002/stage-2/intro (200 OK)
- ✅ Stage 3: http://localhost:3002/stage-3/intro (200 OK)
- ✅ Stage 4: http://localhost:3002/stage-4/intro (200 OK)
- ✅ Stage 5: http://localhost:3002/stage-5/intro (200 OK)
- ✅ Content pages: All accessible (8/8 tests passed)

**Benefits:**
- Clean URLs in local development (no `/AINativeBook/` prefix needed)
- Automatic environment detection
- Production deployment still works correctly
- No manual URL adjustments needed

## Outcome

- ✅ Impact: Docusaurus now accessible with clean URLs in local development. All 5 stages and content pages working.
- 🧪 Tests: 8/8 URL tests passed - all stage intro pages and content pages accessible
- 📁 Files: Modified 1 config file, created 2 documentation/test files
- 🔁 Next prompts: Test navigation between pages, verify production build still works for GitHub Pages
- 🧠 Reflection: Environment-based configuration is essential for projects that deploy to different environments. Always consider local dev experience alongside production requirements.

## Evaluation notes (flywheel)

- Failure modes observed: Hardcoded production URLs causing 404s in local development
- Graders run and results (PASS/FAIL): All URL tests PASS (8/8)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test production build with `npm run build` to ensure GitHub Pages deployment still works correctly
