# IntelliStack Platform

> **AI-Native Learning Management System for Physical AI & Humanoid Robotics Education**

IntelliStack is a full-stack LMS that combines progressive learning paths, an AI-powered tutor, RAG chatbot with citations, content authoring tools, institution management, and community features — purpose-built for Physical AI and Humanoid Robotics education.

---

## Live Services

| Service | URL |
|---------|-----|
| Frontend | Netlify (auto-deployed from `main`) |
| Backend API | [Railway](https://intellistack-backend-production.up.railway.app) |
| Auth Server | [Railway](https://intellistack-auth-production.up.railway.app) |
| Docs / Content | [GitHub Pages](https://saramali15792.github.io/AINativeBook/) |

---

## Technology Stack

### Frontend
| Technology | Version |
|-----------|---------|
| Next.js | 14.x |
| React | 18.x |
| TypeScript | 5.x |
| Tailwind CSS | 3.x |
| Framer Motion | 11.x |
| Three.js / R3F | 0.160 / 8.x |
| Better Auth | 1.4.x |
| Vitest + Playwright | Testing |

### Backend
| Technology | Version |
|-----------|---------|
| Python | 3.11+ |
| FastAPI | 0.109+ |
| SQLAlchemy (async) | 2.0+ |
| Alembic | 1.13+ |
| PostgreSQL (Neon) | 16+ |
| Redis | 5.x |
| Qdrant (vector store) | 1.7+ |
| Google Generative AI | 1.0+ |
| Structlog | 24.x |

### Auth Server
| Technology | Version |
|-----------|---------|
| Node.js | 20+ |
| TypeScript | 5.x |
| Better Auth | 1.4.x |
| Express | 4.x |
| Drizzle ORM | 0.41+ |
| Neon PostgreSQL | Serverless |

### Infrastructure
| Service | Role |
|---------|------|
| Railway | Backend + Auth deployment |
| Netlify | Frontend deployment |
| GitHub Pages | Docusaurus content/docs |
| GitHub Actions | CI/CD pipelines |
| Docker | Local development containers |

---

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                        IntelliStack                            │
│                                                                │
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────┐  │
│  │  Next.js     │    │  FastAPI     │    │  Better-Auth    │  │
│  │  Frontend    │───▶│  Backend     │───▶│  OIDC Server    │  │
│  │  (Netlify)   │    │  (Railway)   │    │  (Railway)      │  │
│  └──────────────┘    └──────┬───────┘    └─────────────────┘  │
│                             │                                   │
│                 ┌───────────┼───────────┐                      │
│                 ▼           ▼           ▼                      │
│          ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│          │PostgreSQL│ │  Redis   │ │  Qdrant  │               │
│          │  (Neon)  │ │  Cache   │ │  Vector  │               │
│          └──────────┘ └──────────┘ └──────────┘               │
│                                                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Docusaurus Content (GitHub Pages)            │ │
│  └───────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

**Key design principles:**
- OIDC/JWT authentication via Better-Auth (RS256 tokens, JWKS endpoint)
- RAG pipeline: Qdrant vector search → Cohere reranking → OpenAI generation + SSE streaming
- Stage-based access control — content unlocks progressively as learners advance
- Async-first backend (SQLAlchemy 2.0 async + asyncpg)

---

## Getting Started

### Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16+ (or a Neon connection string)
- Redis 7+
- Qdrant (local or cloud)

### 1. Clone the repository

```bash
git clone https://github.com/SARAMALI15792/AINativeBook.git
cd AINativeBook
```

### 2. Configure environment variables

```bash
# Root-level env for all services
cp intellistack/.env.example intellistack/.env

# Auth server env
cp intellistack/auth-server/.env.example intellistack/auth-server/.env
```

Key variables to set in `intellistack/.env`:

```env
DATABASE_URL=postgresql://user:password@host:5432/intellistack
REDIS_URL=redis://localhost:6379/0
QDRANT_HOST=localhost
QDRANT_PORT=6333
OPENAI_API_KEY=sk-...
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_SECRET=<min-32-chars>
GOOGLE_CLIENT_ID=...        # optional OAuth
GITHUB_CLIENT_ID=...        # optional OAuth
```

### 3. Start the Auth Server

```bash
cd intellistack/auth-server
npm install
npm run migrate
npm run dev
# Runs on http://localhost:3001
```

### 4. Start the Backend

```bash
cd intellistack/backend
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### 5. Start the Frontend

```bash
cd intellistack/frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

---

## Project Structure

```
AINativeBook/
├── intellistack/
│   ├── .env.example              # Root environment template
│   ├── backend/                  # FastAPI Python backend
│   │   ├── src/
│   │   │   ├── main.py           # FastAPI app entry point
│   │   │   ├── config/           # Settings & logging
│   │   │   ├── core/             # Domain modules (auth, users, content, etc.)
│   │   │   ├── ai/               # AI features (RAG, tutor, chatkit, personalization)
│   │   │   └── shared/           # Database, middleware, utilities
│   │   ├── alembic/              # Database migrations
│   │   ├── scripts/              # Seed & ingestion scripts
│   │   └── requirements.txt
│   ├── auth-server/              # Better-Auth OIDC server (TypeScript)
│   │   └── src/
│   │       ├── index.ts          # Express entry point
│   │       ├── auth.ts           # Better-Auth configuration
│   │       ├── db.ts             # Drizzle ORM setup
│   │       └── email.ts          # Email via Resend
│   ├── frontend/                 # Next.js 14 frontend
│   │   └── src/
│   │       ├── app/              # App Router pages
│   │       ├── components/       # UI components
│   │       ├── contexts/         # React contexts
│   │       └── lib/              # Client utilities
│   └── content/                  # Docusaurus learning content
├── specs/                        # Spec-Driven Development artifacts
│   └── 001-intellistack-platform/
│       ├── spec.md               # Feature requirements
│       ├── plan.md               # Architecture decisions
│       └── tasks.md              # Implementation task tracking
├── history/                      # Prompt History Records (PHRs)
│   ├── prompts/                  # All session PHRs
│   └── adr/                     # Architecture Decision Records
├── .specify/                     # SpecKit Plus templates & scripts
├── .github/
│   └── workflows/                # CI/CD pipelines
└── CLAUDE.md                     # AI assistant development guidelines
```

---

## Key Features

### 5-Stage Learning Path
- **Foundations → ROS 2 & Simulation → Perception & Planning → AI Integration → Capstone**
- Stage locking/unlocking based on prerequisites
- Progress tracking at lesson, exercise, and assessment level
- Badge issuance and certificate generation

### RAG Chatbot (AI-Powered Q&A)
- OpenAI integration with Server-Sent Events (SSE) streaming
- Qdrant vector store with hybrid retrieval
- Text chunking via `tiktoken` (512 tokens, 50 overlap)
- Cohere reranking (`rerank-v3.5`)
- Citations with source passage viewer
- Stage-based access control — only searches content the learner has unlocked
- Text-selection triggered queries

### AI Tutor
- Socratic method dialogue
- Code review and debugging assistance
- LangGraph agent with guardrails

### Authentication & Security
- Better-Auth OIDC server (RS256 JWT, JWKS, OIDC discovery)
- Email/password + Google & GitHub OAuth
- Role-based access control: `student`, `instructor`, `admin`
- JWKS middleware on every backend request

### Content Authoring
- MDX editor with live preview
- Version history with diff viewer
- Review workflow: `draft → in_review → published`
- RAG ingestion pipeline for new content

### Institution Management
- Cohort creation with enrollment limits
- Instructor assignment
- Webhook notifications with retry logic
- Analytics aggregation

### Personalization
- Adaptive content recommendations
- User profile-based learning path adjustments

---

## Development Workflow

### CI/CD Pipelines (GitHub Actions)

| Workflow | Trigger | Target |
|---------|---------|--------|
| `deploy-backend.yml` | Push to `main` (backend changes) | Railway |
| `deploy-auth.yml` | Push to `main` (auth-server changes) | Railway |
| `deploy-frontend.yml` | Push to `main` (frontend changes) | Netlify |
| `deploy-docs.yml` | Push to `main` (content changes) | GitHub Pages |

### Branch Strategy

- `main` — production-ready code; all CI/CD triggers from here
- Feature branches follow the pattern: `<phase-number>-<feature-name>`

### Development Process (Spec-Driven)

1. Write/update spec in `specs/<feature>/spec.md`
2. Generate architecture plan (`/sp.plan`)
3. Generate tasks (`/sp.tasks`)
4. Implement (`/sp.implement`)
5. PHR auto-created after each session for traceability

---

## API Reference

The backend exposes a RESTful API versioned at `/api/v1`.

| Endpoint | Description |
|---------|-------------|
| `GET /health` | Basic health check |
| `GET /health/detail` | Detailed health + metrics |
| `GET /metrics` | Prometheus-compatible metrics |
| `GET /docs` | Swagger UI (dev only) |
| `GET /redoc` | ReDoc (dev only) |

Auth Server endpoints:

| Endpoint | Description |
|---------|-------------|
| `POST /api/auth/sign-up/email` | Email registration |
| `POST /api/auth/sign-in/email` | Email login |
| `POST /api/auth/sign-in/social` | OAuth (Google/GitHub) |
| `POST /api/auth/forget-password` | Request password reset |
| `GET /.well-known/openid-configuration` | OIDC discovery |
| `GET /.well-known/jwks.json` | Public key set |

---

## Testing

### Frontend
```bash
cd intellistack/frontend

# Unit tests (Vitest)
npm test

# E2E tests (Playwright)
npm run test:e2e

# Accessibility audit (Lighthouse)
npm run lighthouse
```

### Backend
```bash
cd intellistack/backend
pytest
```

### Auth Server
```bash
cd intellistack/auth-server
npm run type-check
npm run lint
```

---

## Deployment

### Backend — Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway up --service intellistack-backend --path-as-root intellistack/backend
```

### Auth Server — Railway

```bash
railway up --service intellistack-auth --path-as-root intellistack/auth-server
```

### Frontend — Netlify

```bash
cd intellistack/frontend
npm run build
npx netlify-cli deploy --dir .next --prod
```

**Required secrets** (GitHub → Settings → Secrets):

| Secret | Used By |
|--------|---------|
| `RAILWAY_TOKEN` | Backend + Auth deploy |
| `NETLIFY_SITE_ID` | Frontend deploy |
| `NETLIFY_AUTH_TOKEN` | Frontend deploy |
| `RAILWAY_AUTH_URL` | Docs build |
| `RAILWAY_BACKEND_URL` | Docs build |

---

## Implementation Progress

| Phase | Name | Status |
|-------|------|--------|
| 0 | Vertical Slice | Complete |
| 1 | Setup | Complete |
| 2 | Foundation | Complete |
| 3 | Student Learning | Complete |
| 4 | Content Creation | Complete |
| 5 | Institution Admin | Complete |
| 6 | RAG Chatbot | Complete |
| 7 | AI Tutor | In Progress |
| 8 | Community | Pending |
| 9 | Assessment | Pending |
| 10 | Personalization | Pending |
| 11 | Polish | Pending |

**Overall progress: ~74.5% (38/51 tasks complete)**

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b <phase>-<feature>`
3. Follow the spec-driven workflow (spec → plan → tasks → implement)
4. Ensure tests pass before opening a PR
5. Keep commits small and focused; reference task IDs in commit messages
6. Open a PR against `main`

Coding standards enforced:
- **Python:** PEP 8, type hints required, async-first patterns
- **TypeScript:** strict mode, no `any` without justification
- **React:** functional components only, hooks-based state
- **SQL:** all schema changes via Alembic migrations

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built with [Spec-Driven Development](https://github.com/SARAMALI15792/AINativeBook/tree/main/specs) methodology using Claude Code.*
