# IntelliStack Codebase Flow Auditor Memory

## Last Audit: 2026-02-19 (branch: 001-frontend-redesign)

## Key Architecture Facts
- Backend: FastAPI (Python) at :8000 with async SQLAlchemy 2.0
- Auth: Better-Auth (TypeScript/Express) at :3001, uses EdDSA (Ed25519) JWT signing
- Content Site: Docusaurus at :3002
- New Frontend: Next.js at :3000
- Database: PostgreSQL (Neon) with Alembic migrations
- Vector: Qdrant; Cache: Redis; AI: OpenAI + Cohere

## Critical Patterns Found
1. Auth flow uses opaque session tokens (cookies), NOT JWTs for browser clients
2. JWKS middleware always falls back to session validation for browser requests
3. Two user provisioning paths: `sync_user_from_jwt` (middleware) and `get_or_create_user` (routes)
4. 7 of 14+ routers registered in main.py -- personalization, translation, code execution, enhanced content, tutor, assessment, community NOT registered
5. Personalization models use old Column() style; rest of codebase uses mapped_column()
6. `Content` model (content/models.py) vs `ContentItem` model (learning/models.py) -- two separate content abstractions exist

## Common Bug Patterns
- Type annotations say `User` (ORM) but receive `AuthenticatedUser` (dataclass) from auth deps
- UUID type mismatches: some models use UUID(as_uuid=True), others UUID(as_uuid=False), others String(255)
- Missing imports caught at runtime (func.now, BetterAuthSessionMiddleware)
- Python operator precedence: `x == y or "default"` evaluates wrong

## File Quick Reference
- Entry: `intellistack/backend/src/main.py`
- Auth deps: `intellistack/backend/src/core/auth/dependencies.py`
- Middleware: `intellistack/backend/src/shared/middleware.py`
- Settings: `intellistack/backend/src/config/settings.py`
- Auth server: `intellistack/auth-server/src/auth.ts` + `index.ts`
- Content auth: `intellistack/content/src/lib/auth-client.ts`
- Frontend auth: `intellistack/frontend/src/lib/auth.ts`
