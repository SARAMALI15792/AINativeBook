---
id: 017
title: Better-Auth Integration + Book Theme Frontend Overhaul
stage: refactor
date: 2026-02-10
surface: agent
model: claude-opus-4-5-20251101
feature: 001-intellistack-platform
branch: 001-intellistack-platform
user: saram
command: implement plan
labels: ["better-auth", "book-theme", "frontend", "ui-overhaul", "landing-page", "sidebar", "auth-pages"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/app/globals.css
  - intellistack/frontend/tailwind.config.ts
  - intellistack/frontend/src/styles/design-system.css
  - intellistack/frontend/src/app/page.tsx
  - intellistack/frontend/src/components/auth/BetterAuthBadge.tsx
  - intellistack/frontend/src/components/auth/SocialLoginButtons.tsx
  - intellistack/frontend/src/components/auth/PasswordStrengthMeter.tsx
  - intellistack/frontend/src/app/(auth)/layout.tsx
  - intellistack/frontend/src/app/(auth)/login/page.tsx
  - intellistack/frontend/src/app/(auth)/register/page.tsx
  - intellistack/frontend/src/app/(auth)/forgot-password/page.tsx
  - intellistack/frontend/src/app/(auth)/reset-password/page.tsx
  - intellistack/frontend/src/components/layout/BookTopNav.tsx
  - intellistack/frontend/src/components/layout/BookSidebar.tsx
  - intellistack/frontend/src/app/(dashboard)/layout.tsx
  - intellistack/frontend/src/app/(dashboard)/dashboard/page.tsx
  - intellistack/frontend/src/app/(dashboard)/profile/page.tsx
  - intellistack/frontend/src/components/auth/AuthGuard.tsx
  - intellistack/frontend/src/components/layout/index.ts
tests:
  - Manual verification: npm run dev, visit /, /login, /register, /dashboard
---

## Prompt

Implement the following plan:

# Plan: Better-Auth Integration + Book Theme Frontend Overhaul

Upgrade IntelliStack's frontend with proper Better-Auth integration ("Secured by Better Auth" badge), a full marketing landing page, and a polished Top Nav + Collapsible Sidebar layout -- all using the existing book/paper theme (gold/brown palette) unified through Tailwind tokens.

Key insight: The backend auth is already complete. The frontend auth-client.ts is also working. The main work is UI/UX: theming, landing page, auth page redesign, and layout restructuring.

16 tasks across 7 sub-phases: Theme Tokens, Landing Page, Auth Components, Auth Pages, Navigation, Layout Cleanup, Profile Polish.

## Response snapshot

Implemented all 16 tasks across 7 sub-phases:

**Sub-Phase 11.A - Theme Tokens**: Replaced blue/slate CSS variables with book-theme HSL values (paper #f5f0e8, gold #8b6914, brown #8b7355). Added `book` color group and `serif` font family to tailwind.config.ts. Updated design-system.css with book palette.

**Sub-Phase 11.B - Landing Page**: Created full marketing landing page with Hero, Features Grid (6 cards with lucide icons), Learning Path Timeline (5 stages), Testimonials (3 cards), Pricing (Free/Pro/Institution), CTA section, and 4-column footer.

**Sub-Phase 11.C - Auth Pages**: Created BetterAuthBadge, SocialLoginButtons (Google + GitHub), PasswordStrengthMeter components. Redesigned login/register with split layout (brand panel + form). Applied book theme to forgot-password and reset-password pages.

**Sub-Phase 11.D - Navigation**: Created BookTopNav (logo, notifications, user dropdown with lucide icons) and BookSidebar (collapsible wide/narrow, 7 nav items with lucide icons, mobile overlay).

**Sub-Phase 11.E - Dashboard Layout**: Rewrote dashboard layout to use BookTopNav + BookSidebar with localStorage-persisted collapse state. Replaced all hardcoded hex with Tailwind tokens. Added mobile bottom tab bar with lucide icons.

**Sub-Phase 11.F - Cleanup**: Deleted DashboardLayout.tsx, Header.tsx, Sidebar.tsx, userStore.ts. Updated layout index exports. Updated AuthGuard to allow `/` as public route.

**Sub-Phase 11.G - Profile**: Polished profile page with book theme tokens. Added Connected Accounts section (Google, GitHub). Removed imports of old learning components.

**Created 6 new files**: page.tsx (landing), BookTopNav.tsx, BookSidebar.tsx, BetterAuthBadge.tsx, SocialLoginButtons.tsx, PasswordStrengthMeter.tsx

**Modified 12 files**: globals.css, tailwind.config.ts, design-system.css, auth layout, login, register, forgot-password, reset-password, dashboard layout, dashboard page, profile page, AuthGuard, layout index

**Deleted 4 files**: DashboardLayout.tsx, Header.tsx, Sidebar.tsx, userStore.ts

## Outcome

- Impact: Complete frontend UI overhaul from blue/slate to book/gold theme. All auth pages now have split layout with social login and BetterAuthBadge. Dashboard has proper TopNav + collapsible Sidebar. Landing page provides full marketing presence.
- Tests: Manual verification needed (npm run dev)
- Files: 6 created, 12 modified, 4 deleted
- Next prompts: Verify build passes, test responsive behavior, implement remaining Phase 11 polish items
- Reflection: Large-scope refactor executed systematically through 7 sub-phases. All hardcoded hex values replaced with Tailwind tokens. Old deprecated components cleaned up.

## Evaluation notes (flywheel)

- Failure modes observed: None during implementation. Profile page had old imports to learning components that were removed.
- Graders run and results (PASS/FAIL): N/A - manual verification needed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run npm run dev and verify all pages render correctly
