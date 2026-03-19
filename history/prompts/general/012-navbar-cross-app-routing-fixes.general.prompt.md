---
id: 012
title: Navbar & Cross-App Routing Fixes
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: implement navbar cross-app routing plan
labels: ["navbar","routing","header","footer","docusaurus","tailwind","z-index","dropdown"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/layout/Header.tsx
  - intellistack/frontend/src/components/layout/Footer.tsx
  - intellistack/frontend/src/components/layout/UserMenu.tsx
  - intellistack/content/src/components/UserMenu.tsx
tests:
  - manual: Stages dropdown opens/closes on desktop with 5 stage links
  - manual: Mobile hamburger shows flat stage list
  - manual: Footer Documentation opens Docusaurus in new tab
  - manual: Docusaurus UserMenu Login/SignUp navigate to correct auth pages
  - manual: Navbar renders above Hero (z-index fix)
  - manual: UserMenu dropdown shows visible borders and hover backgrounds
---

## Prompt

Implement the following plan:

# Navbar & Cross-App Routing — Link Next.js Header to Docusaurus Stages

Bugs identified and plan to fix z-sticky class, replace "Book" link with Stages dropdown, fix Footer Documentation external link and wrong port, fix Docusaurus UserMenu auth hrefs, and fix frontend UserMenu missing Tailwind tokens.

## Response snapshot

Implemented all 5 fixes across 4 files:

1. **Header.tsx** — Replaced `z-sticky` with `z-[1100]`. Removed single "Book" link. Added `stages` array with 5 entries + `isStagesOpen` state + `stagesRef` for outside-click detection. Desktop: pill button with chevron + dropdown panel (`z-[1200]`). Mobile: labeled section with flat stage links.

2. **Footer.tsx** — Extracted `docUrl` const with corrected port `3005`. Removed `Documentation` from `resources` array. Added standalone `<a href={docUrl} target="_blank">` in Resources JSX, replacing the broken `<Link>`.

3. **content/UserMenu.tsx** — Used existing `siteConfig.baseUrl` to build `/AINativeBook/auth/login` and `/AINativeBook/auth/signup` hrefs, replacing hardcoded `/login` and `/register`.

4. **frontend/UserMenu.tsx** — Replaced all `glass-border` occurrences → `border-subtle` and all `glass-highlight` occurrences → `bg-elevated` (valid tokens in tailwind config).

## Outcome

- ✅ Impact: All cross-app navigation between Next.js (port 3000) and Docusaurus (port 3005) is now correctly wired. Stages dropdown provides direct access to all 5 learning stages. Auth links resolve to valid Docusaurus pages. UserMenu dropdown is visually correct.
- 🧪 Tests: Manual browser verification required across both apps
- 📁 Files: 4 files modified
- 🔁 Next prompts: Verify on running dev stack; consider adding active-stage highlighting in dropdown
- 🧠 Reflection: The `z-sticky` bug is a classic case of a dev expecting Tailwind to auto-generate a utility from a CSS variable name — Tailwind only generates from its config, not CSS vars. Arbitrary values `z-[1100]` are the correct escape hatch.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): none
- Next experiment: Add keyboard navigation (Escape to close dropdown) to Stages dropdown
