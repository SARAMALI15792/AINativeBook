---
id: 021
title: Better-Auth Cross-Origin Cookie Research
stage: explainer
date: 2026-02-19
surface: agent
model: claude-sonnet-4-6
feature: 001-frontend-redesign
branch: 001-frontend-redesign
user: saram
command: research
labels: ["better-auth", "cross-origin", "cookies", "createAuthClient", "CORS"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/content/src/lib/auth-client.ts
  - intellistack/auth-server/src/auth.ts
  - intellistack/content/src/contexts/AuthContext.tsx
tests:
  - none (research only)
---

## Prompt

I need to understand how `createAuthClient` from `better-auth/react` handles cross-origin cookie sending. Specifically:

1. Does `createAuthClient` automatically set `credentials: 'include'` on fetch requests when the baseURL is a different origin?
2. What configuration is needed for cross-origin session cookie validation?

Search for the latest Better-Auth documentation on cross-origin configuration, cookie handling, and the `createAuthClient` options.

Use Context7 to find the Better-Auth library and query its docs about:
- Cross-origin/cross-domain cookie configuration
- `createAuthClient` fetch options for credentials
- How to configure the client for a different-origin auth server

Only do research - do not write any code.

## Response snapshot

Research findings via Context7 Better-Auth documentation:

1. **createAuthClient does NOT automatically set credentials: 'include'** -- it uses better-fetch internally which defaults to browser's same-origin credential policy. Cross-origin requests require explicit `fetchOptions: { credentials: 'include' }`.

2. **Cross-origin configuration requires both client and server changes:**
   - Client: `credentials: 'include'` in fetchOptions or customFetchImpl
   - Server: `trustedOrigins` array, CORS with `credentials: true`, proper cookie `sameSite`/`domain` attributes

3. **Current project gap identified:** `auth-client.ts` customFetchImpl passes `init` to fetch() without injecting `credentials: 'include'`, causing cookies to not be sent cross-origin (frontend :3000 -> auth server :3001).

4. **Three cross-origin scenarios documented:** same-host-different-port, subdomains (crossSubDomainCookies), completely different domains (sameSite: none + partitioned or reverse proxy).

5. **Safari ITP warning:** Third-party cookie blocking requires reverse proxy or shared parent domain.

## Outcome

- Impact: Identified root cause of potential cross-origin auth failures; documented exact config gap in auth-client.ts
- Tests: none (research only)
- Files: Read auth-client.ts, auth.ts, AuthContext.tsx for current state analysis
- Next prompts: Fix auth-client.ts to include credentials: 'include' in customFetchImpl
- Reflection: Context7 provided comprehensive Better-Auth docs covering all three cross-origin scenarios; project has server-side config correct but client-side missing credentials include

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A (research task)
- Prompt variant (if applicable): N/A
- Next experiment: Apply credentials: 'include' fix and verify session persistence across origins
