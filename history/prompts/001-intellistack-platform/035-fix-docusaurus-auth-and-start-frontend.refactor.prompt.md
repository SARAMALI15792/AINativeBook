---
id: 035
title: Fix Docusaurus Auth and Start Frontend Server
stage: refactor
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: continue
labels: ["authentication", "docusaurus", "frontend", "bug-fix", "server-startup"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/lib/auth.ts
  - intellistack/content/src/types/docusaurus.d.ts
  - intellistack/frontend/package.json
tests:
  - Manual: Verified auth.ts loads in Docusaurus browser environment
  - Manual: Verified Next.js dev server starts successfully
  - Manual: Confirmed server running at http://localhost:3000
---

## Prompt

User requested to continue from previous session where Frontend Redesign reached 76.7% completion. Encountered two critical errors:

1. "process is not defined" error in Docusaurus auth.ts
2. "betterAuth is not a function" error after first fix
3. Request to start Next.js frontend development server

## Response snapshot

**Fixed Docusaurus Authentication Issues:**

1. **First Error - "process is not defined":**
   - Root cause: Docusaurus runs in browser, doesn't have access to Node.js process.env
   - Solution: Changed auth.ts to use `window.docusaurus.siteConfig.customFields` instead of process.env
   - Created TypeScript declarations in docusaurus.d.ts for type safety

2. **Second Error - "betterAuth is not a function":**
   - Root cause: better-auth/client library not compatible with Docusaurus webpack configuration
   - Solution: Replaced Better Auth client library with custom Fetch API implementation
   - Created custom authClient object with getSession() and signOut() methods
   - No external dependencies, uses native browser Fetch API

**Final Working Implementation:**
```typescript
const getConfig = () => {
  if (typeof window !== 'undefined' && window.docusaurus) {
    return {
      betterAuthUrl: window.docusaurus.siteConfig.customFields?.betterAuthUrl as string || 'http://localhost:3001',
      isProduction: window.location.hostname !== 'localhost',
    };
  }
  return { betterAuthUrl: 'http://localhost:3001', isProduction: false };
};

export const authClient = {
  baseURL: config.betterAuthUrl,
  async getSession() {
    const response = await fetch(`${this.baseURL}/api/auth/session`, { credentials: 'include' });
    if (!response.ok) return null;
    const data = await response.json();
    return data.user || null;
  },
  async signOut() {
    const response = await fetch(`${this.baseURL}/api/auth/signout`, { method: 'POST', credentials: 'include' });
    if (!response.ok) throw new Error('Logout failed');
    return await response.json();
  }
};
```

**Started Next.js Frontend Server:**

1. Installed dependencies with `npm install --legacy-peer-deps` (resolved vitest conflict)
2. Started dev server with `npm run dev`
3. Server successfully running at http://localhost:3000
4. Next.js 14.2.35 ready in 25.1s

## Outcome

- ✅ Impact: Fixed critical authentication errors blocking Docusaurus integration, successfully started frontend development server
- 🧪 Tests: Manual verification of auth client in browser, server startup confirmed
- 📁 Files: Modified 2 files (auth.ts, docusaurus.d.ts), installed dependencies
- 🔁 Next prompts: Test frontend features, run Lighthouse audits, complete accessibility testing
- 🧠 Reflection: Browser environment limitations require careful consideration when integrating libraries. Custom Fetch API implementation proved more reliable than external auth library for Docusaurus.

## Evaluation notes (flywheel)

- Failure modes observed: process.env not available in browser, webpack compatibility issues with Better Auth client library
- Graders run and results (PASS/FAIL): Manual testing PASS - auth client works in browser, server starts successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test cross-platform authentication flow between Next.js and Docusaurus with shared cookies
