---
name: Frontend Redesign Dashboard Auth Onboarding Navbar
description: Implements Neural Command Center dashboard, social auth on register, compact wizard sizing, and inline navbar badge
type: general
stage: green
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: implement plan
labels: ["frontend", "dashboard", "auth", "navbar", "personalization", "redesign"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/layout/Header.tsx
  - intellistack/frontend/src/components/auth/RegisterForm.tsx
  - intellistack/frontend/src/components/personalization/PersonalizationWizard.tsx
  - intellistack/frontend/src/app/dashboard/page.tsx
tests: []
---

## Prompt

Implement the following plan:

# Plan: Frontend Redesign — Dashboard, Auth, Onboarding, Navbar

The IntelliStack Platform frontend (Next.js, Tailwind + Neural Forge design system) has four UI issues:
1. The dashboard is a plain bento grid with minimal visual impact — needs a striking "Neural Command Center" redesign
2. The register page shows email-only signup — the SocialAuthButtons component (Google + GitHub OAuth) exists but is never imported into RegisterForm
3. Each onboarding wizard step renders at max-w-4xl with min-h-400px, making it oversized and requiring scrolling
4. The "Community — Soon" badge in the desktop navbar uses absolute -top-2.5 positioning, causing it to overflow above the pill container

## Response

Implemented all four changes in execution order:

**Change 1 — Navbar badge fix (Header.tsx)**
Replaced the `<div class="relative">` wrapper + `absolute -top-2.5` positioned badge with a single `<span>` using `inline-flex items-center gap-1.5`. The "Soon" badge is now rendered inline within the pill, matching the mobile menu pattern. No overflow.

**Change 2 — Register social auth (RegisterForm.tsx)**
Added `import { SocialAuthButtons } from '@/components/auth/SocialAuthButtons'` and inserted `<SocialAuthButtons mode="register" />` as the first child inside `<form>`, before the error block. The component renders its own "Or continue with email" divider.

**Change 3 — Wizard compaction (PersonalizationWizard.tsx)**
Five className swaps:
- `max-w-4xl` → `max-w-2xl`
- `mb-8 space-y-4` → `mb-5 space-y-3` (progress bar container)
- `mb-8` → `mb-5` (step indicators container)
- `p-8 min-h-[400px]` → `p-6 min-h-[300px] max-h-[50vh] overflow-y-auto`
- `p-6` → `p-4` (navigation footer)

**Change 4 — Dashboard Neural Command Center (dashboard/page.tsx)**
Full JSX rewrite preserving `stages` array, `docusaurusUrl`, and `metadata` exports intact. New layout:
- Hero section with ambient glow orbs, font-mono eyebrow, gradient headline with `bg-clip-text text-transparent`, fade-up animation
- Progress card (8 cols) with "Mission Status" label, gradient CTA button with `hover:shadow-glow-blue hover:scale-[1.02]`
- Stats panel (4 cols) with new `StatRow` sub-component showing large 3xl colored numbers per stat
- Stage cards with CSS custom property stagger (`--stagger-delay`) for entry animation, hover arrow opacity transition, and locked state with font-mono label
