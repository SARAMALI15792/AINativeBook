# Scenario: Full NestJS Port

**Source:** IntelliStack FastAPI + Better-Auth + SQLAlchemy
**Target:** NestJS (TypeScript) + Passport JWT + TypeORM / Prisma

---

## Prompt to Use

```
Convert IntelliStack to NestJS. I want the full backend and auth layer.
Target: NestJS with Passport JWT for auth and Prisma for the database.
```

## What the Agent Produces

### 1. Auth Module
- `src/auth/auth.module.ts` — imports PassportModule, JwtModule
- `src/auth/auth.service.ts` — register, login, OAuth callback logic
- `src/auth/jwt.strategy.ts` — validates RS256 JWT from Better-Auth JWKS
- `src/auth/guards/jwt-auth.guard.ts` — drops in place of FastAPI `Depends(get_current_user)`

### 2. Users Module
- `src/users/users.module.ts`
- `src/users/users.service.ts` — profile CRUD, role management
- `src/users/dto/update-profile.dto.ts` — Zod or class-validator equivalent of Pydantic schema

### 3. Learning Module
- `src/learning/learning.module.ts`
- `src/learning/learning.service.ts` — stage unlock logic, progress tracking
- `src/learning/entities/stage.entity.ts`, `lesson.entity.ts`, etc.

### 4. Database (Prisma)
The agent generates `prisma/schema.prisma` from all SQLAlchemy models.

```bash
npx prisma migrate dev --name init
npx prisma generate
```

## Key Differences to Note

| IntelliStack (FastAPI)         | NestJS Equivalent                    |
|-------------------------------|--------------------------------------|
| `Depends(get_current_user)`   | `@UseGuards(JwtAuthGuard)`           |
| Pydantic `BaseModel`          | class-validator DTO                  |
| SQLAlchemy async session      | Prisma `PrismaService`               |
| `HTTPException(status_code=)` | `throw new HttpException(...)`       |
| SSE via `StreamingResponse`   | `@Sse()` decorator + `Observable`    |
| Alembic migrations            | `prisma migrate dev`                 |

## Required Dependencies

```bash
npm install @nestjs/passport passport passport-jwt @nestjs/jwt
npm install @prisma/client prisma
npm install class-validator class-transformer
npm install @nestjs/config
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:5432/intellistack
JWT_SECRET=<same-as-BETTER_AUTH_SECRET>
JWKS_URI=https://your-auth-server/.well-known/jwks.json
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
```
