---
id: "031"
title: Fix Frontend Build Type Errors
stage: general
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: "continue to activate the commands"
labels: ["frontend", "typescript", "build", "bugfix", "next.js", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/components/personalization/ExperienceLevelSelector.tsx
  - intellistack/frontend/src/components/personalization/LearningGoalSelector.tsx
  - intellistack/frontend/src/lib/api-client.ts
tests:
  - npm run build (Next.js — pass)
  - npm run build (Docusaurus — pass, both en + ur locales)
---

## Prompt

continue to activate the commands (run npm install, npm run build, npm start across frontend and content sites)

## Response snapshot

Fixed 4 pre-existing TypeScript type errors that blocked the Next.js build after the Frontend Polish & Redesign implementation:

1. `ExperienceLevelSelector.tsx:84` — removed `opacity={0.7}` from `<GlassCard>` (prop not in GlassCardProps interface)
2. `LearningGoalSelector.tsx:80` — removed `opacity={0.7}` from `<GlassCard>` (same issue)
3. `api-client.ts:53` — changed `client.getJwtToken()` → standalone `getJwtToken()` imported from `@/lib/auth` (Better Auth client object doesn't have this method; it's an exported function)

Next.js: ✓ Compiled successfully
Docusaurus: ✓ Generated static files in "build" (en + ur locales)

## Outcome

- ✅ Impact: Both frontend sites now build cleanly; Frontend Polish & Redesign implementation fully activated
- 🧪 Tests: npm run build passing on both sites
- 📁 Files: 3 files patched (2 GlassCard opacity props removed, 1 api-client auth import fixed)
- 🔁 Next prompts: Run dev servers; continue with Phase 7 AI Tutor tasks
- 🧠 Reflection: These errors were pre-existing type drift — GlassCard's interface never declared opacity but callers passed it anyway, silently working at runtime but failing strict TS build check

## Evaluation notes (flywheel)

- Failure modes observed: Repeated opacity prop pattern across multiple personalization components — suggests original author was passing unsupported props
- Graders run and results (PASS/FAIL): npm run build PASS (Next.js), npm run build PASS (Docusaurus)
- Prompt variant (if applicable): null
- Next experiment: Add opacity support to GlassCardProps if the visual effect is needed, or use CSS class approach
