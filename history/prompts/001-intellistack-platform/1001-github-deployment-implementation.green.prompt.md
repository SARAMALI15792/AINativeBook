---
id: 1001
title: GitHub-Only Deployment Implementation
stage: green
date: 2026-02-20
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: implement deployment plan
labels: ["deployment", "github-pages", "github-actions", "docker", "ci-cd"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .github/workflows/deploy-pages.yml (created)
  - .github/workflows/deploy-backend.yml (created)
  - .github/workflows/deploy-auth.yml (created)
  - intellistack/frontend/next.config.js (modified)
  - intellistack/frontend/public/404.html (created)
  - intellistack/frontend/.env.production (created)
  - intellistack/frontend/src/app/layout.tsx (modified)
  - intellistack/content/docusaurus.config.ts (modified)
  - intellistack/backend/src/config/settings.py (modified)
  - intellistack/auth-server/src/index.ts (modified)
  - .github/workflows/deploy.yml.disabled (deleted)
tests:
  - Manual verification of workflow YAML syntax
  - Verified no getServerSideProps or next/image usage blocking static export
---

## Prompt

Implement the GitHub-Only Deployment Plan: Configure Next.js for static export, set up Docusaurus for /docs/ path, create GitHub Actions workflows for Pages deployment (frontend + docs), backend Docker build + Railway deploy, and auth server Docker build + Railway deploy. Update CORS origins, create 404.html SPA redirect, and add .env.production.

## Response snapshot

Implemented 9 changes across the codebase:

1. **next.config.js** - Enabled `output: 'export'`, `trailingSlash: true`, `unoptimized: true` images, removed Vercel-specific rewrites
2. **docusaurus.config.ts** - Changed `baseUrl` to `/docs/`, fixed duplicate `markdown` key, updated `projectName`/`organizationName` to match repo, fixed footer links to use relative paths
3. **deploy-pages.yml** - Combined workflow that builds Next.js static export + Docusaurus, merges into single site, deploys via `actions/deploy-pages@v4` with proper permissions and concurrency
4. **deploy-backend.yml** - Builds Docker image from backend.Dockerfile, pushes to GHCR, deploys to Railway with health check
5. **deploy-auth.yml** - Builds Docker image from auth-server Dockerfile, pushes to GHCR, deploys to Railway with health check
6. **404.html** - SPA redirect script for GitHub Pages that preserves client-side routing paths
7. **layout.tsx** - Added SPA redirect receiver script in `<head>`, updated Docusaurus URL default
8. **.env.production** - Production environment variables with Railway URL placeholders
9. **CORS updates** - Added `https://saramali15792.github.io` to default origins in backend settings.py and auth-server index.ts

## Outcome

- Impact: Full GitHub-maximum deployment infrastructure created. Static sites deploy to GitHub Pages, backend services build Docker images to GHCR and deploy to Railway.
- Tests: YAML syntax verified, no SSR blockers found in frontend code
- Files: 11 files created/modified/deleted
- Next prompts: Enable GitHub Pages in repo settings (source: GitHub Actions), create Railway services, set GitHub Environment secrets, push to trigger first deployment
- Reflection: The plan was well-structured. Key decisions: using `actions/deploy-pages@v4` (newer API-based deployment vs older branch-based), path-filtered triggers for efficiency, graceful Railway deploy skip when token not set.

## Evaluation notes (flywheel)

- Failure modes observed: None during implementation. Potential: npm ci may fail if lock files are stale.
- Graders run and results (PASS/FAIL): Manual review PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Push to main and verify GitHub Actions triggers correctly
