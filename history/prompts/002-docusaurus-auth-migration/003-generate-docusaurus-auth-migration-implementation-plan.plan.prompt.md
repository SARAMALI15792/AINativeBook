---
id: 003
title: Generate Docusaurus Auth Migration Implementation Plan
stage: plan
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: 002-docusaurus-auth-migration
branch: 002-docusaurus-auth-migration
user: saram
command: /sp.plan
labels: ["planning", "architecture", "authentication", "docusaurus", "onboarding"]
links:
  spec: specs/002-docusaurus-auth-migration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-docusaurus-auth-migration/plan.md
  - specs/002-docusaurus-auth-migration/research.md
  - specs/002-docusaurus-auth-migration/data-model.md
  - specs/002-docusaurus-auth-migration/quickstart.md
  - specs/002-docusaurus-auth-migration/contracts/api-contracts.md
tests:
  - Planning artifacts validated against specification requirements
---

## Prompt

/sp.plan

(No additional user input - standard planning workflow)

## Response snapshot

Executed complete planning workflow for Docusaurus Authentication Migration feature, generating all Phase 0 and Phase 1 artifacts.

**Phase 0: Research (Complete)**

Generated comprehensive research document covering 10 technical decisions:

1. **Better Auth Client Integration**: Lazy singleton pattern with Proxy for SSR/SSG compatibility
2. **Custom Pages for Auth**: Docusaurus `src/pages/` directory with BrowserOnly wrapper
3. **Custom Navbar Components**: Swizzle NavbarItem/ComponentTypes with AuthContext provider
4. **Protected Routes**: Client-side route guards with useEffect-based redirects
5. **Session Cookie Configuration**: SameSite=Lax for same-domain deployment
6. **Docusaurus Routing**: baseUrl='/AINativeBook/', routeBasePath='/', trailingSlash=false
7. **Next.js Simplification**: Remove all auth code, convert to pure marketing site
8. **Onboarding Data Storage**: JSONB field with structured schema
9. **Database Migration**: Alembic migration with idempotent column additions
10. **Environment Variables**: Separate .env files per service with clear prefixes

All research decisions include rationale, implementation patterns, alternatives considered, and references.

**Phase 1: Design (Complete)**

Generated four comprehensive design documents:

1. **Data Model (data-model.md)**:
   - 4 entities: User, Session, OAuth Account, Onboarding Data
   - Complete schema with columns, types, constraints, indexes
   - Entity relationships and state transitions
   - Database migration strategy with Alembic
   - Common query patterns and access patterns
   - JSONB schema for onboarding preferences

2. **API Contracts (contracts/api-contracts.md)**:
   - 16 endpoint definitions with request/response schemas
   - Authentication endpoints (signup, signin, signout, OAuth, JWT)
   - Onboarding endpoints (status, save step, complete)
   - User profile endpoints (get, update)
   - Session management endpoints (list, revoke)
   - OIDC discovery endpoints (openid-configuration, JWKS)
   - Error response format and common error codes
   - Authentication flows (email/password, OAuth, session validation)
   - Rate limiting and CORS configuration

3. **Quickstart Guide (quickstart.md)**:
   - 9 implementation phases with step-by-step instructions
   - Database migration (30 min)
   - Better Auth server configuration (1 hour)
   - Docusaurus configuration (2 hours)
   - Authentication pages (2 hours)
   - Onboarding pages (3 hours)
   - Protected routes (1 hour)
   - Custom navbar (1 hour)
   - Next.js simplification (1 hour)
   - Testing (2 hours)
   - Complete code examples for each component
   - Test checklist with 25+ test cases
   - Troubleshooting guide
   - Deployment checklist

4. **Implementation Plan (plan.md)**:
   - Technical context and constraints
   - Constitution check (no violations)
   - Complete project structure with file paths
   - Complexity tracking (justified)
   - Summary of key changes

**Key Architectural Decisions**:

- **Authentication Consolidation**: Single source of truth in Docusaurus (not Next.js)
- **Client-Side Protection**: Static site deployment requires client-side route guards
- **Same-Domain Deployment**: Simplifies cookie sharing (no cross-domain issues)
- **JSONB Storage**: Flexible onboarding data schema without migrations
- **Mandatory Onboarding**: No skip option, all 4 steps required
- **Save on Step Completion**: No auto-save within steps (clarified in spec)
- **Session Management**: 24-hour expiration, 1-hour refresh, database-backed

**Project Structure**:

- **Auth Server**: Add onboarding endpoints to existing Better Auth server
- **Docusaurus**: Add auth client, context, pages, components, protected routes
- **Next.js**: Remove all auth code, simplify to marketing site
- **Backend**: Add database migration for onboarding columns

**Estimated Implementation Time**: 8-12 hours total

## Outcome

- ✅ Impact: Complete implementation plan generated with research, data model, API contracts, and quickstart guide. Provides clear roadmap for 8-12 hour implementation across 4 services (Auth Server, Docusaurus, Next.js, Backend).
- 🧪 Tests: Test checklist with 25+ test cases covering authentication, onboarding, protected routes, routing, and session management.
- 📁 Files: Created 5 planning artifacts (plan.md, research.md, data-model.md, quickstart.md, api-contracts.md) totaling ~2500 lines of documentation
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable task breakdown with dependencies and acceptance criteria
- 🧠 Reflection: Planning successfully translated clarified requirements into concrete implementation architecture. All technical decisions documented with rationale and alternatives. Quickstart guide provides step-by-step implementation path. Ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None. All planning phases completed successfully.
- Graders run and results (PASS/FAIL): Architecture validation - PASS (no constitution violations, justified complexity, clear separation of concerns)
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 research and Phase 1 design
- Next experiment (smallest change to try): Proceed to task generation to validate that planning artifacts provide sufficient detail for implementation breakdown
