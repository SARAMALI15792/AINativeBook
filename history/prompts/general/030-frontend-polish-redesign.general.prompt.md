---
name: Frontend Polish & Redesign
description: Comprehensive UI redesign — Fraunces font, glassmorphism footer, split-screen login, bento grid, triangle loaders, dark/light mode, onboarding redesign
type: general
stage: green
id: "030"
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: "Implement the following plan: Frontend Polish & Redesign — IntelliStack Platform"
labels: ["frontend", "redesign", "ux", "design-system", "dark-mode", "onboarding", "auth"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

## Prompt

Implement the Frontend Polish & Redesign plan for IntelliStack Platform covering:
- Design token updates (Fraunces font, new brand variables)
- Next.js: BentoGrid features, glassmorphism footer (72px), RouterTransition progress bar
- Docusaurus: Split-screen login/signup, triangle loader system, redesigned onboarding (4 steps), dark/light mode toggle with backend persistence
- Backend: /theme endpoint in preferences_routes.py
- canvas-confetti for step-4 confirmation

## Response

### Files Created/Modified

**Next.js Frontend (`intellistack/frontend/`):**
- `src/styles/tokens.css` — Added brand variables (`--color-brand`, `--color-brand-dim`, `--color-surface`, `--color-surface-elevated`, `--color-border`), updated `--font-heading` to Fraunces
- `src/app/layout.tsx` — Swapped `Sora` → `Fraunces` from `next/font/google`, added `RouterTransition` component
- `src/components/ui/RouterTransition.tsx` — NEW: 3px brand-color progress bar on route change using `usePathname`
- `src/components/ui/TriangleLoader.tsx` — NEW: SVG equilateral triangle with `stroke-dasharray` animation + gradient stroke + pulse scale; sizes sm/md/lg; variants inline/page
- `src/components/layout/Footer.tsx` — REPLACED: 72px glassmorphism slim bar with gradient top border, logo+tagline, nav links, social icons
- `src/components/landing/BentoGrid.tsx` — NEW: Asymmetric 12-col CSS Grid with Framer Motion `whileInView` + `staggerChildren: 0.07`; hover glow + scale; gradient border accent line
- `src/app/page.tsx` — Updated to use `BentoGrid` instead of `FeatureCard` grid

**Docusaurus Content (`intellistack/content/`):**
- `src/css/tokens.css` — Updated `--font-heading` to Fraunces
- `docusaurus.config.ts` — Updated Google Fonts URL to include Fraunces; enabled `colorMode.disableSwitch: false` + `respectPrefersColorScheme: true`
- `src/css/custom.css` — Added brand vars, light mode CSS variable overrides (html[data-theme='light']), smooth `transition: 0.3s ease` on all elements, split-screen auth classes, onboarding card classes, floating label styles, pill buttons, icon cards
- `src/components/ui/TriangleLoader.tsx` — NEW: Same triangle loader design for Docusaurus (no 'use client' directive)
- `src/pages/auth/login.tsx` — REPLACED: Full split-screen layout with animated conic-gradient blob, rotating quotes, floating label inputs, brand CTA, OAuth outlined buttons, "Powered by BetterAuth" footer
- `src/pages/auth/signup.tsx` — REPLACED: Matching split-screen treatment for registration
- `src/pages/auth/callback.tsx` — UPDATED: Replaced circular spinner with TriangleLoader; premium dark card UI
- `src/components/onboarding/StepIndicator.tsx` — REPLACED: Thin 3px progress bar + step counter text
- `src/pages/onboarding/step-1.tsx` — REDESIGNED: Onboarding card with pill language selector + timezone select
- `src/pages/onboarding/step-2.tsx` — REDESIGNED: Role pill buttons (Student/Professional/Researcher/Hobbyist) + experience pills
- `src/pages/onboarding/step-3.tsx` — REDESIGNED: Icon cards (Solo/Team/Academic) + goal pill multi-select
- `src/pages/onboarding/step-4.tsx` — REDESIGNED: Source pills + canvas-confetti confirmation screen on completion
- `src/theme/ColorModeToggle/index.tsx` — NEW: Swizzled Docusaurus toggle with custom Sun/Moon SVGs; persists theme via PATCH /api/v1/users/preferences/theme
- `src/clientModules/authInit.ts` — UPDATED: Restores saved theme preference on login by reading from auth server session
- `package.json` — Added `canvas-confetti@^1.9.3` + `@types/canvas-confetti`

**Backend (`intellistack/backend/`):**
- `src/core/users/preferences_routes.py` — Added `PATCH /api/v1/users/preferences/theme` endpoint; stores in `user.preferences["theme"]` JSON column

## Outcome

All 22 files implemented. Key design decisions:
- Fraunces serif replaces Sora for heading display — editorial premium aesthetic
- Split-screen login uses CSS class-based approach (not Tailwind) for Docusaurus compatibility
- Triangle SVG loader uses `stroke-dasharray`/`stroke-dashoffset` animation + linear gradient stroke
- canvas-confetti loaded via dynamic `import()` for graceful degradation if not installed
- Light mode uses `html[data-theme='light']` selectors matching Docusaurus data attribute
- Theme persistence: toggle → PATCH backend → restore in authInit.ts on next login
