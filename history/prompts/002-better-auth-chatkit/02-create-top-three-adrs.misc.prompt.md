---
id: 02
title: Create top three architecture decision records
stage: misc
date: 2026-02-11
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-better-auth-chatkit
branch: 002-better-auth-chatkit
user: user
command: /sp.adr (x3)
labels: ["adr", "architecture", "better-auth", "jwt", "microservices"]
links:
  spec: specs/002-better-auth-chatkit/spec.md
  ticket: null
  adr: history/adr/001-three-service-architecture.md, history/adr/002-better-auth-as-oidc-server.md, history/adr/003-jwks-jwt-validation-strategy.md
  pr: null
files:
  - history/adr/001-three-service-architecture.md
  - history/adr/002-better-auth-as-oidc-server.md
  - history/adr/003-jwks-jwt-validation-strategy.md
tests: []
---

## Prompt

Create Architecture Decision Records for the top 3 significant architectural decisions before implementation:
1. Three-Service Architecture (Auth Node.js + FastAPI + Next.js Frontend)
2. Better-Auth as Standalone OIDC Server
3. JWKS-Based JWT Validation in FastAPI Resource Server

## Response snapshot

Created 3 comprehensive ADRs documenting major architectural decisions from the plan.md. Each ADR includes:

**ADR-001: Three-Service Architecture**
- Context: Technology mismatch (Node.js auth, Python backend, TypeScript frontend)
- Decision: Three containerized services (auth-server:3001, backend:8000, frontend:3000)
- Consequences: Standards compliance, independent scaling, operational complexity
- Alternatives considered & rejected: Monolith, separate auth DB, custom Python auth, Auth0/Keycloak
- Related ADRs: ADR-002, ADR-003
- Risk mitigation: JWKS caching, health checks, Docker Compose orchestration

**ADR-002: Better-Auth as Standalone OIDC Server**
- Context: Need for standards-compliant auth (OIDC, JWKS, PKCE, OAuth 2.1)
- Decision: Better-Auth Node.js with JWT, OIDC Provider, Admin plugins
- Features: Email/password, OAuth (Google/GitHub), PKCE, email verification, password reset, lockout, RS256 signing
- Consequences: Production-grade, standards-compliant, feature-complete (no custom code)
- Alternatives considered & rejected: Custom Python JWT, Keycloak, Auth0, OAuth 2.0 without OIDC
- Data migration path: Old tables → Better-Auth schema (big-bang cutover)

**ADR-003: JWKS-Based JWT Validation in FastAPI**
- Context: FastAPI must validate tokens without per-request auth server calls
- Decision: JWKS caching (5-min TTL) with fallback to last-known-good keys
- Strategy: PyJWT RS256 verification, role extraction, email verification checks
- Consequences: Standards-compliant, low latency (cached), resilient to auth server downtime
- Alternatives considered & rejected: Per-request verification (latency), HS256 (security), sessions (stateful), API keys (wrong pattern)
- Risk mitigation: Cache fallback, monitoring, token rotation, revocation strategy

All ADRs include:
✅ Clustering of related decisions (not atomic choices)
✅ At least one alternative with rationale
✅ Clear pros/cons for chosen approach
✅ Risk analysis and mitigation strategies
✅ Implementation roadmap and testing strategy
✅ References to plan.md, research.md, data-model.md

## Outcome

- ✅ Impact: 3 foundational architecture decisions formally documented before implementation begins. Team has clear record of *why* decisions were made, alternatives considered, and long-term consequences. Provides reference for future architectural questions.
- 🧪 Tests: No tests generated (ADRs are design artifacts, not code). Each ADR includes testing strategy section for implementation phase.
- 📁 Files: Created `history/adr/001-*.md`, `history/adr/002-*.md`, `history/adr/003-*.md` (1000+ lines total)
- 🔁 Next prompts: `/sp.implement` to begin Phase 1 (setup); `/sp.git.commit_pr` to create PR with ADRs + tasks.md; `/sp.clarify` if any decisions need refinement
- 🧠 Reflection: ADRs correctly identify the three highest-impact decisions affecting multiple services and long-term platform structure. ADR-003 (JWKS strategy) is technically deepest; includes fallback resilience strategy critical for production. All ADRs reference task breakdown (tasks.md) for implementation sequencing. Team can now proceed to implementation with clear architectural guidance.

## Evaluation notes (flywheel)

- Failure modes observed: None — all three ADRs passed significance test (impact on engineering, multiple alternatives, long-term consequences). Each decision clusters related choices rather than atomic ones.
- Graders run and results (PASS/FAIL): PASS
  - ADR-001: Clusters three services as integrated decision ✅ | Alternatives: monolith, separate auth DB, Keycloak ✅ | Consequences: operational complexity, scalability, resilience ✅
  - ADR-002: Clusters Better-Auth plugins as integrated solution ✅ | Alternatives: custom auth, Keycloak, Auth0 ✅ | Consequences: standards compliance, maintenance, data migration ✅
  - ADR-003: Clusters JWKS + caching + fallback strategy ✅ | Alternatives: per-request validation, HS256, sessions ✅ | Consequences: latency, resilience, security ✅
- Prompt variant (if applicable): None — single execution created all three ADRs
- Next experiment (smallest change to try): If user requests, could create detailed implementation checklist per ADR or link ADRs to specific tasks.md phases for traceability

## Follow-up recommendations

1. **Pre-Implementation Review**: Schedule 30-min team sync to review ADRs-001-003; confirm alignment on architectural approach
2. **Risk Mitigation**: Create monitoring/alerting tasks for JWKS failures, auth server downtime, data migration validation
3. **Knowledge Sharing**: Add ADRs to platform architecture documentation (for onboarding new team members)
4. **ADR Linking**: Cross-reference tasks.md tasks to relevant ADR sections (traceability)
5. **Post-Implementation**: ADRs should be updated if architectural decisions change during implementation (mark as "Superseded" if revised)
