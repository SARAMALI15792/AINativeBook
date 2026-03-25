---
name: export-rag
description: >
  Re-implements the IntelliStack RAG pipeline (Qdrant + Cohere + OpenAI SSE)
  in any target language or framework, preserving hybrid retrieval, reranking,
  citation architecture, and stage-based access control.
license: MIT
allowed-tools: read_file, search_code
metadata:
  author: IntelliStack Team
  version: "1.0.0"
  category: migration
---

# Skill: Export RAG Pipeline

## Purpose
Port the IntelliStack RAG chatbot — the most complex subsystem — to any
target stack while keeping retrieval quality, citation fidelity, and
streaming behaviour identical.

## IntelliStack RAG Architecture (Source of Truth)

### Ingestion Pipeline
```
Raw document
  → text extraction
  → tiktoken chunking (512 tokens, 50 token overlap)
  → OpenAI text-embedding-3-small (1536 dims)
  → BM25 sparse vector (SPLADE or keyword)
  → Qdrant upsert (collection per stage)
      payload: { source_id, chunk_index, stage_id, lesson_id, text }
```

### Retrieval Pipeline
```
User query
  → dense embedding (text-embedding-3-small)
  → Qdrant hybrid search (dense + sparse, top-20)
  → stage_access filter (only user's unlocked stages)
  → Cohere rerank-v3.5 (top-5)
  → system prompt assembly
  → OpenAI GPT-4o streaming (SSE)
  → citation extraction from streamed text
```

### SSE Event Schema
```
event: data      → { content: string }
event: citation  → { id, source_id, lesson_id, passage, score }
event: done      → {}
event: error     → { message: string }
```

### Source Files
- `intellistack/backend/src/core/rag/routes.py` — endpoints
- `intellistack/backend/src/core/rag/service.py` — retrieval + LLM
- `intellistack/backend/src/core/rag/ingestion.py` — chunking + embedding
- `intellistack/backend/src/core/rag/schemas.py` — request/response shapes

## Supported Target Stacks
| Target                    | Language   | Notes                         |
|---------------------------|------------|-------------------------------|
| LangChain.js + Express    | TypeScript | Drop-in for Node backends     |
| LlamaIndex (Python)       | Python     | Alternative retrieval engine  |
| Spring AI                 | Java       | Spring Boot RAG               |
| Go + Qdrant Go SDK        | Go         | Low-latency option            |
| Vercel AI SDK             | TypeScript | Edge-compatible streaming     |

## Instructions

### Step 1 — Confirm Qdrant stays or is replaced
Ask: "Are you keeping Qdrant as the vector store, or switching?"
- Keep Qdrant → port only the application layer
- Switch → also produce the new vector store config + ingestion adapter

### Step 2 — Produce ingestion adapter
For the target language, produce:
1. Chunking function (512 tokens, 50 overlap — use tiktoken or equivalent)
2. Embedding call (OpenAI `text-embedding-3-small` or alternative)
3. Qdrant upsert (collection name, vector + payload structure)

### Step 3 — Produce retrieval + LLM function
1. Dense embedding of user query
2. Qdrant hybrid query with stage filter
3. Cohere rerank call (or alternative reranker)
4. System prompt template (preserve citation instruction exactly)
5. Streaming LLM call with SSE output

### Step 4 — Produce SSE endpoint
For the target framework, wire the streaming function to an HTTP endpoint
that emits the exact SSE event schema above.

### Step 5 — Environment variables
```
OPENAI_API_KEY=
COHERE_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION_PREFIX=intellistack_stage_
```

### Step 6 — Quality checklist
- [ ] Citation IDs are stable across requests (use chunk UUID, not position)
- [ ] Stage access filter applied before reranking, not after
- [ ] SSE connection closed gracefully on client disconnect
- [ ] Streaming errors emit `event: error` before closing stream
- [ ] Ingestion is idempotent (upsert by chunk UUID)
