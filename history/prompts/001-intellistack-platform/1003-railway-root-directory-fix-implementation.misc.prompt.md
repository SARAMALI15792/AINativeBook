---
id: 1003
title: Railway Root Directory Fix Implementation
stage: misc
date: 2026-02-21
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: Implement the following plan
labels: ["railway", "deployment", "fix", "root-directory", "devops"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - fix-railway-root-directory.py
  - fix-railway-root-directory.bat
  - RAILWAY_FIX_CHECKLIST.md
  - RAILWAY_SIMPLE_GUIDE.md
  - RAILWAY_FIX_COMPLETE.md
tests:
  - None (deployment configuration fix)
---

## Prompt

Implement the following plan:

# Fix Railway Deployment Root Directory Issue

## Context

The Railway deployment migration was completed, but all services are failing to deploy with the error:
```
Root Directory `intellistack/content   ` does not exist
```

**Current State:**
- Railway project created: `intellistack-platform`
- 4 services exist: backend, auth-server, content, Redis
- All environment variables are correctly configured
- The issue: Root Directory settings in Railway dashboard have trailing spaces
- Railway CLI cannot fix this - it must be done through the dashboard

**Root Cause:**
When the user configured the Root Directory in the Railway dashboard, trailing spaces were accidentally added. The Railway CLI shows the environment variable `RAILWAY_ROOT_DIRECTORY` is correct, but the actual service configuration (set in the dashboard UI) has spaces that prevent deployment.

## Problem

Railway's build system (Railpack) reads the Root Directory from the service settings (not from environment variables). The trailing spaces cause it to look for:
- `intellistack/content   ` (with 3 spaces) ❌
Instead of:
- `intellistack/content` ✅

## Solution

Since Railway CLI cannot modify the Root Directory setting in the dashboard, we need to provide the user with the simplest possible way to fix this manually.

[Full plan details provided in context]

## Response snapshot

Created a comprehensive solution with multiple approaches to fix the Railway Root Directory trailing spaces issue:

### Files Created:

1. **fix-railway-root-directory.py** - Interactive Python script
   - Opens Railway dashboard automatically using webbrowser module
   - Guides user step-by-step through each service (backend, auth-server, content)
   - Waits for user confirmation after each fix
   - Attempts to verify deployments using Railway CLI
   - Provides final status check after 60-second wait

2. **fix-railway-root-directory.bat** - Windows batch script
   - Native Windows solution with no dependencies
   - Opens Railway dashboard using `start` command
   - Shows clear instructions for each service
   - Pauses between services for user action
   - Simple and reliable for Windows users

3. **RAILWAY_FIX_CHECKLIST.md** - Manual checklist
   - Step-by-step checkbox format
   - Detailed instructions for each service
   - Success indicators section
   - Troubleshooting guide
   - Perfect for users who prefer manual control

4. **RAILWAY_SIMPLE_GUIDE.md** - Comprehensive guide (updated existing file)
   - Complete problem explanation
   - Detailed fix instructions with emphasis on "Select ALL text" and "Delete completely"
   - Verification steps with curl commands
   - Expected service URLs
   - Troubleshooting section
   - Links to alternative helper scripts

5. **RAILWAY_FIX_COMPLETE.md** - Implementation summary
   - Problem analysis
   - Solution overview
   - All approaches documented
   - Success criteria
   - Next steps after deployment
   - Rationale for manual approach

### Key Implementation Details:

**Why Manual Fix:**
- Railway CLI cannot modify Root Directory settings (dashboard-only configuration)
- Railway API documentation unclear for this specific setting
- Manual fix is simple (2-3 minutes) and guaranteed to work
- Helper scripts provide guidance without complex dependencies

**Critical Fix Steps:**
1. Select ALL text in Root Directory field (Ctrl+A / Cmd+A)
2. Delete it completely
3. Type exact path manually (no copy-paste to avoid hidden characters)
4. Press Tab to save
5. Click Redeploy

**Correct Paths:**
- backend: `intellistack/backend`
- auth-server: `intellistack/auth-server`
- content: `intellistack/content`

**Expected Timeline:**
- Fix time: 2-3 minutes
- Deployment time: 5-10 minutes per service
- Total: ~15 minutes

**Verification:**
```bash
curl https://intellistack-platform-production-backend.up.railway.app/health
curl https://intellistack-platform-production-auth-server.up.railway.app/health
curl https://intellistack-platform-production-content.up.railway.app/health
```

All should return: `{"status": "healthy"}`

## Outcome

- ✅ Impact: Created comprehensive fix solution with 3 different approaches (Python script, batch script, manual checklist) to resolve Railway deployment failure caused by trailing spaces in Root Directory fields
- 🧪 Tests: None (deployment configuration fix, no code changes)
- 📁 Files: 5 files created/updated (Python script, batch script, 3 markdown guides)
- 🔁 Next prompts: User executes fix using preferred method, then verifies deployments and tests health endpoints
- 🧠 Reflection: Railway CLI limitation required creative solution - provided multiple user-friendly approaches to ensure success regardless of user preference or environment

## Evaluation notes (flywheel)

- Failure modes observed: Railway CLI cannot modify dashboard-only settings; trailing spaces in text fields are invisible and hard to debug
- Graders run and results (PASS/FAIL): N/A (deployment configuration, not code)
- Prompt variant (if applicable): Implementation from plan mode
- Next experiment (smallest change to try): After user fixes and deploys, monitor for any additional Railway configuration issues or environment variable problems
