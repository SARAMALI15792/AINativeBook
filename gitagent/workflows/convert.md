# Workflow: Convert IntelliStack to Any Framework / Language

This is the main entry-point workflow for the IntelliStack Export Agent.
Run it whenever a developer wants to port the entire platform — or just one
layer — to their preferred language or framework.

---

## How to Start

Ask the agent in plain language. Examples:

```
"Convert IntelliStack to Django + React"
"Port only the auth layer to NestJS with Passport JWT"
"Give me the Go Fiber equivalent of the RAG chatbot endpoint"
"Convert the database models to Prisma (TypeScript)"
"Show me the Laravel version of the cohort management module"
```

The agent will ask **two clarifying questions** if your request is ambiguous:
1. Which layer(s)? — backend / auth / database / frontend / RAG (or all)
2. What is the target framework and language?

Then it produces a full migration plan before writing any code.

---

## Supported Target Languages & Frameworks

| Language   | Framework Options                         |
|------------|-------------------------------------------|
| Python     | Django REST Framework                     |
| TypeScript | NestJS, Express.js, Hono, Elysia          |
| Java       | Spring Boot (Spring MVC + Spring Security)|
| PHP        | Laravel (Eloquent, Sanctum/Passport)      |
| Ruby       | Ruby on Rails (Devise, Pundit)            |
| Go         | Go Fiber, Gin, Echo                       |
| .NET (C#)  | ASP.NET Core Minimal APIs                 |

---

## Step-by-Step Conversion Process

### Step 1 — Choose your layers

| Layer      | IntelliStack Source                              | Agent Skill       |
|------------|--------------------------------------------------|-------------------|
| Backend API| `intellistack/backend/src/core/`                 | `export-backend`  |
| Auth       | `intellistack/auth-server/src/`                  | `export-auth`     |
| Database   | `intellistack/backend/src/core/*/models.py`      | `export-database` |
| Frontend   | `intellistack/frontend/src/`                     | `export-frontend` |
| RAG / AI   | `intellistack/backend/src/ai/`                   | `export-rag`      |

You can migrate all at once or one layer at a time. One layer at a time is
recommended for large rewrites.

### Step 2 — Read the migration plan

The agent outputs a plan before any code:
```
## Migration Plan: <layer> → <framework>
- Files to create: [list]
- Dependencies to add: [list with versions]
- Breaking changes: [list]
- Environment variables: [list]
```

Review this plan and confirm before proceeding.

### Step 3 — Receive production-ready code

For each file the agent generates:
- All imports included
- Full class / function bodies (no stubs)
- Framework-idiomatic patterns (not transliterated Python)
- Auth guards / middleware equivalent
- Error handling matching IntelliStack's HTTP taxonomy
- A "To wire up:" checklist at the end

### Step 4 — Apply database migrations

Whenever models are ported:
```bash
# Prisma (TypeScript)
npx prisma migrate dev --name init

# Django
python manage.py makemigrations && python manage.py migrate

# Rails
rails db:migrate

# GORM (Go) — migrations are auto-applied on startup by default
```

### Step 5 — Configure environment variables

The agent always lists required env vars. Copy the pattern from
`intellistack/.env.example` and adapt variable names to your framework's
convention.

### Step 6 — Verify parity

After conversion, check:
- [ ] All API endpoints respond with the same HTTP status codes
- [ ] Auth flow issues RS256 JWT (or equivalent for target framework)
- [ ] Stage-locking business rules preserved
- [ ] RAG citations returned in the same shape
- [ ] Database schema matches (run both `alembic show` and your ORM's schema)

---

## Common Conversion Scenarios

See `gitagent/workflows/scenarios/` for worked examples:

| Scenario | File |
|----------|------|
| Full NestJS port | `scenarios/nestjs.md` |
| Django REST Framework port | `scenarios/django.md` |
| Go Fiber port | `scenarios/go-fiber.md` |

---

## What the Agent Will Never Do

- Invent API contracts not in the IntelliStack spec
- Hardcode secrets or API keys
- Silently drop features — it always flags what cannot be ported
- Modify the IntelliStack source files directly

---

## Quick Reference — IntelliStack Module Catalogue

| Module        | What it covers                                              |
|---------------|-------------------------------------------------------------|
| `auth`        | Login, register, OAuth (Google/GitHub), JWT, password reset |
| `users`       | Profile, preferences, role management                       |
| `learning`    | 5-stage path, lessons, exercises, assessments, progress     |
| `content`     | MDX authoring, versioning, review workflow                  |
| `institution` | Cohorts, enrollment, instructor assignment, webhooks        |
| `rag`         | Chatbot, ingestion, retrieval, Cohere reranking, citations  |
| `badges`      | Badge issuance, certificate generation                      |
| `analytics`   | Cohort analytics, progress aggregation                      |
