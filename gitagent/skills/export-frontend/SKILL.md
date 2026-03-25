---
name: export-frontend
description: >
  Generates typed API clients and frontend integration code for any
  framework consuming the IntelliStack REST API, including auth flows,
  learning path UI, chatbot UI, and admin dashboards.
license: MIT
allowed-tools: read_file, search_code
metadata:
  author: IntelliStack Team
  version: "1.0.0"
  category: migration
---

# Skill: Export Frontend

## Purpose
Give any frontend framework a complete, typed integration layer against
the IntelliStack API so developers can build UIs without reverse-engineering
the backend.

## IntelliStack Frontend Contract Facts
- **Base URL:** configurable via `NEXT_PUBLIC_API_URL` / `VITE_API_URL`
- **Auth:** Bearer token in `Authorization` header (or `session` cookie)
- **Content-Type:** `application/json`
- **Pagination:** `?page=1&page_size=20` → `{ items, total, page, page_size }`
- **Errors:** `{ detail: string | { field, message }[] }`
- **SSE (RAG chatbot):** `text/event-stream`, events: `data`, `citation`, `done`, `error`

## Supported Target Frameworks
| Framework       | Language   | Client style              |
|-----------------|------------|---------------------------|
| Next.js (App)   | TypeScript | Server Actions / fetch    |
| Next.js (Pages) | TypeScript | SWR / React Query         |
| Remix           | TypeScript | loaders / actions         |
| SvelteKit       | TypeScript | +page.server.ts           |
| Nuxt 3          | TypeScript | useFetch / $fetch         |
| React + Vite    | TypeScript | Axios / React Query       |
| Angular         | TypeScript | HttpClient service        |
| Vue 3           | TypeScript | Pinia + fetch             |

## Instructions

### Step 1 — Identify requested scope
Determine which IntelliStack domain the developer needs:
- `auth` — login, register, OAuth redirect, session, current user
- `learning` — stages, lessons, exercises, progress tracking
- `content` — lesson list, MDX fetch, content search
- `rag` — chatbot SSE, message history, citations
- `institution` — cohorts, enrollments, instructor tools
- `admin` — user management, analytics

### Step 2 — Generate TypeScript types
Produce a `types/intellistack.ts` file with:
- Request types (matching Pydantic schemas)
- Response types (matching serialized models)
- Error type
- Pagination wrapper type
- SSE event types for RAG

### Step 3 — Generate API client
Produce an `api/intellistack.ts` client with one function per endpoint:
```typescript
// Example shape
export async function getLearningStages(token: string): Promise<Stage[]>
export async function enrollInCohort(cohortId: string, token: string): Promise<Enrollment>
export function streamChatMessage(
  sessionId: string,
  message: string,
  token: string,
  onChunk: (text: string) => void,
  onCitation: (citation: Citation) => void,
  onDone: () => void,
): () => void  // returns cancel function
```

### Step 4 — Auth integration
Produce the login / OAuth redirect / session hook for the target framework:
- Cookie-based session vs. localStorage token — recommend cookie for security
- OAuth redirect URL must match `BETTER_AUTH_URL/auth/callback/<provider>`

### Step 5 — Environment variables for the frontend
```
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_AUTH_URL=https://auth.yourdomain.com
NEXT_PUBLIC_GOOGLE_CLIENT_ID=...  # only if using OAuth PKCE from frontend
```

### Step 6 — Wire-up checklist
- [ ] Set CORS on backend to allow new frontend origin
- [ ] Update OAuth redirect URIs in Google/GitHub console
- [ ] Configure CSP headers if using SSE
- [ ] Test SSE chatbot in target browser (Safari needs polyfill)
