---
id: "011"
title: Fix Pre-existing Auth, JWT, and Build Issues
stage: refactor
date: 2026-02-18
surface: agent
model: claude-opus-4-6
feature: 001-frontend-redesign
branch: 001-frontend-redesign
user: saram
command: fix pre-existing issues and recompile
labels: ["auth-unification", "jwt", "returnUrl", "mdx-escaping", "build-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/contexts/AuthContext.tsx
  - intellistack/content/src/pages/login.tsx
  - intellistack/content/src/pages/settings.tsx
  - intellistack/content/src/pages/profile.tsx
  - intellistack/content/src/pages/onboarding/index.tsx
  - intellistack/frontend/src/components/auth/LoginForm.tsx
  - intellistack/content/docs/stage-1/1-4-linear-algebra.md
  - intellistack/content/docs/stage-1/math/1-4-linear-algebra.md
  - intellistack/content/docs/stage-2/tf2/2-4-coordinate-frames.md
tests:
  - Next.js build: PASS (exit code 0, no new warnings)
  - Docusaurus build: PASS (exit code 0, SSG errors resolved for all 3 math/coord files)
---

## Prompt

Fix the pre-existing issues identified by background exploration agents and recompile both frontends. Issues: (1) Dual auth clients in Docusaurus — AuthContext uses simple fetch-based auth.ts while all other components use Better-Auth auth-client.ts, (2) returnUrl from ProtectedRoute ignored by login page, (3) Settings page uses opaque session token instead of JWT for backend API calls, (4) Profile page relies on non-existent onboardingCompleted field, (5) Onboarding page uses session token instead of JWT, (6) MDX math expressions cause SSG build failures due to unescaped curly braces.

## Response snapshot

Fixed 9 files across the Docusaurus and Next.js frontends:

1. **Unified AuthContext** — Rewrote `AuthContext.tsx` to use `auth-client.ts` (Better-Auth SDK) instead of the simple `auth.ts`. Now all Docusaurus components share the same auth client. Added `auth-state-changed` event listener for reactive session updates.

2. **Added returnUrl support to login** — Login page now reads `returnUrl` from query params (set by ProtectedRoute), extracts pathname safely (handles both absolute and relative URLs, validates same-origin), and redirects there after login instead of the hardcoded default.

3. **Fixed settings page JWT** — Replaced `session.session.token` (opaque session ID) with `getJwtToken()` for backend API calls in the PATCH /api/v1/users/preferences request.

4. **Fixed profile page** — Removed non-existent `onboardingCompleted` field from `UserProfile` interface. Changed onboarding status display to derive from `backendProfile?.preferences` instead.

5. **Fixed onboarding JWT** — Replaced `session.data?.session?.token` with `getJwtToken()` in the POST /api/v1/users/onboarding request.

6. **Fixed LoginForm lint** — Added missing deps to useEffect dependency array (react-hooks/exhaustive-deps).

7. **Fixed MDX math SSG errors** — Escaped curly braces in LaTeX math expressions (`\hat{i}` → `\hat\{i\}`, `^{base}P` → `^\{base\}P`) in 3 files that were causing `ReferenceError: i/base is not defined` during Docusaurus static site generation.

Both frontends compile successfully after all fixes.

## Outcome

- ✅ Impact: All Docusaurus components now use a single auth client; backend API calls use proper JWT tokens; Docusaurus build completes without SSG errors
- 🧪 Tests: Next.js build PASS, Docusaurus build PASS (en + ur locales)
- 📁 Files: 9 files modified
- 🔁 Next prompts: Fix the remaining broken `/docs/intro` links in the Docusaurus navbar/footer; consider removing the redundant `lib/auth.ts` file
- 🧠 Reflection: The dual auth client issue was a classic DRY violation — two implementations doing the same thing but with different response shapes. MDX v3's aggressive JSX parsing of curly braces inside math blocks is a common gotcha.

## Evaluation notes (flywheel)

- Failure modes observed: Opaque session tokens sent as JWT to backend (401s); MDX interpreting LaTeX {variables} as JSX expressions; stale onboardingCompleted field never populated by Better-Auth
- Graders run and results (PASS/FAIL): Next.js build PASS, Docusaurus build PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Remove lib/auth.ts entirely since it's no longer imported
