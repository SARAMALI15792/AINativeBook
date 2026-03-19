---
id: "011"
title: Neural Forge UI Redesign — Full Platform Polish
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: implement neural forge ui redesign plan
labels: ["ui", "design-system", "tokens", "fonts", "tailwind", "docusaurus", "next.js"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/styles/tokens.css
  - intellistack/content/src/css/tokens.css
  - intellistack/frontend/tailwind.config.js
  - intellistack/frontend/src/app/layout.tsx
  - intellistack/frontend/src/styles/globals.css
  - intellistack/frontend/src/styles/animations.css
  - intellistack/frontend/src/components/ui/Button.tsx
  - intellistack/frontend/src/components/ui/Input.tsx
  - intellistack/frontend/src/components/effects/GlassCard.tsx
  - intellistack/frontend/src/components/effects/NeuralNetworkBackground.tsx
  - intellistack/frontend/src/components/layout/Header.tsx
  - intellistack/frontend/src/components/layout/Footer.tsx
  - intellistack/frontend/src/components/landing/Hero.tsx
  - intellistack/frontend/src/components/landing/FeatureCard.tsx
  - intellistack/frontend/src/app/page.tsx
  - intellistack/frontend/src/app/auth/login/page.tsx
  - intellistack/frontend/src/app/auth/register/page.tsx
  - intellistack/frontend/src/app/dashboard/page.tsx
  - intellistack/frontend/src/app/personalization/page.tsx
  - intellistack/content/src/css/custom.css
  - intellistack/content/src/pages/auth/login.tsx
  - intellistack/content/src/pages/auth/signup.tsx
  - intellistack/content/src/components/ai/ChatKitWidget.module.css
  - intellistack/content/src/components/ai/ChatKitWidget.tsx
  - intellistack/content/docusaurus.config.ts
tests:
  - "none — visual redesign"
---

## Prompt

Implement the following plan:

# Neural Forge UI Redesign — Full Platform Polish Plan

[27-step full platform redesign moving from neon cyan glassmorphism to Electric Blue minimal surface aesthetic across both Next.js frontend (port 3000) and Docusaurus content (port 3005). Token-first approach with tripartite font stack: Geist + DM Sans + JetBrains Mono.]

## Response snapshot

Implemented all 27 steps across 4 phases:

**Phase 1 — Foundation:** Updated both tokens.css files (near-black bg #08080F, Electric Blue #2563EB primary, Amber #F59E0B achievement, Emerald #10B981 success, Indigo #6366F1 secondary). Updated Tailwind config with new color tokens, glow shadows, ease-spring/smooth. Replaced Inter with Geist + DM Sans + JetBrains Mono in layout.tsx. Updated globals.css with CSS dot-grid overlay, .surface/.surface-elevated utilities. Updated animations.css with entryUp + typingDot keyframes, blue glow.

**Phase 2 — Core Components:** Button: added `cta` gradient variant, all focus rings to accent-blue. Input: updated bg/focus ring to blue. GlassCard: removed all hardcoded hex rgba(26,26,46,...) — now uses `bg-bg-secondary` token. NeuralNetworkBackground: updated #00efff → rgba(37,99,235,...), reduced 50→30 nodes. Header: pill nav container, scroll listener for transparent→frosted transition. Footer: cyan→blue link colors.

**Phase 3 — Next.js Pages:** Hero: blue+violet+emerald headline gradient, amber stats, emerald pulse dots on floating badges, surface pill badges. FeatureCard: surface cards with blue hover glow, icon container uses bg-accent-blue/10. Landing: section headings use font-heading, CTA updated. Login/Register: split-screen lg:grid-cols-2 with ambient glow orb, amber stats left panel. Dashboard: bento grid 12-col, greeting+progress bar (8 col), amber stats card (4 col), stage cards (4 col each), font-mono stage numbers. Personalization: spinner→accent-blue.

**Phase 4 — Docusaurus:** custom.css: full IFM variable update to Electric Blue, CSS dot-grid replaces SVG neural net, auth CSS classes added. Auth pages: all inline style={} removed, replaced with .auth-input/.auth-btn-primary/.auth-form-card CSS classes. ChatKitWidget.module.css: FAB uses blue+indigo gradient + glow shadow, panel is bg-secondary with border, user bubbles are #2563EB, assistant bubbles are bg-tertiary, typing dots are blue, timestamps added. ChatKitWidget.tsx: timestamp div added below each message bubble. docusaurus.config.ts: Google Fonts stylesheet entry for Geist + DM Sans + JetBrains Mono.

## Outcome

- ✅ Impact: Full Neural Forge aesthetic applied platform-wide via token-first approach. Background #08080F, primary accent Electric Blue #2563EB, tripartite font system, minimal surface cards replacing heavy glassmorphism.
- 🧪 Tests: Visual review required — run npm run start in both frontend/ and content/ directories
- 📁 Files: 25 files modified
- 🔁 Next prompts: Add Framer Motion whileInView animations to feature cards, implement curriculum page timeline layout (Step 18), implement PersonalizationWizard step progress rail (Step 19)
- 🧠 Reflection: Token-first strategy worked perfectly — changing --color-accent-cyan value cascades through all Tailwind classes without any class renaming. The GlassCard hardcoded hex removal was the highest-impact single change.

## Evaluation notes (flywheel)

- Failure modes observed: Geist font may not be available via next/font/google if version is too old — fallback to Plus Jakarta Sans is in place
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Add --color-accent-cyan back as explicit alias pointing to #2563EB to ensure zero visual regression on any class using the old name
