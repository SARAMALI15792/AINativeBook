---
id: 1002
title: Railway Deployment Migration Implementation
stage: misc
date: 2026-02-21
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: implement
labels: ["deployment", "railway", "infrastructure", "migration", "devops"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - render.yaml (deleted)
  - .github/workflows/deploy.yml (deleted)
  - railway.toml (created)
  - intellistack/backend/railway.toml (created)
  - intellistack/auth-server/railway.toml (created)
  - intellistack/content/railway.toml (created)
  - .github/workflows/railway-deploy.yml (created)
  - RAILWAY_DEPLOYMENT.md (created)
  - RAILWAY_NEXT_STEPS.md (created)
  - setup-railway.sh (created)
  - setup-railway.bat (created)
  - railway-credentials.sh (created, gitignored)
  - .gitignore (updated)
tests:
  - Manual verification required after Railway deployment
---

## Prompt

Implement the following plan:

# Railway Deployment Migration Plan

## Context

The user wants to migrate from Render to Railway for deploying the IntelliStack Platform. The project consists of multiple services:
- **Backend API** (FastAPI/Python) - currently has Dockerfile at `intellistack/docker/backend.Dockerfile`
- **Auth Server** (Better-Auth/Node.js) - has Dockerfile at `intellistack/auth-server/Dockerfile`
- **Content Site** (Docusaurus) - static site
- **Frontend** (Next.js) - static export (currently removed from repo)
- **Redis** - managed service
- **PostgreSQL** - external (Neon)
- **Qdrant** - external (Qdrant Cloud)

[Full plan details provided by user...]

## Response snapshot

Successfully migrated IntelliStack Platform from Render to Railway deployment:

### Phase 1: Removed Render Files
- Deleted `render.yaml` configuration
- Deleted `.github/workflows/deploy.yml` (Render-specific workflow)

### Phase 2: Created Railway Configuration
- Created `railway.toml` (monorepo root configuration)
- Created `intellistack/backend/railway.toml` (FastAPI service with Dockerfile build)
- Created `intellistack/auth-server/railway.toml` (Better-Auth service with Dockerfile build)
- Created `intellistack/content/railway.toml` (Docusaurus static site with Nixpacks)

### Phase 3: Created GitHub Actions CI/CD
- Created `.github/workflows/railway-deploy.yml` with path-based change detection
- Configured automatic deployment on push to main branch
- Set up parallel deployment jobs for backend, auth-server, and content services

### Phase 4: Created Documentation
- Created `RAILWAY_DEPLOYMENT.md` - comprehensive deployment guide with:
  - Prerequisites and initial setup instructions
  - Environment variable reference tables
  - Railway CLI commands for all operations
  - Monitoring and troubleshooting guides
  - Cost estimation
  - Service reference syntax documentation

### Phase 5: Collected Credentials
- User provided: DATABASE_URL, QDRANT_HOST, QDRANT_API_KEY, OPENAI_API_KEY
- Generated secure secrets:
  - SECRET_KEY: `nMtFNk9t8b-Xd--skOZhzOlQavkjc18bOPQf-hKHTWM`
  - BETTER_AUTH_SECRET: `XSkx1wWU6051ttlH7DQ9o_5cIhGEtmhXIXz0htELjQU`

### Phase 6: Created Setup Scripts
- Created `setup-railway.sh` (Linux/Mac) and `setup-railway.bat` (Windows)
- Scripts automate: project creation, service creation, Redis provisioning
- Prompts user to set environment variables manually (security best practice)
- Handles service reference linking and deployment

### Phase 7: Security Handling
- Encountered GitHub push protection (detected OpenAI API key in scripts)
- Removed hardcoded credentials from setup scripts
- Created `railway-credentials.sh` for local credential management (gitignored)
- Updated `.gitignore` to exclude credential files
- Amended commit to remove secrets before pushing

### Phase 8: Git Operations
- Committed all changes with descriptive message
- Successfully pushed to GitHub (commit: 461f5dc)
- Created `RAILWAY_NEXT_STEPS.md` with step-by-step manual instructions

## Outcome

- ✅ Impact: Complete migration from Render to Railway with secure credential handling, automated CI/CD, and comprehensive documentation
- 🧪 Tests: Manual verification required after Railway deployment (health checks, service connectivity)
- 📁 Files: 13 files modified (2 deleted, 10 created, 1 updated)
- 🔁 Next prompts: User needs to run `railway login` and execute `setup-railway.sh` or `setup-railway.bat` to complete deployment
- 🧠 Reflection: Successfully handled GitHub push protection by removing hardcoded secrets and creating secure local credential management. Railway's service reference syntax (`${{service.VARIABLE}}`) provides elegant cross-service communication.

## Evaluation notes (flywheel)

- Failure modes observed: GitHub push protection blocked initial push due to hardcoded API keys in setup scripts. Resolved by removing credentials and creating gitignored credential file.
- Graders run and results (PASS/FAIL): N/A - deployment verification pending user execution of setup scripts
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): After successful Railway deployment, consider creating Railway project template or Terraform configuration for infrastructure-as-code approach
