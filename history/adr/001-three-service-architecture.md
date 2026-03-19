# ADR-001: Three-Service Architecture (Auth Node.js + FastAPI + Next.js)

**Date**: 2026-02-11
**Status**: Accepted
**Initiated By**: Feature 002-better-auth-chatkit

---

## Context

IntelliStack Platform requires a modern authentication system (Better-Auth OIDC) that is fundamentally a Node.js library, while the existing backend is built in Python (FastAPI) and the frontend in TypeScript/Next.js. A decision was needed on how to structure these three technology stacks within a unified platform.

**Constraints**:
- Better-Auth is a Node.js-only library; cannot run natively in Python
- FastAPI is the existing backend framework; significant rewrite cost to change
- Next.js is the existing frontend framework; stable and performant for this use case
- Platform requires OIDC discovery endpoint (`/.well-known/openid-configuration`) for token distribution to multiple downstream services
- Platform requires JWT token validation without per-request coupling to the auth service

**Drivers**:
- Need for standards-compliant authentication (OIDC, JWKS, PKCE)
- Multi-service token sharing (auth server issues tokens, FastAPI validates them independently)
- Independent deployability and scalability of services
- Clear separation of concerns (auth, API, frontend)

---

## Decision

**Adopt a three-service microservices architecture**:

1. **Auth Server** (Node.js/Express): Standalone Better-Auth OIDC server
   - Runs on port 3001 (containerized)
   - Issues RS256-signed JWT tokens
   - Exposes `/.well-known/openid-configuration` for OIDC discovery
   - Exposes `/.well-known/jwks.json` for public key distribution
   - Manages user accounts, sessions, OAuth providers, email verification

2. **FastAPI Backend** (Python): Resource server + AI tutor
   - Runs on port 8000 (containerized)
   - Validates Better-Auth JWTs using JWKS public keys (not direct auth server calls)
   - Implements ChatKit AI tutor with Socratic teaching
   - Manages learning content, progress, RAG, ChatKit persistence

3. **Next.js Frontend** (TypeScript): Client application
   - Runs on port 3000 (containerized)
   - Uses Better-Auth React client for session management
   - Communicates with FastAPI backend and auth server
   - Renders lesson pages, AI tutor widget, user dashboard

**Orchestration**: All three services run in Docker Compose with shared PostgreSQL (Neon) database.

---

## Consequences

### ✅ Advantages

1. **Standards Compliance**: Better-Auth provides production-grade OIDC discovery and JWKS endpoints without custom implementation
2. **Independent Token Validation**: FastAPI validates tokens via cached JWKS (5-min TTL), not per-request auth server calls → lower latency, higher resilience
3. **Service Independence**: Each service can be deployed, scaled, and upgraded independently
4. **Clear Separation**: Auth concerns isolated in dedicated service; no auth logic mixed into FastAPI or frontend
5. **Multi-Service Auth**: JWKS endpoint allows future services (mobile app, CLI, webhooks) to validate same tokens
6. **Technology Fit**: Uses each language/framework's native ecosystem (Node.js for auth, Python for ML/AI, TypeScript for frontend)

### ⚠️ Tradeoffs

1. **Operational Complexity**: Three containers, three deployment pipelines, shared database → requires orchestration (Docker Compose, Kubernetes)
2. **Cross-Service Debugging**: Issues may span multiple services; requires distributed logging and tracing
3. **Network Latency**: Initial JWKS fetch adds ~50-200ms to auth flow (mitigated by 5-min cache)
4. **Data Consistency**: All three services share single PostgreSQL database → potential bottleneck at scale
5. **Deployment Coordination**: Auth server must be up before FastAPI and frontend can function; migration is critical path

### 🚨 Risks

1. **Auth Server Downtime**: If auth server down for extended time, cannot issue new tokens or verify email. Mitigation: JWKS caching allows existing users to continue; already-authenticated users with valid tokens unaffected
2. **JWKS Fetch Failures**: If FastAPI cannot reach auth server JWKS endpoint, falls back to cached keys (5-min TTL). If no cache and unreachable: return 503. Mitigation: robust fallback strategy, monitoring
3. **Database Single Point of Failure**: All three services depend on shared PostgreSQL. Mitigation: use managed PostgreSQL (Neon) with backups; monitor database health
4. **Scale Bottleneck**: At 500+ concurrent users, shared database becomes constraint. Mitigation: caching layer (Redis), database replicas, sharding strategy (future)

---

## Alternatives Considered

### Alternative 1: Monolith (Auth + API + Frontend in Single Process)

**Approach**: Integrate Better-Auth into Next.js API routes; FastAPI becomes backend-only; all session handling in Next.js.

**Rationale for rejection**:
- Better-Auth cannot run in FastAPI (Python issue)
- Mixing auth into Next.js complicates deployment and scaling
- Cannot expose OIDC provider to multiple services
- Tightly couples frontend and API lifecycles
- Not future-proof for mobile or third-party integrations

**Score**: ❌ Rejected — architectural mismatch

---

### Alternative 2: Separate Auth Database

**Approach**: Auth server has its own PostgreSQL instance; FastAPI has separate database; sync via API/webhooks.

**Rationale for rejection**:
- Adds operational complexity (two databases, sync strategy)
- User and learning data live in FastAPI database; auth data in separate auth DB → inconsistency risk
- OAuth links, user roles, email verification split across databases
- Increases deployment and maintenance burden
- No clear benefit for current scale (500 concurrent users)

**Score**: ❌ Rejected — complexity without benefit

---

### Alternative 3: Keep Custom Python Auth

**Approach**: Build Better-Auth equivalent in Python; run auth in FastAPI; skip Node.js entirely.

**Rationale for rejection**:
- Better-Auth is production-grade, actively maintained; rebuilding wastes engineering effort
- Better-Auth's OIDC Provider and JWKS plugins are mature; Python equivalent would take months
- Better-Auth ecosystem (email templates, OAuth providers, admin plugin) well-tested
- Locks platform into Python; limits future technology flexibility
- No strategic advantage; adds technical debt

**Score**: ❌ Rejected — not invented here fallacy

---

### Alternative 4: Auth0 / Keycloak (Third-Party)

**Approach**: Use managed auth service (Auth0) or self-hosted identity provider (Keycloak); no custom auth server.

**Rationale for rejection**:
- Auth0 adds monthly cost and external dependency (vendor lock-in)
- Keycloak adds operational complexity (separate Java service, separate database, steep learning curve)
- Better-Auth provides 95% of needed functionality at lower cost and complexity
- Learning platform wants to own auth logic and branding; third-party services add abstraction layer
- Data residency and privacy concerns (especially for educational content)

**Score**: ⚠️ Defer — valid for enterprise, but over-engineered for current stage

---

## Compatibility & Dependencies

- **Better-Auth**: Node.js 18+, PostgreSQL adapter via Drizzle
- **FastAPI**: Python 3.11+, PyJWT + jwcrypto for RS256 validation, access to BETTER_AUTH_JWKS_URL environment variable
- **Next.js**: TypeScript 5.3+, @better-auth/react client library
- **PostgreSQL**: Single instance (Neon) shared by all three services; migrations managed by Better-Auth CLI + Alembic
- **Docker**: Compose orchestration with health checks, environment variable injection

---

## Implementation Notes

1. **Phase 1**: Auth server scaffolding (Node.js, Express, Better-Auth setup)
2. **Phase 2**: FastAPI JWKS integration (replace old cookie auth with JWT validation)
3. **Phase 3+**: Auth flows (email/password, OAuth, password reset, roles)
4. **Phase 7**: Data migration (cutover from old auth tables to Better-Auth schema)

**Critical Path**: Auth server must be operational before FastAPI can validate tokens. Frontend can cache session and continue even if auth server is temporarily down (using cached JWKS).

---

## Related ADRs

- ADR-002: Better-Auth as Standalone OIDC Server (complements this decision)
- ADR-003: JWKS-Based JWT Validation in FastAPI (addresses token validation strategy)

---

## References

- `specs/002-better-auth-chatkit/plan.md` § Project Structure, Phase Dependencies
- `specs/002-better-auth-chatkit/research.md` § R-001, R-003
- `specs/002-better-auth-chatkit/data-model.md` § Entity Relationship Overview
- Better-Auth Documentation: https://better-auth.com
- Docker Compose: https://docs.docker.com/compose/

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-02-11 | SDD Agent | Initial decision record |
