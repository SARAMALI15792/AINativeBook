# Database Setup Guide

## Prerequisites

PostgreSQL is required for local development. Use Docker for easiest setup.

## Quick Start (Docker)

1. Start PostgreSQL and other services:
   ```bash
   docker-compose -f docker-compose.dev.yml up -d postgres redis qdrant
   ```

2. Run migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

3. Start the backend:
   ```bash
   python -m uvicorn src.main:app --reload
   ```

## Manual Setup (Without Docker)

If you prefer to run PostgreSQL locally:

1. Install PostgreSQL 16
2. Create database and user:
   ```sql
   CREATE DATABASE intellistack;
   CREATE USER intellistack WITH PASSWORD 'intellistack_dev';
   GRANT ALL PRIVILEGES ON DATABASE intellistack TO intellistack;
   ```
3. Update `DATABASE_URL` in `.env` if using different credentials

## Running Migrations

```bash
# Apply all migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Rollback one migration
alembic downgrade -1
```

## Seeding Initial Data

To seed initial roles and data:

```bash
python scripts/seed_database.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | `postgresql://intellistack:intellistack_dev@localhost:5432/intellistack` | Database connection string |
| DB_POOL_SIZE | 5 | Connection pool size |
| DB_MAX_OVERFLOW | 10 | Max overflow connections |
| DB_POOL_TIMEOUT | 30 | Pool timeout in seconds |
