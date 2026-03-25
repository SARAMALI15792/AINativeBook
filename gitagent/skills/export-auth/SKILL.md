---
name: export-auth
description: >
  Migrates the IntelliStack Better-Auth OIDC authentication system to any
  target auth framework, preserving OAuth flows, session management,
  role/permission model, and JWT claim structure.
license: MIT
allowed-tools: read_file, search_code
metadata:
  author: IntelliStack Team
  version: "1.0.0"
  category: migration
---

# Skill: Export Auth

## Purpose
Re-implement IntelliStack's full auth system in any target environment.

## IntelliStack Auth Architecture (Source of Truth)
- **Server:** Better-Auth TypeScript OIDC (`intellistack/auth-server/src/`)
- **Entry:** `auth-server/src/index.ts` — Express server wrapping Better-Auth
- **Config:** `auth-server/src/auth.ts` — providers, session, callbacks
- **OAuth providers:** Google, GitHub
- **Session:** JWT (access token 15 min) + refresh token (7 days)
- **Roles:** `student`, `instructor`, `admin`, `institution_admin`
- **JWT claims:** `sub`, `email`, `role`, `institution_id`, `stage_access[]`

## Supported Target Auth Frameworks
| Target              | Language   | Notes                              |
|---------------------|------------|------------------------------------|
| Auth.js (NextAuth)  | TypeScript | Next.js / Edge                     |
| Passport.js + JWT   | TypeScript | Express / NestJS                   |
| Spring Security     | Java       | OAuth2 Resource Server             |
| Devise + OmniAuth   | Ruby       | Rails                              |
| Laravel Sanctum     | PHP        | SPA / API tokens                   |
| Supabase Auth       | Any        | Managed auth with RLS              |
| Clerk               | Any        | Hosted auth, webhook sync          |
| Keycloak            | Any        | Self-hosted OIDC                   |
| Better-Auth (keep)  | TypeScript | Different backend, same auth       |

## Instructions

### Step 1 — Map the IntelliStack auth flow
Describe:
1. `/auth/sign-in` — credential + OAuth entry points
2. `/auth/callback` — OAuth redirect handling
3. `/auth/sign-out` — session teardown
4. `/auth/refresh` — token refresh
5. `/auth/me` — current user + claims
6. JWT middleware applied to FastAPI routes

### Step 2 — Produce migration plan
```
## Auth Migration Plan → <target>
- Provider credentials needed: GOOGLE_CLIENT_ID/SECRET, GITHUB_CLIENT_ID/SECRET
- Session storage: [cookie / DB / Redis]
- JWT library: [name + version]
- Breaking changes: [anything the target cannot replicate exactly]
```

### Step 3 — Generate auth configuration
Output complete, working auth config for the target including:
- Provider setup (OAuth client ID/secret via env)
- Session/token configuration
- Role extraction from claims
- Protected route middleware

### Step 4 — Role/Permission mapping
Produce a mapping table:
```
IntelliStack Role → Target Role/Policy
student          → ROLE_STUDENT
instructor       → ROLE_INSTRUCTOR
admin            → ROLE_ADMIN
institution_admin → ROLE_INSTITUTION_ADMIN
```

### Step 5 — Security checklist
- [ ] Rotate all OAuth secrets before deploying
- [ ] Set CORS origins to new domain
- [ ] Update OAuth callback URLs in Google/GitHub console
- [ ] Confirm HTTPS in production (cookies require Secure flag)
- [ ] Test token refresh flow end-to-end
