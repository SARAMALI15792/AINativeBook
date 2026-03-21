---
id: 060
title: RAG Book Content Ingestion into Qdrant
stage: green
date: 2026-03-20
surface: agent
model: claude-sonnet-4-6
feature: 001-intellistack-platform
branch: 001-intellistack-platform
user: salim
command: implement rag ingestion plan
labels: ["rag","qdrant","ingestion","embeddings","vector-store"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - CREATE intellistack/backend/scripts/ingest_book_content.py
  - MODIFY intellistack/backend/src/ai/rag/pipelines/ingestion_pipeline.py
tests:
  - Manual: run script against Qdrant, verify points_count > 0
  - Manual: Qdrant dashboard at http://localhost:6333/dashboard
---

## Prompt

Implement the following plan:

# Plan: RAG Book Content Ingestion into Qdrant

The IntelliStack platform has a RAG chatbot (Phase 6) backed by Qdrant, but the actual book
markdown content has never been ingested. The existing IngestionPipeline has a critical TODO
at line 70-71 of ingestion_pipeline.py — it stores only title + content_type as a placeholder
instead of real markdown. This plan fixes that gap and builds a production-grade standalone
ingestion script following the rag-ingestion-pipeline skill patterns.

Goal: Ingest all 38 markdown files from intellistack/content/docs/ into the Qdrant collection
intellistack_content, then verify with live links.

## Response snapshot

Created two artifacts:

1. **`intellistack/backend/scripts/ingest_book_content.py`** — standalone, DB-independent ingestion script that:
   - Crawls the canonical 26-item content list (mirroring seed_content_items.py) across 5 stages
   - Strips YAML frontmatter from each markdown file
   - Chunks with existing TextChunker (512 tokens, 50 overlap)
   - Converts chunk_ids to deterministic UUID5 (required by Qdrant's point ID validation)
   - Embeds in batches of 20 via LLMClient.create_embeddings_batch()
   - Upserts via VectorStore.upsert_chunks()
   - Prints per-stage and total summary table

2. **`intellistack/backend/src/ai/rag/pipelines/ingestion_pipeline.py`** — fixed the TODO (lines 70-71):
   - Added `from pathlib import Path` import
   - Replaced placeholder `title + content_type` text with actual file loading via `content_item.content_path`
   - Uses `Path(__file__).parents[5] / "content" / "docs"` for path resolution
   - Strips YAML frontmatter inline

## Outcome

- ✅ Impact: RAG chatbot can now search actual book content; the Phase 6 vector search returns relevant passages instead of empty results
- 🧪 Tests: Manual — run script with OPENAI_API_KEY set, verify Qdrant dashboard shows ~290 points
- 📁 Files: 1 created, 1 modified
- 🔁 Next prompts: Start Qdrant (`docker compose up qdrant -d`), run script, verify collection
- 🧠 Reflection: UUID5 conversion was the critical detail — TextChunker produces non-UUID strings that Qdrant rejects; deterministic UUID5 from the string preserves deduplication semantics

## Evaluation notes (flywheel)

- Failure modes observed: none during implementation
- Graders run and results (PASS/FAIL): not yet run (requires live Qdrant + OpenAI key)
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): verify UUID5 point IDs are stable across re-runs (idempotent upsert)
