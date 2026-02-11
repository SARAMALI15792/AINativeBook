# Research: Better-Auth OIDC Server + ChatKit AI Tutor

**Feature Branch**: `002-better-auth-chatkit`
**Date**: 2026-02-11
**Status**: Complete

## R-001: Better-Auth as OIDC Provider

### Decision
Use Better-Auth with the **OIDC Provider plugin** + **JWT plugin** running as a standalone Node.js/Express server in Docker, issuing RS256-signed JWTs with JWKS endpoint.

### Rationale
- Better-Auth has a native OIDC Provider plugin that exposes `/.well-known/openid-configuration`, `/oauth2/authorize`, `/oauth2/token`, and JWKS endpoints.
- The JWT plugin enables asymmetric RS256 signing with auto-generated key pairs and a `/.well-known/jwks.json` endpoint.
- The Admin plugin provides role management (create/assign roles with permission claims in JWT).
- PostgreSQL adapter (`drizzle` or `kysely`) connects directly to the existing Neon database.
- Running as a standalone server (not inside Next.js API routes) keeps auth concerns separated and allows the frontend to remain a pure client.

### Alternatives Considered
| Alternative | Why Rejected |
|---|---|
| Integrate Better-Auth into Next.js API routes | Mixes auth server with frontend; complicates deployment; harder to expose as OIDC provider to FastAPI |
| Keep custom Python JWT auth (current v2) | Doesn't provide OIDC discovery, JWKS, PKCE, or standards-compliant token issuance |
| Use Keycloak/Auth0 | External dependency; heavier operational overhead for a learning platform |

### Key Configuration
```typescript
// better-auth server config
import { betterAuth } from "better-auth";
import { oidcProvider } from "better-auth/plugins";
import { jwt } from "better-auth/plugins";
import { admin } from "better-auth/plugins";

export const auth = betterAuth({
  database: { /* PostgreSQL via Drizzle adapter */ },
  plugins: [
    jwt({ jwks: { jwksPath: "/.well-known/jwks.json" } }),
    oidcProvider({ useJWTPlugin: true, loginPage: "/sign-in" }),
    admin({ roles: { student: {}, instructor: {}, admin: {} } }),
  ],
  socialProviders: {
    google: { clientId: "...", clientSecret: "..." },
    github: { clientId: "...", clientSecret: "..." },
  },
  emailAndPassword: { enabled: true, requireEmailVerification: true },
});
```

---

## R-002: Better-Auth React Client

### Decision
Use `createAuthClient` from `better-auth/react` with `baseURL` pointing to the standalone auth server. Replace the custom `AuthClient` class entirely.

### Rationale
- The official client provides `signIn.email()`, `signUp.email()`, `signIn.social()`, `signOut()`, `useSession()` hooks.
- Handles token refresh, session management, and cookie handling automatically.
- Reduces custom code and bug surface (e.g., the current cookie name mismatch between middleware.ts and backend).

### Key Pattern
```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { adminClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
  plugins: [adminClient()],
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

---

## R-003: JWKS Token Validation in FastAPI

### Decision
Use `PyJWT` with `jwcrypto` for RS256 JWT verification in FastAPI, fetching and caching JWKS from the Better-Auth server's `/.well-known/jwks.json` endpoint.

### Rationale
- FastAPI acts as a **resource server** — it never issues tokens, only validates them.
- JWKS caching (TTL 5 minutes, fallback to last-known-good keys) prevents auth server dependency per request.
- `PyJWT` is more actively maintained than `python-jose` for RS256/JWKS validation.
- Role claims extracted from JWT payload for authorization middleware.

### Alternatives Considered
| Alternative | Why Rejected |
|---|---|
| python-jose | Less active maintenance; PyJWT has better RS256/JWKS support |
| Call auth server per request | Adds latency and coupling; JWKS is the standard pattern |
| Shared secret (HS256) | Not standards-compliant; less secure for multi-service architecture |

### Key Pattern
```python
import jwt
from jwt import PyJWKClient

jwks_client = PyJWKClient(
    uri=f"{BETTER_AUTH_URL}/.well-known/jwks.json",
    cache_jwk_set=True,
    lifespan=300  # 5 min cache
)

def verify_token(token: str) -> dict:
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    return jwt.decode(
        token, signing_key.key,
        algorithms=["RS256"],
        audience="intellistack",
        issuer=BETTER_AUTH_URL
    )
```

---

## R-004: OpenAI ChatKit Integration

### Decision
Use **ChatKit Python SDK** (`chatkit`) for the server-side, integrated into the existing FastAPI process as a single `/chatkit` endpoint. Use **@openai/chatkit-react** for the frontend chat widget.

### Rationale
- ChatKit Python server provides `ChatKitServer` base class with `respond()` method for streaming responses.
- Integrates with the existing OpenAI Agents SDK (`agents` package) already used in the tutor module.
- `PostgresStore` (or custom Store implementation) handles thread/message persistence in the existing Neon database.
- Frontend `<ChatKit />` component with `useChatKit()` hook provides a complete chat UI out of the box.
- Custom `fetch` override injects JWT auth token and page context into every request.

### Alternatives Considered
| Alternative | Why Rejected |
|---|---|
| Build custom chat UI from scratch | Significant effort; ChatKit provides production-ready streaming UI |
| Use Vercel AI SDK | Doesn't integrate with OpenAI Agents SDK; ChatKit is OpenAI's own solution |
| Keep existing custom RAG chat interface | Missing thread management, proper persistence, and polished UI |

### Architecture Pattern
```
Frontend (ChatKit React)         Backend (FastAPI + ChatKit Python)
┌─────────────────────┐          ┌─────────────────────────────┐
│ <ChatKit />          │ ──POST──▶│ /chatkit endpoint           │
│  useChatKit({        │          │  ChatKitServer.process()    │
│    api: {            │          │    ↓                        │
│      url: "/chatkit",│          │  respond() method           │
│      fetch: custom   │          │    → OpenAI Agent + RAG     │
│    }                 │          │    → Stream SSE response    │
│  })                  │          │  Store: PostgresStore       │
└─────────────────────┘          └─────────────────────────────┘
```

### Key Server Pattern
```python
from chatkit.server import ChatKitServer, StreamingResult
from chatkit.store import Store

class IntelliStackChatKitServer(ChatKitServer):
    async def respond(self, thread, input_message, context):
        # 1. Extract user identity + page context from RequestContext
        # 2. Check rate limit (20 msg/day for students)
        # 3. Run RAG retrieval with stage-based access control
        # 4. Run OpenAI Agent with Socratic teaching instructions
        # 5. Yield streaming ThreadStreamEvents
        ...
```

---

## R-005: Data Migration Strategy

### Decision
Big-bang cutover with a migration script that transforms existing auth data into Better-Auth's schema format. Run on staging first, validate, then production with backup.

### Rationale
- Spec explicitly requires big-bang cutover (FR-025).
- Better-Auth has its own table structure (user, session, account, verification tables).
- Existing data (7 auth tables) maps cleanly to Better-Auth schema.
- The migration script must handle: users (preserve IDs), password hashes (bcrypt, compatible), OAuth accounts, and active sessions.

### Migration Steps
1. Backup existing database
2. Run Better-Auth's `npx better-auth migrate` to create its schema
3. Run custom migration script to copy data from old tables to Better-Auth tables
4. Validate: all users can authenticate, OAuth links preserved
5. Remove old auth code paths
6. Update frontend to use Better-Auth client

---

## R-006: Email Delivery

### Decision
Use **Resend API** as primary email provider with SMTP (Gmail) as fallback for development.

### Rationale
- Resend is purpose-built for transactional email (verification, password reset).
- Simple API integration, good deliverability.
- Better-Auth supports custom email handlers.

---

## R-007: ChatKit Store (Persistence)

### Decision
Implement a custom `PostgresStore` extending ChatKit's `Store` base class, using the existing SQLAlchemy async engine and Neon PostgreSQL.

### Rationale
- ChatKit provides an `InMemoryStore` for development and a `Store` base class for custom implementations.
- The existing project already has SQLAlchemy async + Neon PostgreSQL infrastructure.
- Thread/Message models need to include course association, stage context, and retention metadata (FR-018).
- Custom store allows enforcing the 30-day post-completion retention policy.

---

## R-008: Rate Limiting

### Decision
Implement AI tutor rate limiting at the ChatKit server `respond()` method level, using a database counter (messages per user per rolling 24-hour window).

### Rationale
- FR-027 requires 20 messages/day/student, instructors/admins exempt.
- Checking at the respond() level catches all message paths.
- Database counter (not Redis) keeps the architecture simpler and uses existing infrastructure.
- Rate limit info returned in response metadata for frontend display.
