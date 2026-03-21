---
id: "033"
title: Deploy Docusaurus to GitHub Pages with CI/CD
stage: general
date: 2026-03-22
surface: agent
model: claude-sonnet-4-6
feature: none
branch: main
user: salim
command: plan + implement deploy-docs workflow
labels: ["deployment", "ci-cd", "github-actions", "docusaurus", "github-pages", "railway"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .github/workflows/deploy-docs.yml
tests:
  - Manual: push to main → verify GitHub Actions run → verify site at https://saramali15792.github.io/AINativeBook/
---

## Prompt

ok now i want you to make an plan to deploy the docusours to te github sue the skills docusaurus-deployer and also make sure that use the CI/CD pipeline for this deployment to the github and and then weill deployed our the foretend and backend and the auth server and other sercives so can u make an plan and also tell me that how can u delpoy this whole projects

## Response snapshot

Created `.github/workflows/deploy-docs.yml` — a GitHub Actions CI/CD pipeline that:
- Triggers on push to `main` with `paths:` filter for `intellistack/content/**`
- Jobs: build (Node 20, npm ci, typecheck, build) → deploy (GitHub Pages artifact upload)
- Uses `actions/upload-pages-artifact@v3` + `actions/deploy-pages@v4` (latest)
- `docusaurus.config.ts` required no changes — already correctly configured for GitHub Pages

Full platform deployment strategy documented in plan:
- Docusaurus → GitHub Pages (automated via this workflow)
- FastAPI backend → Railway (manual setup, Dockerfile at intellistack/backend/Dockerfile)
- Better-Auth server → Railway (manual setup, Dockerfile at intellistack/auth-server/Dockerfile)
- PostgreSQL → Neon (already in use)
- Qdrant → Qdrant Cloud (already in use)
- Redis → Railway addon

## Outcome

- ✅ Impact: First CI/CD pipeline in the project; Docusaurus auto-deploys on every push to main that touches content
- 🧪 Tests: Push a docs change to main, check Actions tab, verify site loads at https://saramali15792.github.io/AINativeBook/
- 📁 Files: .github/workflows/deploy-docs.yml (created)
- 🔁 Next prompts: Configure GitHub Pages in repo Settings → Pages → Source: GitHub Actions; update customFields in docusaurus.config.ts with Railway URLs; set up Railway services for backend + auth-server
- 🧠 Reflection: The Docusaurus config was already production-ready (correct url/baseUrl/org/projectName). The only missing piece was the workflow file. Used v3/v4 of Pages actions instead of the skill template's v2 to avoid deprecation failures.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment: Add deploy-backend.yml and deploy-auth.yml workflows using Railway CLI for full CI/CD
