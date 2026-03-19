---
id: "016"
title: Navbar Footer Logo Polish
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: implement plan
labels: ["ui-polish","navbar","footer","auth-guard","logo","docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/layout/Header.tsx
  - intellistack/frontend/src/app/dashboard/layout.tsx
  - intellistack/frontend/src/components/layout/Footer.tsx
  - intellistack/frontend/src/components/layout/UserMenu.tsx
  - intellistack/content/static/img/logo.svg
tests:
  - manual: community pill shows "Soon" badge above pill, dimmed, cursor-not-allowed
  - manual: /dashboard while logged out redirects to /auth/login?redirect=/dashboard
  - manual: footer shows IS logo, gradient border, 4 columns, social icons
  - manual: usermenu trigger shows avatar+name only, email in dropdown panel
  - manual: docusaurus navbar logo is blue-to-violet IS square
---

## Prompt

Implement the following plan:

# Navbar Polish, Footer Redesign & Docusaurus Logo Sync

## Context

All routing bugs from the previous plan are fixed. This plan addresses 5 remaining UX/visual polish items:
1. Community "Coming Soon" badge repositioned to float **above** the nav pill (not inline to the side)
2. Dashboard page needs an **auth guard** — currently any unauthenticated visitor can reach `/dashboard` and see the stage content
3. Footer needs a **visual redesign** — better brand presence, gradient divider, logo+tagline, cleaner layout
4. UserMenu trigger button currently **leaks the user's email** in the navbar — it should show avatar + name only; email appears only inside the open dropdown
5. Docusaurus navbar logo is a plain green circle — replace with the same **"IS" rounded-rect gradient logo** used in the Next.js frontend

## Response snapshot

Implemented all 5 changes:

1. **Header.tsx** — Removed Community from navLinks array. Added dedicated `<div className="relative">` block with `absolute -top-2.5` "Soon" badge floating above the dimmed, `cursor-not-allowed` pill. Mobile menu gets inline "Soon" badge next to label.

2. **dashboard/layout.tsx** (NEW) — Client component auth guard using `useAuth()`. Redirects unauthenticated users to `/auth/login?redirect=/dashboard`. Shows spinner while loading, renders null if unauthenticated, renders `{children}` when authenticated.

3. **Footer.tsx** — Full redesign: gradient `h-px` top border (blue→violet), IS logo mark + tagline + social icons in top section, 4 reorganized link columns (Learning with stage links, Resources, Company, Legal), bottom bar with copyright.

4. **UserMenu.tsx** — Removed email `<p>` from trigger button. Dropdown panel still shows full name + email.

5. **content/static/img/logo.svg** — Replaced plain green circle with rounded-rect gradient "IS" logo matching Next.js frontend.

## Outcome

- ✅ Impact: All 5 UX/visual polish items implemented — navbar, dashboard auth guard, footer redesign, email privacy, Docusaurus logo sync
- 🧪 Tests: Manual verification required for each change
- 📁 Files: 5 files modified/created
- 🔁 Next prompts: Phase 7 AI Tutor implementation
- 🧠 Reflection: Layout-level auth guard pattern in Next.js App Router keeps server metadata exports in page.tsx while protecting the route client-side

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): pending manual verification
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): add server-side middleware redirect for dashboard as belt-and-suspenders
