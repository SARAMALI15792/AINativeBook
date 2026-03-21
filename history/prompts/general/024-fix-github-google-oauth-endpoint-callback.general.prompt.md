---
name: Fix GitHub/Google OAuth Endpoint and Callback URL
description: Fixed wrong Better-Auth social sign-in endpoint and missing baseUrl in OAuth callback URL for GitHub and Google OAuth
type: general
stage: general
date: 2026-03-21
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
labels: ["bug-fix", "oauth", "auth", "github", "google", "better-auth"]
---

## Prompt

when i singup with gtihub it shows me this erros the same wiht the google no i want you to fix this issue ::3001/favicon.ico:1  Failed to load resource: the server responded with a status of 404 (Not Found)

## Response

Identified and fixed two root causes for OAuth sign-in failing with GitHub and Google:

### Bug 1: Wrong Better-Auth endpoint in `lib/auth.ts`
The `signInWithOAuth` method was calling `/api/auth/oauth/${provider}` which does not exist in Better-Auth. The correct endpoint is `/api/auth/sign-in/social` with body `{ provider, callbackURL }`.

### Bug 2: Wrong callback URL path (missing Docusaurus baseUrl)
All OAuth handlers in `signup.tsx` and `login.tsx` built the callback URL as `${window.location.origin}/auth/callback`, but Docusaurus runs at baseUrl `/AINativeBook/`. The callback page is actually at `${origin}/AINativeBook/auth/callback`.

### Files modified
- `intellistack/content/src/lib/auth.ts` — fixed endpoint + body shape
- `intellistack/content/src/pages/auth/signup.tsx` — fixed callback URL (Google + GitHub handlers)
- `intellistack/content/src/pages/auth/login.tsx` — fixed callback URL (Google + GitHub handlers)

### Note for GitHub/Google OAuth App settings
The OAuth provider console must whitelist the auth-server callback URL:
- GitHub: `http://localhost:3001/api/auth/callback/github`
- Google: `http://localhost:3001/api/auth/callback/google`
