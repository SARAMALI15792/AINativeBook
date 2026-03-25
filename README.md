<div align="center">

# 🤖 IntelliStack Platform

### AI-Native Learning Management System for Physical AI & Humanoid Robotics

[![Live App](https://img.shields.io/badge/Live_App-intellistack--app.netlify.app-00C7B7?style=for-the-badge&logo=netlify)](https://intellistack-app.netlify.app/)
[![Docs](https://img.shields.io/badge/Docs-GitHub_Pages-181717?style=for-the-badge&logo=github)](https://saramali15792.github.io/AINativeBook/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)
[![Export Agent](https://img.shields.io/badge/Export_Agent-Convert_to_Any_Framework-6366F1?style=for-the-badge&logo=github-actions&logoColor=white)](./gitagent/workflows/convert.md)

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)

</div>

---

## 🔄 Export Agent — Convert to Any Framework

IntelliStack ships with a built-in **Export Agent** (`gitagent/`) that lets any developer port the entire platform — or just one layer — to their preferred language and framework.

| Target Language | Frameworks Supported |
|----------------|---------------------|
| Python | Django REST Framework |
| TypeScript / Node.js | NestJS, Express.js, Hono, Elysia |
| Java | Spring Boot |
| PHP | Laravel |
| Ruby | Ruby on Rails |
| Go | Go Fiber, Gin, Echo |
| C# | ASP.NET Core Minimal APIs |

**How it works — just ask in plain language:**

```
"Convert IntelliStack to NestJS with Prisma"
"Port only the auth layer to Laravel"
"Give me the Go Fiber version of the RAG chatbot"
"Convert the database models to TypeORM"
```

The agent reads the live codebase, produces a migration plan, then outputs production-ready, framework-idiomatic code with all imports, env vars, and a wire-up checklist.

**Start here:** [`gitagent/workflows/convert.md`](./gitagent/workflows/convert.md) · Example scenarios: [NestJS](./gitagent/workflows/scenarios/nestjs.md) · [Django](./gitagent/workflows/scenarios/django.md) · [Go Fiber](./gitagent/workflows/scenarios/go-fiber.md)

---

## What Is IntelliStack?

IntelliStack is an AI-native Learning Management System purpose-built for **Physical AI and Humanoid Robotics education**. It replaces static course platforms with an intelligent, adaptive environment where learners progress through 5 gated stages — from foundational robotics concepts to a full capstone project — guided by a RAG-powered chatbot and a Socratic AI tutor at every step.

**The problem it solves:**
- Traditional LMS platforms have no AI layer — learners get stuck with no contextual help
- Robotics education content is scattered across docs, papers, and videos with no unified path
- Instructors have no visibility into where students struggle or how to adapt content
- Institutions lack the tools to manage cohorts, track progress, and deliver assessments at scale

**How it works:**

```mermaid
graph LR
    A[Student Signs Up] --> B[Personalized Onboarding]
    B --> C[Stage 1 Unlocked]
    C --> D{Learn via Lessons}
    D --> E[Ask RAG Chatbot]
    D --> F[Use AI Tutor]
    D --> G[Complete Assessment]
    G -->|Pass| H[Stage 2 Unlocked]
    G -->|Fail| D
    H --> I[...]
    I --> J[Stage 5 Capstone]
    J --> K[Certificate Issued]
```

**Scale:** The platform is architected to handle **10,000+ concurrent learners** — async FastAPI backend with connection pooling, Redis-backed rate limiting and caching, Qdrant vector search with sub-50ms retrieval, and horizontally scalable Railway deployments.

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph Client["Client Layer"]
        FE["Next.js 14 Frontend\n(Netlify)"]
        DOCS["Docusaurus Docs\n(GitHub Pages)"]
    end

    subgraph Auth["Auth Layer"]
        AUTH["Better-Auth OIDC Server\n(Railway · Node.js)"]
        JWKS["JWKS Endpoint\n/.well-known/jwks.json"]
    end

    subgraph API["API Layer"]
        BACKEND["FastAPI Backend\n(Railway · Python 3.11)"]
        MW["JWKS Middleware\nJWT Validation"]
    end

    subgraph AI["AI Layer"]
        RAG["RAG Pipeline\nQdrant + Cohere + OpenAI"]
        TUTOR["AI Tutor\nLangGraph · Socratic Method"]
        CHATKIT["ChatKit\nStreaming SSE"]
    end

    subgraph Data["Data Layer"]
        PG[("PostgreSQL\nNeon")]
        REDIS[("Redis\nCache + Rate Limit")]
        QDRANT[("Qdrant\nVector Store")]
    end

    FE -->|"OAuth / Session"| AUTH
    FE -->|"API Calls"| BACKEND
    DOCS -->|"Auth Redirect"| AUTH
    AUTH --> JWKS
    AUTH --> PG
    BACKEND --> MW
    MW --> JWKS
    BACKEND --> RAG
    BACKEND --> TUTOR
    BACKEND --> CHATKIT
    BACKEND --> PG
    BACKEND --> REDIS
    RAG --> QDRANT
    RAG -->|"OpenAI API"| CHATKIT
```

---

## 🔄 Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Next.js Frontend
    participant AUTH as Better-Auth OIDC
    participant API as FastAPI Backend
    participant AI as RAG / Tutor AI
    participant DB as PostgreSQL

    U->>FE: Visit intellistack-app.netlify.app
    FE->>AUTH: Sign In (Email / Google / GitHub)
    AUTH-->>FE: JWT Access Token (RS256)
    FE->>API: API Request + Bearer Token
    API->>AUTH: Verify via JWKS endpoint
    AUTH-->>API: Token valid
    API->>DB: Fetch user/content data
    DB-->>API: Data
    API->>AI: RAG query / Tutor session
    AI-->>API: Streamed response (SSE)
    API-->>FE: Response
    FE-->>U: Rendered content
```

---

## 🎓 5-Stage Learning Path

```mermaid
graph LR
    S1["Stage 1\nFoundations"]
    S2["Stage 2\nROS 2 & Simulation"]
    S3["Stage 3\nPerception & Planning"]
    S4["Stage 4\nAI Integration"]
    S5["Stage 5\nCapstone"]

    S1 -->|"Unlock"| S2
    S2 -->|"Unlock"| S3
    S3 -->|"Unlock"| S4
    S4 -->|"Unlock"| S5

    style S1 fill:#3B82F6,color:#fff
    style S2 fill:#22C55E,color:#fff
    style S3 fill:#EAB308,color:#000
    style S4 fill:#F97316,color:#fff
    style S5 fill:#EF4444,color:#fff
```

Each stage unlocks based on passing assessments in the previous stage. Progress is tracked at lesson, exercise, and assessment level with badge issuance and certificate generation upon completion.

---

## 🛠️ Technology Stack

### Frontend
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat&logo=next.js)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.x-06B6D4?style=flat&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Framer Motion](https://img.shields.io/badge/Framer_Motion-11-0055FF?style=flat&logo=framer)](https://www.framer.com/motion/)
[![Three.js](https://img.shields.io/badge/Three.js-0.160-black?style=flat&logo=three.js)](https://threejs.org/)

### Backend
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0_async-D71F00?style=flat)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-5.x-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Qdrant](https://img.shields.io/badge/Qdrant-1.7+-FF4158?style=flat)](https://qdrant.tech/)

### Auth Server
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Better Auth](https://img.shields.io/badge/Better_Auth-1.4.x-6366F1?style=flat)](https://www.better-auth.com/)
[![Drizzle ORM](https://img.shields.io/badge/Drizzle_ORM-0.41+-C5F74F?style=flat&logoColor=black)](https://orm.drizzle.team/)
[![Express](https://img.shields.io/badge/Express-4.x-000000?style=flat&logo=express)](https://expressjs.com/)

### AI & ML
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-1.0+-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev/)
[![Cohere](https://img.shields.io/badge/Cohere_Rerank-v3.5-39594E?style=flat)](https://cohere.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent-1C3C3C?style=flat)](https://langchain-ai.github.io/langgraph/)

### Infrastructure
[![Railway](https://img.shields.io/badge/Railway-Deploy-0B0D0E?style=flat&logo=railway)](https://railway.app/)
[![Netlify](https://img.shields.io/badge/Netlify-Frontend-00C7B7?style=flat&logo=netlify&logoColor=white)](https://netlify.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=flat&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🤖 RAG Chatbot
- OpenAI + SSE streaming responses
- Qdrant hybrid vector retrieval
- Cohere `rerank-v3.5` for precision
- Source citations with passage viewer
- Stage-locked content access
- Text-selection triggered queries

</td>
<td width="50%">

### 🎓 AI Tutor
- Socratic method dialogue engine
- Code review & debugging assistant
- LangGraph multi-agent architecture
- Safety guardrails built-in
- Session persistence

</td>
</tr>
<tr>
<td width="50%">

### 🔐 Authentication
- Better-Auth OIDC (RS256 JWT)
- Email/password + Google + GitHub OAuth
- JWKS endpoint for token verification
- Role-based access: `student` / `instructor` / `admin`

</td>
<td width="50%">

### 📝 Content Authoring
- MDX editor with live preview
- Version history & diff viewer
- Review workflow: `draft → in_review → published`
- RAG auto-ingestion pipeline for new content

</td>
</tr>
<tr>
<td width="50%">

### 🏫 Institution Management
- Cohort creation with enrollment limits
- Instructor assignment & management
- Webhook notifications with retry logic
- Analytics aggregation dashboards

</td>
<td width="50%">

### 🎯 Personalization
- Adaptive content recommendations
- Profile-based learning path adjustments
- Progress tracking (lesson / exercise / assessment)
- Badge issuance & certificate generation

</td>
</tr>
<tr>
<td width="100%" colspan="2">

### 🔄 Export Agent — Convert to Any Framework or Language
- Port any layer (backend / auth / database / frontend / RAG) to your preferred stack
- Supports 7 languages: Python, TypeScript, Java, PHP, Ruby, Go, C#
- Frameworks: Django, NestJS, Express, Spring Boot, Laravel, Rails, Go Fiber, and more
- Full migration plan produced before any code is written
- Production-ready output: imports, full bodies, env vars, wire-up checklist
- See [`gitagent/workflows/convert.md`](./gitagent/workflows/convert.md) to get started

</td>
</tr>
</table>

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version |
|------|---------|
| Node.js | 20+ |
| Python | 3.11+ |
| PostgreSQL | 16+ (or Neon cloud) |
| Redis | 7+ |
| Qdrant | 1.7+ (or Qdrant Cloud) |

### 1. Clone

```bash
git clone https://github.com/SARAMALI15792/AINativeBook.git
cd AINativeBook
```

### 2. Configure Environment

```bash
cp intellistack/.env.example intellistack/.env
cp intellistack/auth-server/.env.example intellistack/auth-server/.env
```

Key values in `intellistack/.env`:

```env
DATABASE_URL=postgresql://user:password@host:5432/intellistack
REDIS_URL=redis://localhost:6379/0
QDRANT_HOST=localhost
OPENAI_API_KEY=sk-...
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_SECRET=<min-32-random-chars>
```

### 3. Start Auth Server

```bash
cd intellistack/auth-server && npm install && npm run migrate && npm run dev
# Runs on http://localhost:3001
```

### 4. Start Backend API

```bash
cd intellistack/backend
pip install -r requirements.txt && alembic upgrade head
uvicorn src.main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### 5. Start Frontend

```bash
cd intellistack/frontend && npm install && npm run dev
# Runs on http://localhost:3000
```

Or skip local setup and use the live app: **[intellistack-app.netlify.app](https://intellistack-app.netlify.app/)**

---

## 📖 How to Use the Platform

**Students** — [Sign up](https://intellistack-app.netlify.app/) → complete onboarding → work through Stage 1 lessons and exercises → ask the RAG chatbot for instant answers with source citations → use the AI Tutor when you're stuck (it guides, not gives away answers) → pass the assessment → Stage 2 unlocks → repeat through all 5 stages → receive your certificate.

**Instructors** — Log in with an `instructor` account → go to Content Authoring → write lessons in MDX with live preview → submit for review → once approved, content is automatically indexed into the RAG vector store → manage your cohort enrollments and view per-student progress analytics.

**Admins** — Log in with an `admin` account → manage institutions, cohorts, and user roles → monitor platform health and Prometheus metrics → configure external webhooks.

---

## 📁 Project Structure

```
AINativeBook/
├── intellistack/
│   ├── backend/                  # FastAPI Python backend
│   │   ├── src/
│   │   │   ├── main.py           # App entry point
│   │   │   ├── config/           # Settings & structured logging
│   │   │   ├── core/             # Domain modules (auth, users, content, learning, institution, assessment)
│   │   │   ├── ai/               # RAG, AI Tutor, ChatKit, Personalization
│   │   │   └── shared/           # DB, middleware, metrics
│   │   └── alembic/              # DB migrations
│   ├── auth-server/              # Better-Auth OIDC server (TypeScript/Node.js)
│   ├── frontend/                 # Next.js 14 App Router frontend
│   └── content/                  # Docusaurus learning content
├── specs/                        # Feature specs, plans, and task tracking
├── history/                      # Prompt History Records & ADRs
├── gitagent/                     # Export Agent — convert to any framework/language
│   ├── workflows/convert.md      # Main conversion workflow guide
│   ├── workflows/scenarios/      # NestJS, Django, Go Fiber worked examples
│   └── skills/                   # export-backend, export-auth, export-database, export-frontend, export-rag
└── .github/workflows/            # CI/CD (Railway + Netlify + GitHub Pages)
```

---

## 🧪 Testing

### Frontend

```bash
cd intellistack/frontend
npm test              # Unit tests (Vitest)
npm run test:e2e      # E2E tests (Playwright)
npm run lighthouse    # Performance + accessibility audit
```

### Backend

```bash
cd intellistack/backend
pytest
```

---

## 🚢 Deployment

All deployments are automated via GitHub Actions on push to `main`:

| Workflow | Path Trigger | Target |
|---------|-------------|--------|
| `deploy-backend.yml` | `intellistack/backend/**` | Railway |
| `deploy-auth.yml` | `intellistack/auth-server/**` | Railway |
| `deploy-frontend.yml` | `intellistack/frontend/**` | Netlify |
| `deploy-docs.yml` | `intellistack/content/**` | GitHub Pages |

**Required GitHub Secrets:** `RAILWAY_TOKEN`, `NETLIFY_SITE_ID`, `NETLIFY_AUTH_TOKEN`, `RAILWAY_AUTH_URL`, `RAILWAY_BACKEND_URL`

---

## 📊 Implementation Progress

```
Phase 0  ████████████████████  Complete  — Vertical Slice
Phase 1  ████████████████████  Complete  — Setup & Infrastructure
Phase 2  ████████████████████  Complete  — Auth & Foundation
Phase 3  ████████████████████  Complete  — Student Learning (5-Stage Path)
Phase 4  ████████████████████  Complete  — Content Authoring
Phase 5  ████████████████████  Complete  — Institution Management
Phase 6  ████████████████████  Complete  — RAG Chatbot
Phase 7  ░░░░░░░░░░░░░░░░░░░░  Pending   — AI Tutor
Phase 8  ░░░░░░░░░░░░░░░░░░░░  Pending   — Community Features
Phase 9  ░░░░░░░░░░░░░░░░░░░░  Pending   — Assessment Engine
Phase 10 ░░░░░░░░░░░░░░░░░░░░  Pending   — Personalization
Phase 11 ░░░░░░░░░░░░░░░░░░░░  Pending   — Production Polish
```

**Overall: 74.5% complete (38 / 51 tasks)**

---

## 🤝 Contributing

1. Fork the repository and create a branch: `git checkout -b <phase>-<feature>`
2. Keep commits small and reference task IDs
3. Ensure tests pass before opening a PR against `main`

**Code Standards:** Python — PEP 8, type hints, async-first · TypeScript — strict mode · React — functional components only · DB — all schema changes via Alembic migrations

---

## 📄 License

MIT — see [LICENSE](./LICENSE)

---

<div align="center">

**[Try the Live App](https://intellistack-app.netlify.app/) · [Read the Docs](https://saramali15792.github.io/AINativeBook/)**

</div>
