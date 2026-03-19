# Implementation Plan: Docusaurus Authentication Migration & Onboarding

**Branch**: `002-docusaurus-auth-migration` | **Date**: 2026-02-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-docusaurus-auth-migration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Migrate authentication from Next.js to Docusaurus using Better Auth, implement a 4-step onboarding flow, fix Docusaurus routing issues, and simplify the Next.js frontend to a pure marketing site. This consolidates authentication in a single location (Docusaurus), reduces code duplication, and provides a clean separation between marketing (Next.js) and learning platform (Docusaurus).

**Key Changes**:
- Move Better Auth client integration from Next.js to Docusaurus
- Implement 4-step onboarding flow (Basic Info → Education → Interests → Additional)
- Add onboarding columns to users table (email_verified, onboarding_completed, current_stage, role, preferences)
- Configure Docusaurus routing (baseUrl='/AINativeBook/', routeBasePath='/')
- Remove all authentication code from Next.js
- Implement protected routes in Docusaurus with onboarding checks

## Technical Context

**Language/Version**: TypeScript 5.x (Docusaurus, Auth Server), Python 3.11+ (Backend migrations)
**Primary Dependencies**:
- Docusaurus 3.x (static site generator with React)
- Better Auth (authentication library with OIDC support)
- React 18+ (UI framework)
- PostgreSQL 16+ (database)
- Alembic (database migrations)

**Storage**: PostgreSQL with JSONB for onboarding preferences
**Testing**: Manual testing for auth flows, integration tests for API endpoints
**Target Platform**: Web (Chrome, Firefox, Safari, Edge - latest 2 versions)
**Project Type**: Web application (frontend + auth server + backend)
**Performance Goals**:
- Authentication flow completion < 30 seconds
- Onboarding completion < 3 minutes
- Session validation < 100ms
- Page load time < 2 seconds

**Constraints**:
- Static site deployment (GitHub Pages) - no server-side auth checks
- Same-domain deployment (simplifies cookie sharing)
- Client-side route protection only
- No auto-save within onboarding steps (save on step completion)

**Scale/Scope**:
- ~1000 concurrent users expected
- 4 onboarding pages + 2 auth pages
- 6 API endpoints for onboarding
- ~15 existing Better Auth endpoints
- Affects 3 services: Docusaurus, Auth Server, Next.js

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: ⚠️ Constitution file is template only - using general best practices

**Applied Principles**:
1. **Separation of Concerns**: Authentication consolidated in Docusaurus, marketing in Next.js
2. **Data Integrity**: Database migration with idempotent checks, JSONB validation
3. **Security First**: HttpOnly cookies, CSRF protection, password hashing, rate limiting
4. **User Experience**: Clear step indicators, validation feedback, session persistence
5. **Maintainability**: Remove duplicate auth code, single source of truth

**Potential Violations**: None identified

**Re-check After Phase 1**: ✅ Design maintains separation of concerns, no unnecessary complexity

## Project Structure

### Documentation (this feature)

```text
specs/002-docusaurus-auth-migration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command) ✅
├── data-model.md        # Phase 1 output (/sp.plan command) ✅
├── quickstart.md        # Phase 1 output (/sp.plan command) ✅
├── contracts/           # Phase 1 output (/sp.plan command) ✅
│   └── api-contracts.md # API endpoint definitions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
intellistack/
├── auth-server/                    # Better Auth OIDC server (TypeScript)
│   ├── src/
│   │   ├── auth.ts                # Better Auth configuration
│   │   ├── routes/
│   │   │   └── onboarding.ts      # NEW: Onboarding endpoints
│   │   └── index.ts               # Express server entry
│   └── package.json
│
├── content/                        # Docusaurus application
│   ├── src/
│   │   ├── lib/
│   │   │   └── auth.ts            # NEW: Better Auth client
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx    # NEW: Auth state management
│   │   ├── components/
│   │   │   ├── AuthNavbarItem.tsx # NEW: Login/Signup/User menu
│   │   │   └── ProtectedRoute.tsx # NEW: Route protection
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── login.tsx      # NEW: Login page
│   │   │   │   ├── signup.tsx     # NEW: Signup page
│   │   │   │   └── callback.tsx   # NEW: OAuth callback
│   │   │   └── onboarding/
│   │   │       ├── step-1.tsx     # NEW: Basic info
│   │   │       ├── step-2.tsx     # NEW: Education
│   │   │       ├── step-3.tsx     # NEW: Interests
│   │   │       └── step-4.tsx     # NEW: Additional
│   │   ├── theme/
│   │   │   ├── Root.tsx           # NEW: AuthProvider wrapper
│   │   │   ├── DocPage/
│   │   │   │   └── Layout/        # MODIFIED: Add ProtectedRoute
│   │   │   └── NavbarItem/
│   │   │       └── ComponentTypes.tsx # MODIFIED: Register AuthNavbarItem
│   │   └── clientModules/
│   │       └── authInit.ts        # NEW: Auth initialization
│   ├── docusaurus.config.ts       # MODIFIED: Add customFields, clientModules
│   └── package.json
│
├── frontend/                       # Next.js marketing site
│   ├── src/
│   │   ├── components/
│   │   │   └── layout/
│   │   │       └── Header.tsx     # MODIFIED: Simplified nav, external links
│   │   ├── lib/
│   │   │   └── auth.ts            # DELETED: Remove auth client
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx    # DELETED: Remove auth context
│   │   ├── components/
│   │   │   ├── UserMenu.tsx       # DELETED: Remove user menu
│   │   │   └── ProtectedRoute.tsx # DELETED: Remove route protection
│   │   ├── app/
│   │   │   └── auth/              # DELETED: Remove auth pages
│   │   └── middleware.ts          # DELETED: Remove auth middleware
│   └── package.json
│
└── backend/                        # FastAPI backend
    ├── alembic/
    │   └── versions/
    │       └── 20260225_add_onboarding_columns.py # NEW: Database migration
    └── src/
        └── core/
            └── auth/
                └── models.py       # MODIFIED: Already has required columns
```

**Structure Decision**: Web application structure with separate frontend (Next.js), content platform (Docusaurus), auth server (Better Auth), and backend API (FastAPI). Authentication logic moves from Next.js to Docusaurus, with Next.js becoming a pure marketing site.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations identified. All complexity is justified by requirements:
- Multiple services (Next.js, Docusaurus, Auth Server) required for separation of concerns
- JSONB storage for onboarding data provides flexibility without schema changes
- Client-side route protection necessary due to static site deployment model
