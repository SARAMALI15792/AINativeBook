---
name: analyze-codebase
description: >
  Produces a complete structural analysis of the IntelliStack codebase —
  modules, API surface, database schema, auth flows, and RAG pipeline —
  as a human-readable export map that any developer can use as a migration
  blueprint regardless of their target framework.
license: MIT
allowed-tools: read_file, list_directory, search_code
metadata:
  author: IntelliStack Team
  version: "1.0.0"
  category: analysis
---

# Skill: Analyze Codebase

## Purpose
Generate a complete picture of IntelliStack so a developer can understand
what they are migrating before writing a single line of code.

## Instructions

When invoked, produce a structured report with the following sections:

### 1. Module Map
List every module under `intellistack/backend/src/core/` with:
- Module name
- Responsibility (one sentence)
- Key files (routes, service, models, schemas)
- External dependencies (Redis, Qdrant, OpenAI, etc.)

### 2. API Surface
For every router file, list:
- HTTP method + path
- Auth requirement (public / JWT required / admin only)
- Request body shape (Pydantic schema name)
- Response shape (Pydantic schema name)
- Side effects (DB writes, cache invalidation, vector upsert, etc.)

### 3. Database Schema
For every SQLAlchemy model, list:
- Table name
- Columns (name, type, nullable, default, constraints)
- Relationships (FK targets, cascade rules)
- Indexes

### 4. Auth Flow
Describe:
- Session lifecycle (login → token → refresh → logout)
- OAuth providers (Google, GitHub) and their callback routes
- JWT claims structure
- Role/permission matrix

### 5. RAG Pipeline
Describe:
- Ingestion flow (document → chunking → embedding → Qdrant upsert)
- Retrieval flow (query → dense+sparse retrieval → Cohere rerank → LLM)
- Streaming (SSE event shape, error events)
- Citation structure

### 6. Environment Variables
List every `os.getenv` / `settings.*` reference with:
- Variable name
- Purpose
- Example value (never real secrets)
- Required or optional

### 7. Migration Readiness Score
Rate each layer (1–5) on migration complexity:
- Backend routes
- Business logic / services
- Database models
- Auth system
- RAG pipeline
- Frontend API contract

## Output Format
Markdown with clear H2/H3 headings. Include source file references
(e.g., `intellistack/backend/src/core/auth/routes.py:12`) for every claim.
