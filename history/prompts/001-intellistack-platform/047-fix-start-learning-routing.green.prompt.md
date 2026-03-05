---
id: "047"
title: Fix Start Learning Routing
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-intellistack-platform
branch: main
user: saram
command: fix start learning routing
labels: ["routing","frontend","curriculum","next.js"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/app/curriculum/stage-2/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-3/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-4/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-5/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-1/page.tsx
  - intellistack/frontend/src/components/landing/Hero.tsx
  - intellistack/frontend/src/app/curriculum/page.tsx
tests:
  - none
---

## Prompt

You are working on a Next.js frontend at `intellistack/frontend/`. The task is to fix the "Start Learning" routing by:

1. The `intellistack/frontend/src/app/curriculum/stage-1/page.tsx` already exists (was just created). Create identical pages for stages 2-5 in their respective folders:
   - `intellistack/frontend/src/app/curriculum/stage-2/page.tsx`
   - `intellistack/frontend/src/app/curriculum/stage-3/page.tsx`
   - `intellistack/frontend/src/app/curriculum/stage-4/page.tsx`
   - `intellistack/frontend/src/app/curriculum/stage-5/page.tsx`

   Each page should be the same pattern as stage-1 but with `stage-2`, `stage-3`, etc. substituted everywhere the slug appears.

2. Also update `intellistack/frontend/src/app/curriculum/stage-1/page.tsx` to fix the API URL — it currently calls `/api/learning/...` (no env var) but should call `${process.env.NEXT_PUBLIC_API_URL}/learning/...`. Replace both fetch calls to use the env var.

3. Update `intellistack/frontend/src/components/landing/Hero.tsx` — change both Link hrefs from external Docusaurus URLs to internal Next.js routes:
   - "Start Learning Free" → `/curriculum/stage-1`
   - "Explore Curriculum" → `/curriculum`
   Also remove `target="_blank"` and `rel="noopener noreferrer"` from both links.

4. Update `intellistack/frontend/src/app/curriculum/page.tsx` — the stage links currently go to external Docusaurus URLs. Change them to internal Next.js `<Link href={`/curriculum/${stage.slug}`}>` and remove `target="_blank"` and `rel="noopener noreferrer"`.

## Response snapshot

All four tasks completed successfully:

1. Created stage-2, stage-3, stage-4, stage-5 pages — each is an exact copy of the stage-1 pattern with the stage slug substituted in all relevant locations: auth redirect URL, both fetch URLs (`/learning/stages/stage-N` and `/learning/stages/stage-N/content`), content item "View content" router.push path, and the exported function name (`Stage2Page`, etc.).

2. Fixed stage-1 page: replaced `/api/learning/stages/stage-1` with `${process.env.NEXT_PUBLIC_API_URL}/learning/stages/stage-1` and `/api/learning/stages/stage-1/content` with `${process.env.NEXT_PUBLIC_API_URL}/learning/stages/stage-1/content`.

3. Fixed Hero.tsx: replaced both external Docusaurus Link hrefs with `/curriculum/stage-1` and `/curriculum` respectively, and removed `target="_blank"` and `rel="noopener noreferrer"` from both.

4. Fixed curriculum/page.tsx: replaced the external Docusaurus href template literal with internal `/curriculum/${stage.slug}`, and removed `target="_blank"` and `rel="noopener noreferrer"`.

## Outcome

- Impact: All five curriculum stage pages are now reachable via internal Next.js routing. Hero CTA buttons and curriculum stage cards link internally instead of externally to a Docusaurus instance.
- Tests: No automated tests run; routing changes are structural/navigational.
- Files: 7 files modified/created (4 new stage pages, 3 updated existing files).
- Next prompts: Implement actual content viewer pages at `/curriculum/stage-N/[slug]`; wire up backend authentication token to fetch calls.
- Reflection: The fix is minimal and isolated — no unrelated code changed. The pattern is consistent across all five stage pages.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Add a dynamic `[slug]` content viewer route under each stage folder
