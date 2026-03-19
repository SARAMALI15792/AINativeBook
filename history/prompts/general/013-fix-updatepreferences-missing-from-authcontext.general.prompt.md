---
id: 013
title: Fix updatePreferences Missing from AuthContext
stage: general
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: fix TypeError updatePreferences is not a function
labels: ["bug","auth","context","personalization","typescript"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/src/contexts/AuthContext.tsx
tests:
  - manual: PersonalizationWizard completes without TypeError
---

## Prompt

Console error: TypeError: updatePreferences is not a function at handleComplete (page.tsx:48:13)

## Response snapshot

Root cause: `personalization/page.tsx` destructures `updatePreferences` from `useAuth()`, but `AuthContextType` never declared it and `AuthProvider` never provided it — so the destructured value was `undefined`.

Fix: Added `updatePreferences: (preferences: PersonalizationPreferences) => Promise<void>` to `AuthContextType` interface, implemented it in `AuthProvider` by delegating to the existing `apiClient.updatePreferences()`, and included it in the context value object.

## Outcome

- ✅ Impact: PersonalizationWizard `handleComplete` no longer throws; preferences are POSTed to `/users/preferences/onboarding`
- 🧪 Tests: Manual — complete the wizard and verify no console error
- 📁 Files: 1 file modified (AuthContext.tsx)
- 🔁 Next prompts: Verify backend 401/403 handling if auth token is absent when wizard completes
- 🧠 Reflection: Context drift — consumer code was written expecting a method that was never added to the context interface. TypeScript would have flagged this if the page used a typed destructure rather than relying on runtime behavior.

## Evaluation notes (flywheel)

- Failure modes observed: missing method in context value
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): none
- Next experiment: Add a unit test that asserts all AuthContextType methods are present in the provider value
