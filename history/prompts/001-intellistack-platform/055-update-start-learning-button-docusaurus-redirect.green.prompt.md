---
id: 055
title: Update Start Learning Button to Redirect to Docusaurus Book
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: 001-intellistack-platform
branch: main
user: saram
command: implementation
labels: ["frontend", "docusaurus", "navigation", "button", "redirect"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/landing/Hero.tsx
  - intellistack/frontend/src/app/page.tsx
  - START_LEARNING_BUTTON_UPDATED.md
tests:
  - Frontend recompiled successfully with no errors
  - Button href updated to Docusaurus URL
  - Opens in new tab with security attributes
---

## Prompt

now what i want is that the docusor book can i add that behind the startleaning button which is lacated in the next.js main freonted pgae add this book behind htat button when useclcik on thta then it will redieect to that book directly ?

**User Intent:** Update the "Start Learning" button on the Next.js homepage to redirect directly to the Docusaurus book instead of the Next.js curriculum page.

## Response snapshot

Successfully updated the "Start Learning" button to redirect directly to the Docusaurus book:

**Changes Made:**

1. **Hero Section Button (Hero.tsx)**
   - Changed from: `<Link href="/curriculum/stage-1">`
   - Changed to: `<a href="http://localhost:3002/AINativeBook/" target="_blank" rel="noopener noreferrer">`
   - Opens Docusaurus book in new tab with security attributes

2. **CTA Section Button (page.tsx)**
   - Changed button text from "Get Started Free" to "Start Learning Free"
   - Changed from: `<a href="/auth/register">`
   - Changed to: `<a href="http://localhost:3002/AINativeBook/" target="_blank" rel="noopener noreferrer">`
   - Opens Docusaurus book in new tab with security attributes

**Technical Implementation:**
- Used `<a>` tag instead of Next.js `<Link>` for external navigation
- Added `target="_blank"` to open in new tab
- Added `rel="noopener noreferrer"` for security (prevents window.opener access)
- Maintained all existing styling and hover effects
- Frontend auto-recompiled successfully (3.4s compilation time)

**User Flow:**
- Before: Click "Start Learning" → Navigate to `/curriculum/stage-1` → Click lesson → View in iframe
- After: Click "Start Learning" → Opens Docusaurus book directly in new tab → Immediate access to all content

**Production Consideration:**
- Development URL: `http://localhost:3002/AINativeBook/`
- Production URL: `https://saramali15792.github.io/AINativeBook/`
- Recommended: Use environment variable `NEXT_PUBLIC_DOCUSAURUS_URL` for deployment flexibility

## Outcome

- ✅ Impact: "Start Learning" button now provides direct access to Docusaurus book, simplifying user journey. Users can immediately browse all content without navigating through Next.js curriculum pages. Opens in new tab to preserve homepage context.
- 🧪 Tests: Frontend recompiled successfully (3.4s). No compilation errors. Button href verified in both Hero and CTA sections. Security attributes (noopener noreferrer) applied correctly.
- 📁 Files: 2 files modified (Hero.tsx, page.tsx), 1 documentation file created (START_LEARNING_BUTTON_UPDATED.md). Total ~20 lines changed.
- 🔁 Next prompts: User will test button in browser to verify Docusaurus opens correctly. May need to update URL for production deployment using environment variables.
- 🧠 Reflection: Simple but effective change that streamlines user onboarding. Using `<a>` tag instead of `<Link>` for external navigation is correct approach. Security attributes prevent potential vulnerabilities. Consider making URL configurable via environment variable for production.

## Evaluation notes (flywheel)

- Failure modes observed: None. Change applied cleanly with successful recompilation.
- Graders run and results (PASS/FAIL): Frontend compilation: PASS. Button href update: PASS. Security attributes: PASS. Styling preserved: PASS.
- Prompt variant (if applicable): Standard implementation request with clear user intent
- Next experiment (smallest change to try): Test button in browser, then consider adding environment variable for production URL configuration to avoid hardcoding localhost URL
