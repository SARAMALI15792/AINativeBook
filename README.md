<div align="center">

# 🤖 IntelliStack Platform

### AI-Native Learning Management System for Physical AI & Humanoid Robotics

[![Live App](https://img.shields.io/badge/🌐_Live_App-intellistack--app.netlify.app-00C7B7?style=for-the-badge&logo=netlify)](https://intellistack-app.netlify.app/)
[![Docs](https://img.shields.io/badge/📚_Docs-GitHub_Pages-181717?style=for-the-badge&logo=github)](https://saramali15792.github.io/AINativeBook/)
[![Backend](https://img.shields.io/badge/⚙️_API-Railway-0B0D0E?style=for-the-badge&logo=railway)](https://intellistack-backend-production.up.railway.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

<br/>

> **IntelliStack** is a full-stack, AI-native LMS built for the next generation of robotics engineers.
> It combines progressive learning paths, a RAG-powered chatbot with citations, an AI Socratic tutor,
> content authoring tools, and institution management — all in one platform.

<br/>

![Platform Banner](https://img.shields.io/badge/Phases_Complete-6_of_11-blueviolet?style=flat-square)
![Tasks Done](https://img.shields.io/badge/Tasks-38_of_51_done-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)

</div>

---

## 🌐 Live Application

| Service | URL | Status |
|---------|-----|--------|
| **Frontend** | [https://intellistack-app.netlify.app/](https://intellistack-app.netlify.app/) | [![Netlify Status](https://api.netlify.com/api/v1/badges/placeholder/deploy-status)](https://intellistack-app.netlify.app/) |
| **Backend API** | [Railway — intellistack-backend](https://intellistack-backend-production.up.railway.app) | Auto-deploy on push |
| **Auth Server** | [Railway — intellistack-auth](https://intellistack-auth-production.up.railway.app) | Auto-deploy on push |
| **Docs** | [GitHub Pages](https://saramali15792.github.io/AINativeBook/) | Auto-deploy on push |

---

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph Client["🖥️ Client Layer"]
        FE["Next.js 14 Frontend<br/>(Netlify)"]
        DOCS["Docusaurus Docs<br/>(GitHub Pages)"]
    end

    subgraph Auth["🔐 Auth Layer"]
        AUTH["Better-Auth OIDC Server<br/>(Railway · Node.js)"]
        JWKS["JWKS Endpoint<br/>/.well-known/jwks.json"]
    end

    subgraph API["⚙️ API Layer"]
        BACKEND["FastAPI Backend<br/>(Railway · Python 3.11)"]
        MW["JWKS Middleware<br/>JWT Validation"]
    end

    subgraph AI["🤖 AI Layer"]
        RAG["RAG Pipeline<br/>Qdrant + Cohere + OpenAI"]
        TUTOR["AI Tutor<br/>LangGraph · Socratic Method"]
        CHATKIT["ChatKit<br/>Streaming SSE"]
    end

    subgraph Data["🗄️ Data Layer"]
        PG[("PostgreSQL<br/>(Neon)")]
        REDIS[("Redis<br/>Cache + Rate Limit")]
        QDRANT[("Qdrant<br/>Vector Store")]
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
    participant U as 👤 User
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
    AUTH-->>API: Token valid ✓
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
    S1["🔵 Stage 1<br/>Foundations"]
    S2["🟢 Stage 2<br/>ROS 2 & Simulation"]
    S3["🟡 Stage 3<br/>Perception & Planning"]
    S4["🟠 Stage 4<br/>AI Integration"]
    S5["🔴 Stage 5<br/>Capstone"]

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

Each stage unlocks progressively based on prerequisite completion. Progress is tracked at lesson, exercise, and assessment level with badge issuance and certificate generation.

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
[![Alembic](https://img.shields.io/badge/Alembic-1.13+-6BA539?style=flat)](https://alembic.sqlalchemy.org/)
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
- OpenAI + SSE streaming
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
- Password reset via Resend email

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
- User profile-based learning path adjustments
- Progress tracking (lesson / exercise / assessment)
- Badge issuance & certificate generation

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
| Docker | Latest |
| PostgreSQL | 16+ (or Neon cloud) |
| Redis | 7+ |
| Qdrant | 1.7+ (or Qdrant Cloud) |

### 1. Clone the Repository

```bash
git clone https://github.com/SARAMALI15792/AINativeBook.git
cd AINativeBook
```

### 2. Configure Environment Variables

```bash
# Root env (backend + shared services)
cp intellistack/.env.example intellistack/.env

# Auth server env
cp intellistack/auth-server/.env.example intellistack/auth-server/.env
```

Edit `intellistack/.env` with your values:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/intellistack

# Cache
REDIS_URL=redis://localhost:6379/0

# Vector Store
QDRANT_HOST=localhost
QDRANT_PORT=6333

# AI Services
OPENAI_API_KEY=sk-...
COHERE_API_KEY=...          # optional — for reranking

# Better-Auth
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_SECRET=<min-32-random-chars>

# OAuth (optional)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
```

### 3. Start the Auth Server

```bash
cd intellistack/auth-server
npm install
npm run migrate          # run DB migrations
npm run dev              # http://localhost:3001
```

Test: `GET http://localhost:3001/.well-known/openid-configuration`

### 4. Start the Backend API

```bash
cd intellistack/backend
pip install -r requirements.txt
alembic upgrade head     # run DB migrations
uvicorn src.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

### 5. Start the Frontend

```bash
cd intellistack/frontend
npm install
npm run dev              # http://localhost:3000
```

Open [http://localhost:3000](http://localhost:3000) — or visit the live app at **[https://intellistack-app.netlify.app/](https://intellistack-app.netlify.app/)**

---

## 📖 How to Use the Platform

### For Students

1. **Sign up** at [intellistack-app.netlify.app](https://intellistack-app.netlify.app/) using email or Google/GitHub
2. **Complete onboarding** — set your learning preferences and background
3. **Start Stage 1** — Foundations of Physical AI
4. **Work through lessons** — video, text, and interactive Pyodide coding exercises
5. **Ask the AI Chatbot** — click the chat button to query the RAG chatbot for help
6. **Use the AI Tutor** — get Socratic guidance on problems without being given direct answers
7. **Complete assessments** — unlock the next stage after passing requirements
8. **Earn badges & certificates** upon stage completion

### For Instructors

1. Log in with an `instructor` role account
2. Navigate to **Content Authoring** to create/edit lessons in MDX
3. Submit content for review → it enters the `in_review` workflow
4. Once published, content is automatically ingested into the RAG vector store
5. Manage your **Cohort** — add students, set enrollment limits
6. View **Analytics** — track student progress and engagement

### For Admins

1. Log in with an `admin` role account
2. Manage institutions, cohorts, and user roles from the admin dashboard
3. Monitor platform health at `/health/detail` and Prometheus metrics at `/metrics`
4. Configure webhooks for external integrations

---

## 📁 Project Structure

```
AINativeBook/
│
├── 🌐 intellistack/
│   ├── .env.example                 # Root environment template
│   │
│   ├── 🐍 backend/                  # FastAPI Python backend
│   │   ├── src/
│   │   │   ├── main.py              # App entry point
│   │   │   ├── config/              # Settings & structured logging
│   │   │   ├── core/                # Domain modules
│   │   │   │   ├── auth/            # Auth routes & JWT handling
│   │   │   │   ├── users/           # User management
│   │   │   │   ├── content/         # Content CRUD & versioning
│   │   │   │   ├── learning/        # Learning paths & progress
│   │   │   │   ├── institution/     # Cohorts & analytics
│   │   │   │   └── assessment/      # Quizzes & grading
│   │   │   ├── ai/
│   │   │   │   ├── rag/             # RAG pipeline (Qdrant + Cohere + OpenAI)
│   │   │   │   ├── tutor/           # AI Tutor (LangGraph)
│   │   │   │   ├── chatkit/         # ChatKit streaming server
│   │   │   │   └── personalization/ # Adaptive learning engine
│   │   │   └── shared/              # DB, middleware, metrics
│   │   └── alembic/                 # DB migrations
│   │
│   ├── 🔐 auth-server/              # Better-Auth OIDC (TypeScript)
│   │   └── src/
│   │       ├── index.ts             # Express entry point
│   │       ├── auth.ts              # Better-Auth config
│   │       └── db.ts                # Drizzle ORM + Neon
│   │
│   ├── ⚛️  frontend/                # Next.js 14 (App Router)
│   │   └── src/
│   │       ├── app/                 # Pages & layouts
│   │       ├── components/          # UI components
│   │       ├── contexts/            # Auth & app contexts
│   │       └── lib/                 # API clients & utilities
│   │
│   └── 📚 content/                  # Docusaurus learning content
│
├── 📋 specs/                        # SDD artifacts
│   └── 001-intellistack-platform/
│       ├── spec.md                  # Requirements (~1400 lines)
│       ├── plan.md                  # Architecture decisions
│       └── tasks.md                 # Task tracking
│
├── 📜 history/                      # Prompt History Records (PHRs)
│   ├── prompts/                     # Session records
│   └── adr/                         # Architecture Decision Records
│
└── ⚙️  .github/workflows/           # CI/CD pipelines
    ├── deploy-backend.yml           # → Railway
    ├── deploy-auth.yml              # → Railway
    ├── deploy-frontend.yml          # → Netlify
    └── deploy-docs.yml              # → GitHub Pages
```

---

## 🔌 API Reference

### Backend — `https://intellistack-backend-production.up.railway.app`

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/health` | Basic health check |
| `GET` | `/health/detail` | Health + live metrics |
| `GET` | `/metrics` | Prometheus scrape endpoint |
| `GET` | `/api/v1` | API root |
| `GET` | `/docs` | Swagger UI (dev only) |

### Auth Server — `https://intellistack-auth-production.up.railway.app`

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/auth/sign-up/email` | Email registration |
| `POST` | `/api/auth/sign-in/email` | Email login |
| `POST` | `/api/auth/sign-in/social` | OAuth (Google / GitHub) |
| `POST` | `/api/auth/forget-password` | Request password reset |
| `POST` | `/api/auth/reset-password` | Reset with token |
| `GET` | `/.well-known/openid-configuration` | OIDC discovery |
| `GET` | `/.well-known/jwks.json` | Public key set (JWKS) |

---

## 🧪 Testing

### Frontend (Vitest + Playwright)
```bash
cd intellistack/frontend

npm test              # Unit tests (Vitest)
npm run test:watch    # Watch mode
npm run test:e2e      # E2E tests (Playwright)
npm run lighthouse    # Accessibility + performance audit
```

### Backend (pytest)
```bash
cd intellistack/backend
pytest
```

### Auth Server (TypeScript checks)
```bash
cd intellistack/auth-server
npm run type-check
npm run lint
```

---

## 🚢 Deployment

### CI/CD — GitHub Actions

| Workflow | Trigger Path | Target |
|---------|-------------|--------|
| `deploy-backend.yml` | `intellistack/backend/**` | Railway |
| `deploy-auth.yml` | `intellistack/auth-server/**` | Railway |
| `deploy-frontend.yml` | `intellistack/frontend/**` | Netlify |
| `deploy-docs.yml` | `intellistack/content/**` | GitHub Pages |

All pipelines trigger automatically on push to `main`.

### Required GitHub Secrets

| Secret | Used By |
|--------|---------|
| `RAILWAY_TOKEN` | Backend + Auth deploys |
| `NETLIFY_SITE_ID` | Frontend deploy |
| `NETLIFY_AUTH_TOKEN` | Frontend deploy |
| `RAILWAY_AUTH_URL` | Docs build env |
| `RAILWAY_BACKEND_URL` | Docs build env |

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

1. Fork the repository
2. Create a feature branch: `git checkout -b <phase>-<feature-name>`
3. Follow the **Spec-Driven workflow**: write spec → plan → tasks → implement
4. Keep commits small and focused
5. Ensure all tests pass before opening a PR
6. Open a pull request against `main`

**Code Standards:**
- **Python:** PEP 8 · type hints required · async-first
- **TypeScript:** strict mode · no untyped `any`
- **React:** functional components · hooks only
- **Database:** all schema changes via Alembic migrations

---

## 📄 License

```
MIT License

Copyright (c) 2026 IntelliStack Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

---

<div align="center">

Built with ❤️ using [Spec-Driven Development](https://github.com/SARAMALI15792/AINativeBook/tree/main/specs) and [Claude Code](https://claude.ai/code)

**[🌐 Try the Live App](https://intellistack-app.netlify.app/) · [📚 Read the Docs](https://saramali15792.github.io/AINativeBook/) · [⚙️ API Reference](https://intellistack-backend-production.up.railway.app/docs)**

</div>
