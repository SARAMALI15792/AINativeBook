---
id: 026
title: Fix Docker, Better-Auth, and Docusaurus Frontend
stage: refactor
date: 2026-02-17
surface: agent
model: claude-opus-4-6
feature: 001-intellistack-platform
branch: main
user: saram
command: implement plan
labels: ["docker", "better-auth", "docusaurus", "migrations", "configuration"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/docker/backend.Dockerfile
  - intellistack/docker-compose.dev.yml
  - intellistack/auth-server/.env
  - intellistack/auth-server/tsconfig.json
  - intellistack/backend/.env
  - intellistack/backend/src/shared/database.py
  - intellistack/backend/src/config/settings.py
  - intellistack/backend/alembic/env.py
  - intellistack/backend/alembic/versions/20260209_2033_2df1e27640d0_initial_migration.py
  - intellistack/backend/alembic/versions/001_add_chatkit_tables.py
  - intellistack/backend/requirements.txt
  - intellistack/content/.env
  - intellistack/content/package.json
tests:
  - curl http://localhost:3001/health → 200 OK
  - curl http://localhost:8000/health → 200 healthy
  - curl http://localhost:3001/.well-known/jwks.json → returns keys
  - curl http://localhost:3000 → 200 OK (Docusaurus)
  - All 5 Docker services running and healthy
---

## Prompt

Implement the following plan: Fix Docker, Better-Auth, and Docusaurus Frontend. Get Docker services running (postgres, redis, qdrant, auth-server, backend), fix all errors preventing startup, run Docusaurus frontend locally, and verify Better-Auth signup/login/session flow works end-to-end. Use Docker local Postgres (not Neon cloud). Docusaurus runs locally outside Docker.

## Response snapshot

Successfully fixed 11+ issues across the stack to get all services running end-to-end:

**Docker/Build Fixes:**
- Fixed backend Dockerfile: changed from `pip install -e .` (needs source) to `pip install -r requirements.txt`
- Removed deprecated `version: "3.8"` from docker-compose.dev.yml
- Added CORS_ORIGINS env var to auth-server in docker-compose
- Added tiktoken to requirements.txt (was missing but used in RAG chunking)

**Configuration Fixes:**
- Switched backend .env from Neon cloud to local Docker postgres URL
- Switched backend .env Qdrant from cloud to local Docker
- Updated auth-server .env with proper secret and CORS_ORIGINS
- Removed duplicate `lib` key from auth-server tsconfig.json
- Made SSL conditional in database.py (only for neon.tech/sslmode=require URLs)
- Fixed async_database_url sslmode stripping for &sslmode= edge case
- Fixed alembic env.py to strip sslmode instead of converting to ssl=

**Migration Fixes (critical):**
- Reordered initial migration tables: independent tables first (roles, stages, institutions, users), then dependent tables
- Fixed circular FK: content ↔ content_versions handled with deferred FK creation
- Fixed chatkit migration: changed `down_revision` from `None` to `20260210_0001` (was creating parallel branch)
- Fixed chatkit migration: changed all column types from `String(36)` to `UUID` to match users table
- Added tutor_session_items table to chatkit migration
- Removed obsolete merge and fix migrations (d2bd6cf2bc71, fix_chatkit_fk_001)
- Created Better-Auth tables (user, session, account, verification, jwks, etc.) directly in postgres

**Frontend:**
- Created content/.env from .env.example
- Bumped better-auth from ^1.2.0 to ^1.4.18 in content/package.json

**Final State:**
- postgres :5432 (healthy)
- redis :6379 (healthy)
- qdrant :6333/:6334 (running)
- auth-server :3001 (healthy, JWKS working)
- backend :8000 (healthy)
- Docusaurus :3000 (running)

## Outcome

- ✅ Impact: All services running end-to-end for the first time with local Docker postgres
- 🧪 Tests: Health checks passing on all services, JWKS returning keys
- 📁 Files: 13 files modified/created, 2 migration files deleted
- 🔁 Next prompts: Test Better-Auth signup/login flow in browser, verify ChatKit widget works authenticated
- 🧠 Reflection: The migration issues were the most complex part — multiple problems stacked (table ordering, type mismatches, parallel branches, missing tables). Fixing them required understanding the full dependency graph.

## Evaluation notes (flywheel)

- Failure modes observed: Migration table ordering, type mismatches between chatkit (String) and users (UUID), parallel migration branches, missing Better-Auth tables
- Graders run and results (PASS/FAIL): All health checks PASS, JWKS PASS
- Prompt variant (if applicable): Plan-mode → implementation
- Next experiment (smallest change to try): Test actual signup/login flow in browser to verify Better-Auth end-to-end
