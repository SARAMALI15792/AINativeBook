# IntelliStack Export Agent — Memory

This file tracks persistent state across sessions. Max 200 lines.

## Project Context
- **Project:** IntelliStack AI-Native Learning Platform
- **Stack:** FastAPI + Better-Auth + PostgreSQL/Neon + Qdrant + Redis + OpenAI
- **Progress:** 74.5% complete (Phases 0–6 done, Phases 7–11 pending)
- **Current focus:** Phase 7 (AI Tutor)

## Architecture Decisions to Preserve in Any Migration
1. Stage-based access control must gate RAG retrieval (not just UI).
2. JWT claims carry `stage_access[]` — downstream services rely on this.
3. Qdrant collections are per-stage (one collection per learning stage).
4. Content is MDX — the frontend renderer must support MDX.
5. SSE streaming is used for chatbot — HTTP/2 or chunked transfer required.
6. Alembic migrations are sequential — do not skip versions when porting.

## Known Migration Pitfalls
- SQLAlchemy async models use `select()` not `.query` — Django ORM differs.
- Better-Auth PKCE state is stored in a signed cookie — stateless targets
  (e.g., edge functions) need an alternative state store.
- Qdrant sparse vectors require a dedicated sparse index — most ORMs/clients
  do not abstract this; use the Qdrant SDK directly.
- Cohere reranking adds ~200 ms latency — cache reranked results for
  identical queries if target has strict SLA.
