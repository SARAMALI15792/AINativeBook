---
id: 048
title: Fix Start Learning Not Found Errors
stage: green
date: 2026-02-25
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: fix start learning routing
labels: ["routing","frontend","curriculum","next.js","bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/landing/Hero.tsx
  - intellistack/frontend/src/app/curriculum/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-1/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-2/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-3/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-4/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-5/page.tsx
  - intellistack/frontend/src/app/dashboard/page.tsx
tests:
  - none
---

## Prompt

ok now two erroe when i click on the start leanng form the main next.js freonted it gices me the erros of the not found fix this issue link both freotned proply and all the funcationality of each concneted must each other

## Response snapshot

Root cause: "Start Learning Free" and "Explore Curriculum" buttons in Hero.tsx were pointing to external Docusaurus URL (`http://localhost:3002/stage-1/intro`) which is a separate service not always running. Curriculum page stage links also pointed externally. Dashboard used `getDocusaurusUrl()` helper for the same external link.

Fixes applied:
1. Hero.tsx — both CTAs changed to internal Next.js routes (`/curriculum/stage-1` and `/curriculum`)
2. curriculum/page.tsx — stage links changed to `/curriculum/${stage.slug}` (internal)
3. dashboard/page.tsx — replaced single external link with full stage card grid linking internally
4. Created stage pages for stage-2 through stage-5 (stage-1 existed but used wrong API path)
5. stage-1/page.tsx — fixed API fetch URLs to use `NEXT_PUBLIC_API_URL` env var

## Outcome

- ✅ Impact: All "Start Learning" and "Explore Curriculum" clicks now route within the Next.js app, no more not-found errors
- 🧪 Tests: Manual routing verification; no automated tests added
- 📁 Files: 8 files modified/created
- 🔁 Next prompts: Add real progress data from backend API to dashboard; implement content item detail pages
- 🧠 Reflection: External Docusaurus links should only be used for the "Books" nav item where documentation browsing is intended; all learning flow navigation should be internal

## Evaluation notes (flywheel)

- Failure modes observed: Mixed internal/external routing with no clear convention caused broken UX
- Graders run and results (PASS/FAIL): Manual review PASS
- Prompt variant (if applicable): null
- Next experiment: Add loading skeleton states to stage pages while API fetches
