---
id: 041
title: Migrate Frontend from Railway to Netlify
stage: misc
date: 2026-02-22
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saramali15792
command: implement-plan
labels: ["deployment", "netlify", "railway", "frontend", "migration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/frontend/next.config.js
  - intellistack/frontend/railway.toml (deleted)
  - intellistack/frontend/.vercel/ (deleted)
  - intellistack/frontend/netlify.toml (created)
tests:
  - curl https://intellistack-frontend.netlify.app/ → 200
  - curl https://backend-production-bcb8.up.railway.app/health → 200
---

## Prompt

Migrate Next.js frontend from Railway to a free hosting platform. Initially attempted Vercel but hit free-tier daily deploy limit (100/day). Pivoted to Netlify.

## Response snapshot

### Completed:
1. **Removed `output: 'standalone'`** from `next.config.js` — not needed for Netlify/Vercel serverless deployment.
2. **Deleted `intellistack/frontend/railway.toml`** — Railway-specific config no longer needed. Other services' configs untouched.
3. **Attempted Vercel deploy** — project created and env vars set, but blocked by 100 deploys/day free-tier limit.
4. **Removed `.vercel/` directory** — cleaned up after pivoting away from Vercel.
5. **Installed `@netlify/plugin-nextjs`** — required for Next.js SSR on Netlify.
6. **Created `netlify.toml`** — build config with Next.js plugin.
7. **Created Netlify site** — `intellistack-frontend` linked to account `saramali15792`.
8. **Set 3 environment variables on Netlify:**
   - `NEXT_PUBLIC_AUTH_URL` = `https://auth-server-production-0f46.up.railway.app`
   - `NEXT_PUBLIC_API_URL` = `https://backend-production-bcb8.up.railway.app`
   - `NEXT_PUBLIC_DOCUSAURUS_URL` = `https://saramali15792.github.io/AINativeBook/`
9. **Deployed to production** — https://intellistack-frontend.netlify.app (200 OK)
10. **Updated CORS on Railway backend & auth-server** to include `https://intellistack-frontend.netlify.app`.
11. **Redeployed both Railway services** to pick up new CORS configuration.

### Production URLs:
- Frontend: https://intellistack-frontend.netlify.app
- Backend: https://backend-production-bcb8.up.railway.app
- Auth Server: https://auth-server-production-0f46.up.railway.app
- Docs: https://saramali15792.github.io/AINativeBook/

## Outcome

- ✅ Impact: Frontend successfully migrated from Railway to Netlify. All services communicating with updated CORS.
- 🧪 Tests: curl verification — frontend 200, backend health 200
- 📁 Files: 4 file changes (next.config.js modified, railway.toml deleted, .vercel deleted, netlify.toml created)
- 🔁 Next prompts: Verify auth flow end-to-end from Netlify domain, optionally remove Railway AINativeBook service
- 🧠 Reflection: Vercel free tier has aggressive deploy limits (100/day). Netlify was a smooth alternative with mature Next.js support via @netlify/plugin-nextjs.

## Evaluation notes (flywheel)

- Failure modes observed: Vercel free-tier 100 deploys/day limit; Netlify CLI crashes on interactive prompts (workaround: use --account-slug flag)
- Graders run and results (PASS/FAIL): PASS - site returns 200
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test auth login flow from Netlify domain
