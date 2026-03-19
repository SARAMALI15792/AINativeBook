---
id: "017"
title: Fix Curriculum Error Loading Content
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: bug fix
labels: ["bug","curriculum","backend-offline","docusaurus","graceful-degradation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/app/curriculum/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-1/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-2/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-3/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-4/page.tsx
  - intellistack/frontend/src/app/curriculum/stage-5/page.tsx
tests:
  - manual: clicking stage card in curriculum opens Docusaurus stage intro in new tab
  - manual: navigating to /curriculum/stage-1 while backend is offline shows "Open in Docusaurus" link, not error page
  - manual: clicking "Open Stage N in Learning Platform" button opens correct Docusaurus stage
---

## Prompt

when I click on the curriculum and click on any things it shows me this error: "Error Loading Content - Failed to load stage content. Please try again later." also with docusaurus page

## Root Cause

The FastAPI backend (port 8000) is not running. Only auth-server, postgres, redis, and qdrant are up.

The curriculum stage pages (`/curriculum/stage-1` through `stage-5`) make `fetch()` calls to `http://localhost:8000/api/v1/learning/stages/stage-N` which fail with a network error. The `catch` block sets the error state to "Failed to load stage content. Please try again later." and renders the error UI.

## Response snapshot

**Fix 1 — `curriculum/page.tsx`**: Changed stage card links from `href={/curriculum/${stage.slug}}` (internal route that requires the backend) to `href={${DOCUSAURUS_URL}/${stage.slug}/intro}` with `target="_blank"`. Clicking a stage now opens Docusaurus directly — no backend needed.

**Fix 2 — stage-[1-5]/page.tsx**: Added a 5-second `AbortController` timeout to the backend fetch. On `AbortError` or network failure, sets `backendDown=true` instead of `error`. The `backendDown` state renders a graceful fallback UI: IS logo mark, stage name, and a working "Open Stage N in Learning Platform" button linking to Docusaurus. The full backend flow remains intact for when the backend is running.

**Staged generation**: Stage 2-5 pages were generated from stage-1 as a template, changing only `STAGE_SLUG`, `STAGE_NUMBER`, and the stage title string in the fallback UI.

## Outcome

- ✅ Impact: Curriculum is usable without the backend running — users can open Docusaurus content directly
- 🧪 Tests: Manual verification of both the overview links and the stage fallback pages
- 📁 Files: 6 files modified
- 🔁 Next prompts: Start the backend (`docker compose up backend`) for full progress tracking
- 🧠 Reflection: The curriculum stage pages were tightly coupled to the backend API with no offline fallback. Graceful degradation is critical for dev environments where not all services run at once.

## Evaluation notes (flywheel)

- Failure modes observed: network fetch with no timeout blocked for ~30s before erroring
- Graders run and results (PASS/FAIL): pending manual verification
- Prompt variant (if applicable): none
- Next experiment: add a global "backend health" context to suppress backend-dependent UI when unreachable
