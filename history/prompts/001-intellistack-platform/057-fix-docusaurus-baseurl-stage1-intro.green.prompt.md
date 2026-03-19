---
id: 057
title: Fix Docusaurus BaseUrl and Update Button to Stage 1 Intro
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: 001-intellistack-platform
branch: main
user: saram
command: troubleshooting
labels: ["docusaurus", "routing", "baseUrl", "404-fix", "button"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/docusaurus.config.ts
  - intellistack/frontend/src/components/landing/Hero.tsx
  - intellistack/frontend/src/app/page.tsx
  - DOCUSAURUS_FIXED_NO_404.md
tests:
  - Docusaurus accessible at http://localhost:3005/AINativeBook/
  - Stage 1 intro accessible at http://localhost:3005/AINativeBook/stage-1/intro
  - HTTP 200 status confirmed
  - Frontend buttons updated and recompiled
---

## Prompt

again it shows me this [404 Page Not Found] at this endpoint http://localhost:3005/stage-1/intro

**Context:** User clicked "Start Learning Free" button and got 404 error when trying to access stage-1/intro content.

## Response snapshot

Fixed the 404 error by correcting the Docusaurus baseUrl configuration and updating button URLs to point directly to Stage 1 intro page:

**Root Cause:**
1. Docusaurus config had incorrect baseUrl: `/AINativeBook/ur/` (Urdu language path)
2. Button was pointing to homepage instead of actual content
3. User tried accessing `http://localhost:3005/stage-1/intro` (missing `/AINativeBook/` base path)

**Solution:**

1. **Fixed Docusaurus Configuration:**
   - Changed `baseUrl` from `/AINativeBook/ur/` to `/AINativeBook/`
   - Updated `url` to use port 3005
   - Removed conditional baseUrl (now same for dev and production)
   - Killed old Docusaurus process (PID 10288)
   - Restarted with corrected config

2. **Updated Button URLs:**
   - Changed from: `http://localhost:3005/AINativeBook/`
   - Changed to: `http://localhost:3005/AINativeBook/stage-1/intro`
   - Now opens directly to Stage 1 introduction page
   - Updated both Hero and CTA section buttons

3. **Verified Routing:**
   - Confirmed `routeBasePath: '/'` in Docusaurus config
   - Docs served at root of baseUrl
   - Correct URL structure: `{baseUrl}/stage-1/intro`
   - HTTP 200 status confirmed via curl

**Key Discovery:**
The `/ur/` suffix was for Urdu language support (i18n config with 'en' and 'ur' locales). Using it as the default baseUrl caused all English content to 404.

**Correct URL Structure:**
- Base: `http://localhost:3005/AINativeBook/`
- Stage 1 Intro: `http://localhost:3005/AINativeBook/stage-1/intro`
- Stage 2: `http://localhost:3005/AINativeBook/stage-2/...`

## Outcome

- ✅ Impact: 404 errors resolved. "Start Learning Free" button now opens directly to Stage 1 intro page with actual learning content. Users can immediately start reading and navigating through the curriculum.
- 🧪 Tests: Docusaurus restarted successfully. HTTP 200 status confirmed for both base URL and stage-1/intro. Frontend recompiled with updated button URLs. All 7 services running healthy.
- 📁 Files: 3 files modified (docusaurus.config.ts, Hero.tsx, page.tsx), 1 documentation file created. Docusaurus process restarted (task b64c2a2).
- 🔁 Next prompts: User will test button in browser to verify Stage 1 intro page opens correctly. May want to add navigation between stages or return to Next.js curriculum view.
- 🧠 Reflection: The `/ur/` baseUrl was the root cause of all 404 errors. Docusaurus i18n config was set up for English and Urdu, but the default baseUrl was incorrectly pointing to Urdu path. Changing button to point directly to stage-1/intro provides better UX than landing on homepage.

## Evaluation notes (flywheel)

- Failure modes observed: Initial baseUrl configuration error. Process on port 3005 needed manual kill. Multiple restarts required to apply config changes.
- Graders run and results (PASS/FAIL): Docusaurus config fix: PASS. Process restart: PASS. URL accessibility: PASS (HTTP 200). Button URL updates: PASS. Frontend recompilation: PASS.
- Prompt variant (if applicable): Standard troubleshooting with 404 error report
- Next experiment (smallest change to try): Test button in browser to verify stage-1/intro opens correctly, then consider adding environment variable for baseUrl to avoid hardcoding localhost URLs
