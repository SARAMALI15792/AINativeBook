# Quickstart Guide: IntelliStack Platform

**Branch**: `001-intellistack-platform` | **Date**: 2026-02-07

## Prerequisites

### Required Software

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 20.x LTS | Frontend runtime |
| Python | 3.11+ | Backend runtime |
| Docker | 24.x+ | Container runtime |
| Docker Compose | 2.20+ | Multi-container orchestration |
| Git | 2.40+ | Version control |

### Optional (for local simulation)

| Tool | Version | Purpose |
|------|---------|---------|
| NVIDIA Driver | 535+ | GPU support |
| CUDA | 12.x | GPU compute |
| Gazebo | Harmonic | Robotics simulation |

---

## Quick Start (5 minutes)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-org/intellistack.git
cd intellistack

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (see Environment Variables below)
```

### 2. Start Development Environment

```bash
# Start all services with Docker Compose
docker compose -f docker-compose.dev.yml up -d

# This starts:
# - PostgreSQL (localhost:5432)
# - Redis (localhost:6379)
# - Qdrant (localhost:6333)
# - Backend API (localhost:8000)
# - Frontend (localhost:3000)
# - Content/Docusaurus (localhost:3001)
```

### 3. Initialize Database

```bash
# Run database migrations
docker compose exec backend alembic upgrade head

# Seed initial data (stages, roles, sample content)
docker compose exec backend python -m src.scripts.seed_data
```

### 4. Verify Setup

```bash
# Check API health
curl http://localhost:8000/health

# Expected: {"status": "healthy", "services": {"db": "ok", "redis": "ok", "qdrant": "ok"}}

# Open frontend
open http://localhost:3000
```

---

## Environment Variables

Create a `.env` file with:

```bash
# ===================
# Required
# ===================

# Database (Neon PostgreSQL or local)
DATABASE_URL=postgresql://user:password@localhost:5432/intellistack

# Redis
REDIS_URL=redis://localhost:6379

# Qdrant Vector DB
QDRANT_URL=http://localhost:6333

# OpenAI API (for AI features)
OPENAI_API_KEY=sk-...

# Session secret (generate with: openssl rand -hex 32)
SESSION_SECRET=your-32-byte-hex-secret

# ===================
# Optional
# ===================

# Better-Auth config
BETTER_AUTH_SECRET=your-auth-secret
BETTER_AUTH_URL=http://localhost:3000

# Cohere (for reranking)
COHERE_API_KEY=...

# Simulation cloud (if using cloud GPU)
SIMULATION_API_URL=...
SIMULATION_API_KEY=...

# Email (for password reset, notifications)
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...

# ===================
# Development
# ===================
DEBUG=true
LOG_LEVEL=debug
```

---

## Development Workflow

### Backend Development

```bash
# Enter backend container
docker compose exec backend bash

# Or run locally with virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/unit/test_learning_service.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Frontend Development

```bash
# Enter frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Run E2E tests
npm run test:e2e

# Type check
npm run typecheck

# Lint
npm run lint
```

### Content Development

```bash
# Enter content directory
cd content

# Install dependencies
npm install

# Run Docusaurus dev server
npm start

# Build content
npm run build
```

---

## Database Commands

```bash
# Create new migration
docker compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker compose exec backend alembic upgrade head

# Rollback one migration
docker compose exec backend alembic downgrade -1

# View migration history
docker compose exec backend alembic history

# Reset database (DESTRUCTIVE)
docker compose exec backend alembic downgrade base
docker compose exec backend alembic upgrade head
```

---

## API Documentation

Once running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Common Tasks

### Index Content for RAG

```bash
# Index all published content
docker compose exec backend python -m src.scripts.index_content

# Index specific stage
docker compose exec backend python -m src.scripts.index_content --stage 1

# Clear and reindex
docker compose exec backend python -m src.scripts.index_content --clear
```

### Create Admin User

```bash
# Interactive admin creation
docker compose exec backend python -m src.scripts.create_admin

# Or with args
docker compose exec backend python -m src.scripts.create_admin \
  --email admin@example.com \
  --name "Admin User" \
  --password "secure-password"
```

### Run Background Tasks

```bash
# Start Celery worker (if not using Docker)
celery -A src.tasks worker --loglevel=info

# Start Celery beat (scheduled tasks)
celery -A src.tasks beat --loglevel=info
```

---

## Troubleshooting

### Port Conflicts

```bash
# Check what's using a port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different ports
PORT=8001 npm run dev  # Frontend
uvicorn src.main:app --port 8001  # Backend
```

### Database Connection Issues

```bash
# Verify PostgreSQL is running
docker compose ps

# Check logs
docker compose logs postgres

# Test connection
docker compose exec postgres psql -U intellistack -d intellistack -c "SELECT 1"
```

### Qdrant Issues

```bash
# Check Qdrant status
curl http://localhost:6333/healthz

# View collections
curl http://localhost:6333/collections

# Delete collection (for reindex)
curl -X DELETE http://localhost:6333/collections/textbook_content
```

### AI Features Not Working

1. Verify `OPENAI_API_KEY` is set correctly
2. Check API key has sufficient quota
3. View backend logs: `docker compose logs backend`

---

## Production Deployment

See `docs/deployment.md` for:

- Vercel deployment (frontend)
- Fly.io deployment (backend)
- Neon setup (database)
- Qdrant Cloud setup
- CI/CD configuration

---

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐
│  Next.js        │     │ Docusaurus MDX  │
│  localhost:3000 │     │ localhost:3001  │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   FastAPI Gateway     │
         │   localhost:8000      │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐  ┌───────▼───────┐  ┌─────▼─────┐
│Postgres│  │     Redis     │  │  Qdrant   │
│  :5432 │  │     :6379     │  │   :6333   │
└────────┘  └───────────────┘  └───────────┘
```

---

## Getting Help

- **Documentation**: `/docs` directory
- **API Reference**: http://localhost:8000/docs
- **Issues**: GitHub Issues

---

*Quickstart completed: 2026-02-07*
