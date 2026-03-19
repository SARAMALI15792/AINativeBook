---
id: 1000
title: Fix Frontend Navigation and Routing Issues
stage: green
date: 2026-02-20
surface: agent
model: claude-sonnet-4.5
feature: 001-intellistack-platform
branch: main
user: saram
command: implementation
labels: ["frontend", "navigation", "routing", "bug-fix", "next.js", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/landing/Hero.tsx
  - intellistack/frontend/src/app/page.tsx
  - intellistack/frontend/src/components/layout/Footer.tsx
  - intellistack/frontend/src/app/dashboard/page.tsx
  - intellistack/frontend/src/app/curriculum/page.tsx
tests:
  - Production build completed successfully (exit code 0)
  - Dev server running without errors
  - No 404 errors for navigation links
---

## Prompt

Implement the following plan:

# Fix Frontend Navigation and Routing Issues

## Context

The IntelliStack platform uses a **two-app architecture**:
1. **Next.js Frontend** (port 3000) - Marketing, auth, dashboard
2. **Docusaurus Content** (port 3002) - Learning content, curriculum

**Problem:** Users clicking "Get Started" or "Explore" buttons get 404 errors because these buttons link to `/docs/stage-1/intro` which doesn't exist in the Next.js app. The docs only exist in the separate Docusaurus app at `http://localhost:3002/stage-1/intro`.

**Root Cause:** Hardcoded internal links assume `/docs` routes exist in Next.js when they don't. The Header component correctly uses `NEXT_PUBLIC_DOCUSAURUS_URL` environment variable, but Hero and Home page components don't follow this pattern.

## Recommended Approach: Multi-Phase Fix

### Phase 1: Quick Fix - Update Broken Links (Immediate)

Update all hardcoded `/docs` links to use external Docusaurus URLs with environment variable.

**Files to modify:**
1. `intellistack/frontend/src/components/landing/Hero.tsx` (lines 60, 66)
2. `intellistack/frontend/src/app/page.tsx` (lines 169, 175)
3. `intellistack/frontend/src/components/layout/Footer.tsx` (line 18)

### Phase 2: Add Missing Authenticated Routes (Medium Priority)

Create placeholder pages for authenticated user flows:
1. `/dashboard` - Student dashboard
2. `/curriculum` - Curriculum overview page

## Response snapshot

Successfully implemented all fixes for frontend navigation and routing issues:

### Changes Implemented:

**1. Hero Component** (`src/components/landing/Hero.tsx`)
- Updated both CTA buttons to use `${process.env.NEXT_PUBLIC_DOCUSAURUS_URL || 'http://localhost:3002'}/stage-1/intro`
- Added `target="_blank"` and `rel="noopener noreferrer"` for external links

**2. Home Page CTA Section** (`src/app/page.tsx`)
- Updated "Get Started Free" and "Learn More" links to use environment variable
- Added proper external link attributes

**3. Footer Component** (`src/components/layout/Footer.tsx`)
- Fixed Documentation link to use environment variable with proper fallback

**4. Created Dashboard Page** (`src/app/dashboard/page.tsx`)
- New authenticated user dashboard with link to Stage 1
- Includes Header and Footer components
- Glass morphism design consistent with platform

**5. Created Curriculum Page** (`src/app/curriculum/page.tsx`)
- Comprehensive 5-stage curriculum overview
- Each stage card links to Docusaurus content
- Includes stage descriptions and "How It Works" section
- Responsive grid layout with hover effects

### Build Verification:
- Production build completed successfully (exit code 0)
- Only pre-existing ESLint warnings (no new errors)
- Generated 9 static pages successfully
- Dev server running at http://localhost:3000

## Outcome

- ✅ Impact: Fixed all 404 navigation errors; users can now access Docusaurus content from all CTA buttons
- 🧪 Tests: Production build passed, dev server running without errors, no 404s in logs
- 📁 Files: Modified 3 components, created 2 new pages (dashboard, curriculum)
- 🔁 Next prompts: Test navigation flows manually, verify external links open in new tabs, consider adding loading states
- 🧠 Reflection: Environment variable pattern now consistent across all navigation components; two-app architecture properly handled

## Evaluation notes (flywheel)

- Failure modes observed: None - all changes compiled successfully
- Graders run and results (PASS/FAIL): Build: PASS, Lint: PASS (warnings only), Type check: PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add visual indicators for external links (icon or tooltip)
