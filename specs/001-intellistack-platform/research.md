# Research: IntelliStack Platform

**Branch**: `001-intellistack-platform` | **Date**: 2026-02-07

## Purpose

This document consolidates research findings for all technical decisions and unknowns identified during planning. Each section documents the decision, rationale, and alternatives considered.

---

## 1. Authentication Strategy

### Decision
**Better-Auth** for authentication with global identity pool + institution assignment model.

### Rationale
- Better-Auth provides both client and server SDKs, simplifying integration
- Supports multi-role users (Student, Author, Instructor, Institution Admin, Platform Admin)
- Session-based authentication with configurable timeouts (FR-042)
- Built-in audit trail capabilities (FR-040)
- Supports delegated institution administration (FR-039)

### Alternatives Considered
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| NextAuth.js | Popular, well-documented | Server-only, requires custom API integration | Less flexible for FastAPI backend |
| Auth0 | Enterprise-grade, many features | Cost at scale, vendor lock-in | Adds external dependency, cost concerns |
| Custom JWT | Full control | Development time, security risk | Reinventing wheel, security maintenance burden |

### Best Practices
- Store session tokens in HTTP-only cookies
- Implement CSRF protection
- Use refresh token rotation
- Enforce rate limiting on auth endpoints (10 req/min for unauthenticated)

---

## 2. RAG Pipeline Architecture

### Decision
**LangGraph + LlamaIndex + Qdrant** for RAG orchestration.

### Rationale
- LangGraph provides stateful agent workflows for complex retrieval patterns
- LlamaIndex handles document processing, chunking, and embedding
- Qdrant offers high-performance vector search with filtering (stage-based access control)
- OpenAI ada-002 embeddings (1536 dimensions) for semantic search

### RAG Pipeline Flow
```
Query → Query Analyzer → Access Control Filter → Hybrid Search (Qdrant)
    → Re-ranking (Cohere) → Context Builder → Response Gen (GPT-4o)
    → Streaming SSE → Citation Formatter
```

### Alternatives Considered
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Pinecone | Managed, scalable | Cost, vendor lock-in | Qdrant provides similar features, self-hostable |
| Weaviate | GraphQL API, hybrid search | More complex setup | Qdrant simpler for our use case |
| pgvector | Uses existing Postgres | Limited scale, fewer features | Performance concerns at 10k users |
| ChromaDB | Simple, embedded | Limited scaling, no cloud option | Production readiness concerns |

### Best Practices
- Chunk size: 512 tokens with 50-token overlap
- Hybrid search: 70% semantic + 30% keyword (BM25)
- Re-ranking: Top 20 → Re-rank → Top 5 for context
- Cache frequent queries (Redis, 15-minute TTL)
- Citation format: Chapter:Section:Paragraph

---

## 3. AI Tutor Guardrails

### Decision
**Multi-layer guardrail system** with escalation path.

### Guardrail Architecture
```
User Request → Intent Classifier →
  ├── Concept Question → Generate Socratic Response
  ├── Code Help → Guidance (hints, no solutions)
  ├── Debugging → Systematic methodology guide
  └── Direct Answer Request → Guardrail Check →
        ├── Attempt 1-3: Polite redirect + explain philosophy
        ├── Attempt 4-5: Cooldown (5 min) + alternatives offered
        └── Attempt 6+: Instructor notification
```

### Rationale
- Aligns with Constitution Principle III (Understanding Before Automation)
- Aligns with Constitution Principle IV (AI as Learning Guide)
- Progressive escalation prevents frustration while maintaining learning integrity
- Instructor notification provides human oversight for persistent cases

### Implementation Notes
- Track attempt counter per session (reset after 30 min inactivity)
- Store guardrail events for quality analysis (FR-033, 30-day retention)
- Intent classifier uses fine-tuned model or prompt engineering

### Best Practices
- Never provide complete code solutions for exercises (FR-028)
- Always ask clarifying questions before answering (Socratic method)
- Adapt response depth to demonstrated understanding level (FR-029)
- Guide debugging using reproduce → isolate → hypothesize → test → fix (FR-030)

---

## 4. Database Design Strategy

### Decision
**Neon PostgreSQL** with SQLAlchemy/SQLModel ORM and Alembic migrations.

### Rationale
- Neon provides serverless PostgreSQL with auto-scaling
- Connection pooling handles 10k concurrent users
- Read replicas available for analytics queries
- SQLModel combines Pydantic validation with SQLAlchemy ORM

### Schema Design Principles
- UUID primary keys for all entities
- Soft delete pattern (deleted_at timestamp) for 30-day recovery (FR-090)
- Audit columns (created_at, updated_at, created_by) on all tables
- JSONB for flexible metadata fields (user preferences, personalization)
- Separate analytics tables for read-heavy queries

### Alternatives Considered
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Supabase | Built-in auth, real-time | Coupled architecture | Better-Auth already chosen, separation preferred |
| PlanetScale | MySQL, excellent scaling | MySQL, not PostgreSQL | Team expertise in PostgreSQL |
| CockroachDB | Distributed, resilient | Complexity, cost | Overkill for initial scale |

---

## 5. Streaming Response Architecture

### Decision
**Server-Sent Events (SSE)** for AI response streaming with WebSocket fallback.

### Rationale
- SSE is simpler than WebSocket for unidirectional streaming (AI → client)
- Native browser support without additional libraries
- Automatic reconnection built-in
- WebSocket fallback for environments with SSE issues

### Implementation Pattern
```
Client → POST /api/ai/chat → 202 Accepted + stream_id
Client → GET /api/ai/stream/{stream_id} → SSE stream
  └── Event: {"type": "chunk", "content": "..."}
  └── Event: {"type": "citation", "ref": "ch3:s2:p5"}
  └── Event: {"type": "done", "usage": {...}}
```

### Performance Targets
- First chunk within 1 second (SC-017)
- Complete response within 5 seconds p95 (SC-009)
- Graceful timeout at 30 seconds

### Best Practices
- Send heartbeat every 15 seconds to prevent connection timeout
- Include token usage in final event for quota tracking
- Client-side exponential backoff on reconnection

---

## 6. Simulation Integration

### Decision
**Cloud-first approach** with Gazebo Harmonic and optional NVIDIA Isaac Sim.

### Rationale
- Most learners lack local GPU hardware
- Cloud simulation removes hardware barrier (Constitution: "No learner blocked by hardware")
- Gazebo Harmonic is the default; Isaac Sim for advanced perception exercises
- 25 hours/month default quota balances access with cost

### Integration Architecture
```
Frontend → Backend API → Simulation Service →
  ├── Cloud GPU Pool (AWS/GCP) → Gazebo/Isaac container
  └── State Manager → Save/restore simulation states (FR-022)
```

### Quota Management
- Track usage per user (billing_period, hours_used)
- Notify at 80% and 95% quota
- Institution custom quotas via admin API
- Graceful degradation: disable sim features, show cached content (FR-103)

### Deferred: Isaac Sim Deep Integration
- Phase 1: Gazebo integration only
- Phase 3+: Isaac Sim for perception exercises
- Rationale: Reduce initial complexity; Gazebo covers 80% of curriculum

---

## 7. Content Management

### Decision
**Hybrid approach**: Docusaurus MDX for authored content, PostgreSQL for metadata/versions.

### Rationale
- MDX provides excellent authoring experience for technical content
- Code blocks, interactive components native to MDX
- Git-based versioning for content files
- PostgreSQL tracks versions, review status, stage mapping

### Content Pipeline
```
Author creates MDX → Git commit → CI triggers →
  ├── MDX validation/build
  ├── Content indexing (Qdrant) → embedding generation
  └── Metadata sync to PostgreSQL
```

### Versioning Strategy
- Semantic versioning for content modules
- Breaking changes (curriculum structure) require migration guides
- Students notified of updates in active stages (FR-009)

### Best Practices
- Separate content repo or monorepo subdirectory
- Automated accessibility checks on PR
- Link checker for external references

---

## 8. Frontend State Management

### Decision
**Zustand** for client state, **TanStack Query** for server state.

### Rationale
- Zustand is lightweight, simple API, TypeScript-first
- TanStack Query handles caching, refetching, optimistic updates
- Clear separation: Zustand for UI state, TanStack for API data

### Store Structure
```typescript
// userStore - auth state, preferences
// learningStore - current stage, progress, bookmarks
// chatStore - AI conversation state, streaming buffer
```

### Alternatives Considered
| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Redux Toolkit | Powerful, ecosystem | Boilerplate, complexity | Overkill for this app |
| Jotai | Atomic, simple | Less structured | Zustand has better patterns for our needs |
| Context API | Built-in | Re-render issues, no devtools | Performance concerns |

---

## 9. Assessment Engine

### Decision
**Hybrid assessment** with automated objective grading and human review queue.

### Rationale
- Objective criteria (code execution, simulation performance) can be automated (FR-047)
- Subjective elements (explanations, project quality) require human review
- Understanding Verification Framework (FR-046) requires human evaluation

### Assessment Pipeline
```
Submission → Automated Checks →
  ├── Code execution → test results
  ├── Similarity analysis → plagiarism flag (FR-050)
  ├── Rubric auto-scoring (objective criteria)
  └── Human review queue (subjective criteria) → Instructor dashboard
```

### Automated Capabilities
- Code compilation/execution in sandbox
- Unit test execution for code submissions
- Simulation metric collection (completion time, collision count)
- Similarity detection against corpus + peer submissions

### Human Review Required For
- Explain-without-code verification method
- Teaching-back evaluation
- Complex project rubrics
- Flagged similarity cases

---

## 10. Deployment Strategy

### Decision
**Vercel (frontend) + Fly.io (backend) + Neon (database)** with GitHub Actions CI/CD.

### Rationale
- Vercel optimized for Next.js, edge functions for SSR
- Fly.io supports FastAPI with auto-scaling, global distribution
- Neon serverless PostgreSQL scales with demand
- GitHub Actions for unified CI/CD pipeline

### Environment Strategy
```
main branch → Production
staging branch → Staging
feature/* → Preview deployments (Vercel)
```

### Deployment Pipeline
```yaml
Push → Lint/Type-check → Unit Tests → Build →
  ├── (staging) → Deploy staging → Integration tests → Approval gate
  └── (production) → Deploy production → Smoke tests → Monitor
```

### Infrastructure as Code
- Docker Compose for local development
- Terraform/Pulumi for cloud infrastructure (future)
- Secrets in environment variables, never committed

---

## 11. Localization Strategy

### Decision
**AI-generated translation** (Urdu primary) with caching and quality caveats.

### Rationale
- FR-084 requires Urdu translation on-demand
- AI translation is cost-effective for initial launch
- Quality disclaimer required (Assumption #11 in spec)
- Cache translated content to reduce API costs

### Implementation
```
Content request + locale=ur → Cache check →
  ├── Cache hit → Return cached translation
  └── Cache miss → AI translate → Cache (24h TTL) → Return
```

### Quality Measures
- Display "AI-translated" indicator
- Allow users to report translation issues
- Priority queue for flagged content for human review (future)

### Performance Target
- Translation within 5 seconds (SC-018)
- Cache warm-up for high-traffic content

---

## 12. Security Considerations

### Decision
**Defense in depth** with OWASP top 10 mitigations.

### Key Security Measures
| Threat | Mitigation |
|--------|------------|
| SQL Injection | Parameterized queries (SQLAlchemy ORM) |
| XSS | Content Security Policy, React auto-escaping |
| CSRF | SameSite cookies, CSRF tokens |
| Auth bypass | Better-Auth session management, role checks |
| Data exposure | Field-level access control, audit logging |
| Rate abuse | 60 req/min limit, DDoS protection (CDN) |
| Secrets exposure | Environment variables, no hardcoded credentials |

### Compliance
- GDPR: Data deletion rights, consent management
- Accessibility: WCAG 2.1 AA compliance target

---

## Summary: Key Decisions

| Area | Decision | Confidence |
|------|----------|------------|
| Auth | Better-Auth | High |
| Vector DB | Qdrant | High |
| RAG Orchestration | LangGraph + LlamaIndex | High |
| Database | Neon PostgreSQL | High |
| Frontend State | Zustand + TanStack Query | High |
| Streaming | SSE with WebSocket fallback | High |
| Simulation | Cloud-first, Gazebo primary | Medium (defer Isaac Sim) |
| Content | Docusaurus MDX + PostgreSQL metadata | High |
| Deployment | Vercel + Fly.io + Neon | High |
| Translation | AI-generated with caching | Medium (quality TBD) |

---

*Research completed: 2026-02-07*
