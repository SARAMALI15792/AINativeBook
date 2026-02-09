# Implementation Plan: IntelliStack Platform

**Branch**: `001-intellistack-platform` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-intellistack-platform/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

IntelliStack is an AI-native learning platform for Physical AI & Humanoid Robotics education. The platform delivers a 5-stage progressive curriculum with simulation-first pedagogy, AI tutoring (Socratic method), RAG-powered content search, and comprehensive assessment systems. Technical approach: Next.js frontend (Vercel), FastAPI backend (Fly.io), Neon PostgreSQL, Qdrant vector DB, OpenAI/LangGraph for AI orchestration, Better-Auth for authentication, and Docusaurus for MDX content.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLAlchemy/SQLModel, Alembic, LangGraph, LlamaIndex, Next.js 14, Tailwind CSS, ShadCN UI, TanStack Query, Zustand, Better-Auth
**Storage**: Neon PostgreSQL (relational), Qdrant (vector), Redis (cache/queue)
**Testing**: pytest (backend), Vitest (frontend), Playwright (E2E)
**Target Platform**: Web (responsive), Ubuntu 22.04 (deployment), Cloud GPU instances (simulation)
**Project Type**: Web application (frontend + backend + content)
**Performance Goals**: <3s page load (p95), <5s AI response (p95), 10k concurrent simulation sessions (SC-006)
**Constraints**: 99.5% uptime during academic terms, 60 req/min rate limit, 25 hrs/month simulation quota per user
**Scale/Scope**: 10k concurrent users, ~100 FRs, 5 learning stages, 10 service domains

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Compliance |
|-----------|-------------|------------|
| **I. Simulation Before Hardware** | FR-020 enforces simulation checkpoints; Stages 1-4 simulation-only; FR-064 blocks hardware without simulation mastery | ✅ PASS |
| **II. Safety and Responsibility** | FR-052 (10-item safety assessment), FR-063/64/65 (safety enforcement) | ✅ PASS |
| **III. Understanding Before Automation** | FR-027/28 (Socratic AI tutor), FR-046 (Understanding Verification Framework) | ✅ PASS |
| **IV. AI as Learning Guide** | FR-026-035 define AI tutor guardrails; AI explains, doesn't complete | ✅ PASS |
| **V. Progressive Learning Path** | FR-001-012 implement staged progression; FR-010/11 Challenge Pathway | ✅ PASS |
| **VI. Practical Project Focus** | FR-044 (practical demonstration), FR-015 (portfolio), FR-057 (showcase) | ✅ PASS |
| **VII. Ethical AI** | Addressed in curriculum content (out of platform scope) | ✅ PASS (N/A) |
| **VIII. Embrace Failure** | FR-030 (systematic debugging), FR-048/49 (learning from failures) | ✅ PASS |
| **IX. Sim-to-Real Mastery** | FR-023 (domain randomization), Stage 4 content, FR-020 gates | ✅ PASS |

## Project Structure

### Documentation (this feature)

```text
specs/001-intellistack-platform/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── auth.openapi.yaml
│   ├── learning.openapi.yaml
│   ├── content.openapi.yaml
│   ├── assessment.openapi.yaml
│   ├── ai.openapi.yaml
│   ├── community.openapi.yaml
│   └── institution.openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
intellistack/
├── backend/
│   ├── src/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── config/
│   │   │   ├── settings.py            # Pydantic settings, env vars
│   │   │   └── logging.py             # Structured logging config
│   │   ├── core/
│   │   │   ├── auth/                  # FR-036-042: Authentication & RBAC
│   │   │   │   ├── models.py
│   │   │   │   ├── service.py
│   │   │   │   └── routes.py
│   │   │   ├── learning/              # FR-001-015: Progress, prerequisites, badges
│   │   │   │   ├── models.py
│   │   │   │   ├── service.py
│   │   │   │   └── routes.py
│   │   │   ├── content/               # FR-059-060: Course/stage/content CRUD
│   │   │   │   ├── models.py
│   │   │   │   ├── service.py
│   │   │   │   └── routes.py
│   │   │   ├── assessment/            # FR-043-052: Quizzes, projects, rubrics
│   │   │   │   ├── models.py
│   │   │   │   ├── service.py
│   │   │   │   └── routes.py
│   │   │   ├── community/             # FR-053-058: Forums, groups, mentorship
│   │   │   │   ├── models.py
│   │   │   │   ├── service.py
│   │   │   │   └── routes.py
│   │   │   ├── institution/           # FR-039: Institution management
│   │   │   │   ├── models.py
│   │   │   │   ├── service.py
│   │   │   │   └── routes.py
│   │   │   └── analytics/             # FR-102, FR-110: Metrics, tracing
│   │   │       ├── models.py
│   │   │       └── service.py
│   │   ├── ai/
│   │   │   ├── tutor/                 # FR-026-035: Socratic tutoring
│   │   │   │   ├── agents.py          # LangGraph agent definitions
│   │   │   │   ├── guardrails.py      # Socratic guardrail logic
│   │   │   │   └── service.py
│   │   │   ├── rag/                   # FR-066-080: RAG chatbot
│   │   │   │   ├── pipelines/
│   │   │   │   │   ├── query_pipeline.py
│   │   │   │   │   └── ingestion_pipeline.py
│   │   │   │   ├── retrieval.py
│   │   │   │   └── service.py
│   │   │   ├── personalization/       # FR-081-090: Adaptive content
│   │   │   │   ├── profile.py
│   │   │   │   ├── adaptation.py
│   │   │   │   └── translation.py
│   │   │   └── shared/
│   │   │       ├── llm_client.py      # OpenAI/LLM abstraction
│   │   │       └── prompts.py         # Prompt templates
│   │   ├── simulation/                # FR-016-025: Gazebo/Isaac integration
│   │   │   ├── connector.py
│   │   │   ├── state_manager.py
│   │   │   └── quota_tracker.py
│   │   ├── shared/
│   │   │   ├── database.py            # SQLAlchemy session management
│   │   │   ├── exceptions.py          # Custom exceptions
│   │   │   ├── middleware.py          # Rate limiting, error handling
│   │   │   └── utils.py
│   │   └── tasks/                     # Celery/Dramatiq async tasks
│   │       ├── content_indexing.py
│   │       ├── badge_issuance.py
│   │       └── notifications.py
│   ├── alembic/
│   │   └── versions/
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── contract/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/                # Auth pages (login, register, recover)
│   │   │   │   ├── login/
│   │   │   │   ├── register/
│   │   │   │   └── layout.tsx
│   │   │   ├── (dashboard)/           # Main app layout
│   │   │   │   ├── learn/             # Learning content viewer
│   │   │   │   │   ├── [stageId]/
│   │   │   │   │   │   └── [contentId]/
│   │   │   │   │   │       └── page.tsx
│   │   │   │   │   └── page.tsx       # Learning path overview
│   │   │   │   ├── assessments/       # Quiz/project UI
│   │   │   │   ├── ai/                # AI tutor & RAG chatbot
│   │   │   │   │   ├── tutor/
│   │   │   │   │   └── chatbot/
│   │   │   │   ├── community/         # Forums, groups, mentorship
│   │   │   │   ├── portfolio/         # Student portfolio
│   │   │   │   ├── profile/           # User profile & settings
│   │   │   │   └── admin/             # Platform admin (role-gated)
│   │   │   ├── (institution)/         # Institution admin portal
│   │   │   │   ├── cohorts/
│   │   │   │   ├── analytics/
│   │   │   │   └── branding/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx               # Landing/home
│   │   ├── components/
│   │   │   ├── ui/                    # ShadCN UI components
│   │   │   ├── learning/              # Content viewer, progress bars
│   │   │   ├── ai/                    # Chat interfaces, streaming
│   │   │   ├── assessment/            # Quiz forms, rubric display
│   │   │   └── shared/                # Layout, navigation, skeleton
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useProgress.ts
│   │   │   ├── useAIChat.ts
│   │   │   └── useStreaming.ts
│   │   ├── lib/
│   │   │   ├── api.ts                 # API client (TanStack Query)
│   │   │   ├── auth.ts                # Better-Auth client
│   │   │   └── utils.ts
│   │   ├── stores/
│   │   │   ├── userStore.ts           # Zustand stores
│   │   │   ├── learningStore.ts
│   │   │   └── chatStore.ts
│   │   └── types/
│   │       └── index.ts               # TypeScript types
│   └── tests/
│       ├── unit/
│       └── e2e/                       # Playwright tests
│
├── content/                           # Docusaurus MDX content
│   ├── docusaurus.config.js
│   ├── docs/
│   │   ├── stage-1/
│   │   ├── stage-2/
│   │   ├── stage-3/
│   │   ├── stage-4/
│   │   └── stage-5/
│   └── static/
│
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── content.Dockerfile
├── docker-compose.yml
├── docker-compose.dev.yml
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── deploy-staging.yml
        └── deploy-production.yml
```

**Structure Decision**: Web application structure with separated backend (FastAPI), frontend (Next.js), and content (Docusaurus). Monorepo approach for simplified dependency management and CI/CD. Service domains mapped to feature requirement clusters.

## Complexity Tracking

> No constitution violations requiring justification. Architecture complexity justified by:
> - 10 service domains required by 100+ functional requirements
> - AI/RAG pipeline requires dedicated orchestration (LangGraph)
> - Multi-tenant institution support requires isolated data paths
> - Real-time streaming for AI responses requires WebSocket/SSE infrastructure

---

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INTELLISTACK ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────────┐     ┌─────────────────────────────┐            │
│  │     Next.js Frontend        │     │    Docusaurus Content       │            │
│  │        (Vercel)             │     │       (Vercel)              │            │
│  │  • Learning Dashboard       │     │  • MDX Course Content       │            │
│  │  • AI Chat Interfaces       │     │  • Stage Documentation      │            │
│  │  • Assessment UI            │     │  • Interactive Exercises    │            │
│  │  • Admin Portals            │     │                             │            │
│  └─────────────┬───────────────┘     └─────────────┬───────────────┘            │
│                │                                    │                            │
│                └──────────────┬─────────────────────┘                            │
│                               │                                                  │
│                               ▼                                                  │
│              ┌────────────────────────────────────┐                              │
│              │         FastAPI Gateway            │                              │
│              │           (Fly.io)                 │                              │
│              │  • Better-Auth Integration         │                              │
│              │  • Rate Limiting (60 req/min)      │                              │
│              │  • Request Tracing                 │                              │
│              └────────────────┬───────────────────┘                              │
│                               │                                                  │
│    ┌──────────────────────────┼──────────────────────────┐                      │
│    │                          │                          │                      │
│    ▼                          ▼                          ▼                      │
│  ┌────────────────┐  ┌────────────────────┐  ┌─────────────────────┐           │
│  │  Core Services │  │    AI Services     │  │ Simulation Service  │           │
│  │                │  │                    │  │                     │           │
│  │  • Auth        │  │  • AI Tutor        │  │  • Gazebo Connector │           │
│  │  • Learning    │  │    (LangGraph)     │  │  • Quota Tracker    │           │
│  │  • Content     │  │  • RAG Chatbot     │  │  • State Manager    │           │
│  │  • Assessment  │  │    (LlamaIndex)    │  │                     │           │
│  │  • Community   │  │  • Personalization │  │                     │           │
│  │  • Institution │  │                    │  │                     │           │
│  │  • Analytics   │  │                    │  │                     │           │
│  └───────┬────────┘  └────────┬───────────┘  └──────────┬──────────┘           │
│          │                    │                         │                       │
│          └────────────────────┼─────────────────────────┘                       │
│                               │                                                  │
│    ┌──────────────────────────┼──────────────────────────┐                      │
│    │                          │                          │                      │
│    ▼                          ▼                          ▼                      │
│  ┌────────────────┐  ┌────────────────────┐  ┌─────────────────────┐           │
│  │   PostgreSQL   │  │       Redis        │  │      Qdrant         │           │
│  │    (Neon)      │  │   (Cache + Queue)  │  │   (Vector DB)       │           │
│  │                │  │                    │  │                     │           │
│  │  • Users       │  │  • Session Cache   │  │  • textbook_content │           │
│  │  • Progress    │  │  • Rate Limiting   │  │    collection       │           │
│  │  • Content     │  │  • Task Queue      │  │  • 1536-dim vectors │           │
│  │  • Assessments │  │  • Translation     │  │  • Hybrid search    │           │
│  │  • Community   │  │    Cache           │  │                     │           │
│  └────────────────┘  └────────────────────┘  └─────────────────────┘           │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        External Services                                 │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │    │
│  │  │   OpenAI    │  │   Cohere    │  │ Cloud GPU   │  │    SMTP     │    │    │
│  │  │  (GPT-4o)   │  │ (Reranking) │  │ (Sim Pool)  │  │   (Email)   │    │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Service Decomposition

| Service | FRs | Responsibility | Key Dependencies |
|---------|-----|----------------|------------------|
| **Auth** | FR-036–042 | Authentication, RBAC, sessions, audit | Better-Auth, PostgreSQL |
| **Learning** | FR-001–015 | Progress, prerequisites, badges, certificates, challenge pathway | PostgreSQL, Redis |
| **Content** | FR-059–060 | Course/stage/content CRUD, versioning, review workflow | PostgreSQL, Docusaurus |
| **Assessment** | FR-043–052 | Delivery, submissions, rubrics, peer review, similarity | PostgreSQL, Celery |
| **AI Tutor** | FR-026–035 | Socratic tutoring, debugging guidance, code review, guardrails | LangGraph, OpenAI |
| **RAG Chatbot** | FR-066–080 | Retrieval, citation, streaming, context management | LlamaIndex, Qdrant, OpenAI |
| **Personalization** | FR-081–090 | Profile, content adaptation, translation | OpenAI, Redis (cache) |
| **Community** | FR-053–058 | Forums, study groups, mentorship, moderation | PostgreSQL |
| **Simulation** | FR-016–025 | Gazebo/Isaac integration, state management, quotas | Cloud GPU, Redis |
| **Analytics** | FR-102, FR-110 | Metrics, dashboards, request tracing | PostgreSQL, Redis |

---

## Implementation Phases

### Phase 1: Core Platform (Weeks 1-6)

**Focus**: Foundation infrastructure and authentication

| Week | Deliverables | FRs Covered |
|------|--------------|-------------|
| 1-2 | Project scaffolding, Docker setup, CI/CD pipeline, Database schema | FR-091, FR-096, FR-100 |
| 3-4 | Auth service (Better-Auth, RBAC, sessions), User management | FR-036–042 |
| 5-6 | Content service (stage/content CRUD), Basic frontend (auth, dashboard) | FR-059–060 |

**Exit Criteria**:
- [ ] User can register, login, logout
- [ ] Roles can be assigned/revoked with audit trail
- [ ] Content can be created, versioned, published
- [ ] CI/CD deploys to staging environment

### Phase 2: Learning & AI (Weeks 7-12)

**Focus**: Learning management and AI features

| Week | Deliverables | FRs Covered |
|------|--------------|-------------|
| 7-8 | Learning service (progress, prerequisites, badges) | FR-001–012 |
| 9-10 | RAG pipeline (ingestion, Qdrant, retrieval, streaming) | FR-066–080 |
| 11-12 | AI Tutor (LangGraph agents, Socratic guardrails) | FR-026–035 |

**Exit Criteria**:
- [ ] Student progress tracked across stages
- [ ] Prerequisites enforced for content access
- [ ] RAG chatbot answers questions with citations
- [ ] AI tutor refuses direct answers, guides learning

### Phase 3: Full Features (Weeks 13-18)

**Focus**: Complete feature set

| Week | Deliverables | FRs Covered |
|------|--------------|-------------|
| 13-14 | Assessment service (quizzes, projects, rubrics, peer review) | FR-043–052 |
| 15-16 | Community features (forums, study groups, mentorship) | FR-053–058 |
| 17-18 | Institution admin (cohorts, branding, analytics), Personalization | FR-039, FR-081–090 |

**Exit Criteria**:
- [ ] Assessments can be taken, graded (auto + manual)
- [ ] Community forums operational with moderation
- [ ] Institutions can manage cohorts with custom branding
- [ ] Personalization adapts content to user level

### Phase 4: Polish & Scale (Weeks 19-24)

**Focus**: Production readiness

| Week | Deliverables | FRs Covered |
|------|--------------|-------------|
| 19-20 | Simulation integration (Gazebo connector), Quota management | FR-016–025 |
| 21-22 | Performance optimization, Security hardening, Accessibility audit | FR-101–110, SC-011 |
| 23-24 | Demo mode, API documentation, Deployment automation | FR-112–115 |

**Exit Criteria**:
- [ ] 10k concurrent simulation sessions supported (SC-006)
- [ ] 99.5% uptime achieved in staging (SC-007)
- [ ] Demo video generates in ≤90 seconds
- [ ] All public APIs documented

---

## Critical Files

| File | Purpose | Phase |
|------|---------|-------|
| `backend/src/config/settings.py` | Pydantic settings, environment variables | 1 |
| `backend/src/core/auth/service.py` | Better-Auth integration, RBAC logic | 1 |
| `backend/src/core/learning/service.py` | Progress tracking, prerequisite enforcement | 2 |
| `backend/src/ai/rag/pipelines/query_pipeline.py` | LangGraph RAG orchestration | 2 |
| `backend/src/ai/tutor/guardrails.py` | Socratic guardrail logic (FR-027, FR-028) | 2 |
| `frontend/src/app/(dashboard)/learn/[stageId]/[contentId]/page.tsx` | Main content viewer | 2 |
| `frontend/src/components/ai/ChatInterface.tsx` | AI chat with streaming | 2 |
| `backend/src/core/assessment/service.py` | Assessment delivery, grading | 3 |

---

## Risk Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| RAG quality issues | High | Medium | Reranking pipeline, instructor escalation, quality monitoring |
| Simulation complexity | High | High | Abstraction layer, cloud-first, defer Isaac Sim to Phase 4+ |
| AI guardrail bypass | Medium | Medium | Multi-layer defense, red-teaming, instructor review queue |
| Database scaling | Medium | Low | Connection pooling, read replicas, Neon auto-scaling |
| OpenAI rate limits | Medium | Medium | Response caching, request batching, multiple API keys |
| Scope creep | High | High | Strict phase boundaries, feature freezes, weekly scope reviews |

---

## ADR Candidates

The following architectural decisions warrant formal ADR documentation:

| # | Decision | Status | Rationale |
|---|----------|--------|-----------|
| ADR-001 | Monorepo structure | Proposed | Simplified CI/CD, shared types, coordinated releases |
| ADR-002 | Better-Auth vs NextAuth.js | Proposed | Server SDK for FastAPI, multi-role support |
| ADR-003 | LangGraph for AI orchestration | Proposed | Stateful workflows, guardrail integration |
| ADR-004 | Qdrant for vector storage | Proposed | Self-hostable, filtering support, hybrid search |
| ADR-005 | Hybrid content storage (Git + Postgres) | Proposed | MDX authoring experience + metadata management |
| ADR-006 | SSE for AI streaming | Proposed | Simpler than WebSocket for unidirectional flow |
| ADR-007 | Cloud-first simulation | Proposed | Removes hardware barrier, scales with demand |
| ADR-008 | AI translation with caching | Proposed | Cost-effective, quality caveats documented |

---

## Verification Plan

| Test Type | Tool | Coverage Target | Phase |
|-----------|------|-----------------|-------|
| Unit Tests | pytest, Vitest | 80% critical paths | All |
| Integration Tests | pytest | API contract compliance | 2+ |
| E2E Tests | Playwright | 6 critical user journeys | 3+ |
| RAG Quality | Custom harness | 90% accuracy on test corpus (SC-016) | 2 |
| Performance | k6/Locust | 10k concurrent users (SC-006) | 4 |
| Accessibility | axe-core | WCAG 2.1 AA (SC-011) | 4 |
| Security | OWASP ZAP | No critical vulnerabilities | 4 |

---

## Generated Artifacts

This planning phase produced:

| Artifact | Path | Description |
|----------|------|-------------|
| Implementation Plan | `specs/001-intellistack-platform/plan.md` | This document |
| Research Document | `specs/001-intellistack-platform/research.md` | Technical decisions and rationale |
| Data Model | `specs/001-intellistack-platform/data-model.md` | Entity definitions and relationships |
| Quickstart Guide | `specs/001-intellistack-platform/quickstart.md` | Development setup instructions |
| Auth API Contract | `specs/001-intellistack-platform/contracts/auth.openapi.yaml` | Authentication endpoints |
| Learning API Contract | `specs/001-intellistack-platform/contracts/learning.openapi.yaml` | Progress and badge endpoints |
| AI API Contract | `specs/001-intellistack-platform/contracts/ai.openapi.yaml` | Tutor, RAG, personalization endpoints |

---

## Next Steps

1. **Run `/sp.tasks`** to generate detailed implementation tasks from this plan
2. **Create ADRs** for decisions marked "Proposed" above
3. **Set up repository** with scaffolding from project structure
4. **Begin Phase 1** implementation

---

*Plan completed: 2026-02-07*
*Branch: `001-intellistack-platform`*
