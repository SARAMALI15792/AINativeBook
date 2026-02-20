---
id: 1002
title: Render Deployment Implementation
stage: general
date: 2026-02-20
surface: agent
model: claude-opus-4-6
feature: none
branch: main
user: saram
command: implement
labels: ["deployment", "render", "ci-cd", "infrastructure"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/requirements.txt
  - intellistack/docker/backend.Dockerfile
  - intellistack/auth-server/Dockerfile
  - intellistack/content/docusaurus.config.ts
  - render.yaml
  - .github/workflows/deploy.yml
tests:
  - none
---

## Prompt

Implement the following plan:

# Deployment Plan: IntelliStack on Render (Free Tier)

All previous deployment configs (Vercel, Railway, GitHub Pages) were removed in commit ed9ce04. This plan establishes a fresh deployment strategy using Render as the single platform, with Neon for PostgreSQL and Qdrant Cloud for vector search.

Steps: Remove mangum, fix Dockerfile port handling, update Docusaurus config, create render.yaml Blueprint, create GitHub Actions CI/CD workflow.

## Response snapshot

Implemented all 6 steps of the Render deployment plan:

1. **Removed mangum** from `intellistack/backend/requirements.txt` (Vercel serverless adapter no longer needed)
2. **Fixed backend Dockerfile** (`intellistack/docker/backend.Dockerfile`): Changed CMD to shell form with `${PORT:-8000}` and updated HEALTHCHECK to use dynamic port
3. **Fixed auth server Dockerfile** (`intellistack/auth-server/Dockerfile`): Updated HEALTHCHECK to use `${PORT:-3001}` instead of hardcoded port
4. **Updated Docusaurus config** (`intellistack/content/docusaurus.config.ts`): Changed url to use `SITE_URL` env var with Render default, changed baseUrl from `/docs/` to `/`
5. **Created render.yaml** Blueprint at project root defining 5 services: backend (Docker), auth (Docker), content (static), frontend (static), Redis
6. **Created `.github/workflows/deploy.yml`** with path-filtered jobs using Render Deploy Hooks (requires 4 GitHub secrets)

## Outcome

- Impact: Full Render deployment infrastructure configured
- Tests: none (infrastructure config changes)
- Files: 4 modified, 2 created
- Next prompts: Set up Neon PostgreSQL, Qdrant Cloud, add GitHub secrets for deploy hooks, deploy via Render Blueprint
- Reflection: Clean implementation following the plan exactly. The render.yaml uses sync:false for secrets that must be manually configured on Render dashboard.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
