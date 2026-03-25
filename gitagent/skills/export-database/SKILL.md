---
name: export-database
description: >
  Converts IntelliStack's SQLAlchemy 2.0 models and Alembic migrations to
  any target ORM or database toolkit, preserving the full schema, indexes,
  relationships, and cascade rules.
license: MIT
allowed-tools: read_file, search_code
metadata:
  author: IntelliStack Team
  version: "1.0.0"
  category: migration
---

# Skill: Export Database

## Purpose
Produce a ready-to-run database schema in any target ORM from the
authoritative IntelliStack SQLAlchemy models.

## IntelliStack Database Facts
- **Database:** PostgreSQL (hosted on Neon)
- **ORM:** SQLAlchemy 2.0 async (mapped classes)
- **Migrations:** Alembic (auto-generated, sequential)
- **Connection:** async `asyncpg` driver
- **Models location:** `intellistack/backend/src/core/<module>/models.py`

## Key Tables (partial list)
| Table                  | Module       | Notes                          |
|------------------------|--------------|--------------------------------|
| users                  | auth/users   | Core identity                  |
| sessions               | auth         | JWT refresh tokens             |
| oauth_accounts         | auth         | Google / GitHub links          |
| learning_stages        | learning     | 5-stage curriculum             |
| lessons                | learning     | Lesson metadata                |
| user_progress          | learning     | Per-user stage/lesson progress |
| exercises              | learning     | Coding exercises               |
| assessments            | learning     | Quizzes / evaluations          |
| content_items          | content      | MDX documents                  |
| content_versions       | content      | Version history                |
| institutions           | institution  | Org entities                   |
| cohorts                | institution  | Student groups                 |
| cohort_enrollments     | institution  | User ↔ cohort                  |
| webhooks               | institution  | Outbound webhook configs       |
| chat_sessions          | rag          | Chatbot conversations          |
| chat_messages          | rag          | Per-turn messages + citations  |
| badges                 | badges       | Badge definitions              |
| user_badges            | badges       | Issued badges                  |

## Supported Target ORMs
| ORM            | Language   | Migration Tool        |
|----------------|------------|-----------------------|
| Prisma         | TypeScript | `prisma migrate dev`  |
| TypeORM        | TypeScript | `typeorm migration`   |
| Drizzle ORM    | TypeScript | `drizzle-kit push`    |
| Hibernate      | Java       | Flyway / Liquibase    |
| Django ORM     | Python     | `manage.py migrate`   |
| GORM           | Go         | AutoMigrate / Goose   |
| ActiveRecord   | Ruby       | `rails db:migrate`    |
| Eloquent       | PHP        | Laravel migrations    |

## Instructions

### Step 1 — Read source models
For each requested module, read:
`intellistack/backend/src/core/<module>/models.py`

Extract for every model class:
- `__tablename__`
- All `Column(...)` definitions (name, type, nullable, default, server_default)
- `relationship(...)` (back_populates, cascade, lazy)
- `Index(...)` and `UniqueConstraint(...)` definitions

### Step 2 — Produce schema in target ORM
Output the complete target schema file. For TypeScript ORMs, include
the TypeScript types. For Java, include the full entity class with
annotations. Never truncate — output every field.

### Step 3 — Migration script
Output the migration command for the target tool, e.g.:
```bash
# Prisma
npx prisma migrate dev --name init_intellistack

# Django
python manage.py makemigrations && python manage.py migrate

# GORM
# AutoMigrate called in main.go startup
```

### Step 4 — Data type mapping reference
```
SQLAlchemy → Prisma
String      → String
Integer     → Int
BigInteger  → BigInt
Boolean     → Boolean
DateTime    → DateTime
UUID        → String @db.Uuid
Text        → String @db.Text
JSON / JSONB → Json
Enum        → enum declaration
ForeignKey  → @relation(...)
```

### Step 5 — Seed data checklist
- [ ] Learning stages (5 rows) must be seeded before any user progress.
- [ ] Default badge definitions must be seeded.
- [ ] At least one admin user must be created post-migration.
