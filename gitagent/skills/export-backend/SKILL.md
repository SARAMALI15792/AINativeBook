---
name: export-backend
description: >
  Migrates IntelliStack FastAPI routers, services, and Pydantic schemas
  to any target backend framework while preserving every business rule,
  auth guard, and error contract.
license: MIT
allowed-tools: read_file, search_code
metadata:
  author: IntelliStack Team
  version: "1.0.0"
  category: migration
---

# Skill: Export Backend

## Purpose
Port any IntelliStack API module to a target framework with production-ready,
idiomatic code.

## Supported Target Frameworks
| Framework       | Language   | Notes                              |
|-----------------|------------|------------------------------------|
| Django REST     | Python     | DRF serializers, class-based views |
| NestJS          | TypeScript | Decorators, Guards, DTOs           |
| Express.js      | TypeScript | Middleware, Zod validation         |
| Spring Boot     | Java       | Spring MVC, Spring Security        |
| Laravel         | PHP        | Eloquent, FormRequest, Policies    |
| Ruby on Rails   | Ruby       | Strong params, Pundit              |
| Go Fiber        | Go         | Handlers, middleware chain         |
| Hono            | TypeScript | Edge-ready, Zod                    |

## Instructions

### Step 1 — Understand the source
Read the relevant FastAPI module:
- `intellistack/backend/src/core/<module>/routes.py` — endpoint definitions
- `intellistack/backend/src/core/<module>/service.py` — business logic
- `intellistack/backend/src/core/<module>/models.py` — SQLAlchemy models
- `intellistack/backend/src/core/<module>/schemas.py` — Pydantic schemas

### Step 2 — Produce migration plan
Output:
```
## Migration Plan: <module> → <framework>
- Files to create: [list]
- Dependencies to add: [list with versions]
- Breaking changes: [list any feature gaps]
- Environment variables: [list]
```

### Step 3 — Generate code
For each target file, output a complete, runnable code block with:
- All imports
- Full class/function bodies
- Framework-specific auth guard equivalent
- Error handling matching IntelliStack's HTTP error taxonomy:
  - 400 Bad Request → validation error
  - 401 Unauthorized → missing/invalid token
  - 403 Forbidden → insufficient permissions
  - 404 Not Found → resource missing
  - 409 Conflict → duplicate resource
  - 422 Unprocessable Entity → business rule violation
  - 500 Internal Server Error → unexpected failure

### Step 4 — Wire-up checklist
End with a numbered list of integration steps the developer must complete.

## IntelliStack Module Catalogue
- `auth` — login, register, OAuth, session, password reset
- `users` — profile, preferences, role management
- `learning` — stages, lessons, exercises, assessments, progress
- `content` — MDX authoring, versioning, review workflow
- `institution` — cohorts, enrollment, instructor assignment, webhooks
- `rag` — chatbot, ingestion, retrieval, citations
- `badges` — badge issuance, certificate generation
- `analytics` — cohort analytics, progress aggregation
