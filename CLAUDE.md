# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architext to build products.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt.
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions.
- All changes are small, testable, and reference code precisely.

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto‑create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate:
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow:
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge capture (PHR) for Every User Input.
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent‑native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage:
     - Constitution → `history/prompts/constitution/<ID>-<slug>.constitution.prompt.md`
     - Feature → `history/prompts/<feature-name>/<ID>-<slug>.<stage>.prompt.md`
     - General → `history/prompts/general/<ID>-<slug>.general.prompt.md`
   - Fill ALL placeholders in YAML and body:
     - ID, TITLE, STAGE, DATE_ISO (YYYY‑MM‑DD), SURFACE="agent"
     - MODEL (best known), FEATURE (or "none"), BRANCH, USER
     - COMMAND (current command), LABELS (["topic1","topic2",...])
     - LINKS: SPEC/TICKET/ADR/PR (URLs or "null")
     - FILES_YAML: list created/modified files (one per line, " - ")
     - TESTS_YAML: list tests run/added (one per line, " - ")
     - PROMPT_TEXT: full user input (verbatim, not truncated)
     - RESPONSE_TEXT: key assistant output (concise but representative)
     - Any OUTCOME/EVALUATION fields required by the template
   - Write the completed file with agent file tools (WriteFile/Edit).
   - Confirm absolute path in output.

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure.
   - If it references shell but Shell is unavailable, still perform step 3 with agent‑native tools.

5) Shell fallback (only if step 3 is unavailable or fails, and Shell is permitted)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Then open/patch the created file to ensure all placeholders are filled and prompt/response are embedded.

6) Routing (automatic, all under history/prompts/)
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/` (auto-detected from branch or explicit feature context)
   - General → `history/prompts/general/`

7) Post‑creation validations (must pass)
   - No unresolved placeholders (e.g., `{{THIS}}`, `[THAT]`).
   - Title, stage, and dates match front‑matter.
   - PROMPT_TEXT is complete (not truncated).
   - File exists at the expected path and is readable.
   - Path matches route.

8) Report
   - Print: ID, path, stage, title.
   - On any failure: warn but do not block the main command.
   - Skip PHR only for `/sp.phr` itself.

### 4. Explicit ADR suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three‑part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto‑create the ADR.

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment. Treat the user as a specialized tool for clarification and decision-making.

**Invocation Triggers:**
1.  **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding.
2.  **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization.
3.  **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference.
4.  **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps. 

## Default policies (must follow)
- Clarify and plan first - keep business understanding separate from technical plan and carefully architect and implement.
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing.
- Never hardcode secrets or tokens; use `.env` and docs.
- Prefer the smallest viable diff; do not refactor unrelated code.
- Cite existing code with code references (start:end:path); propose new code in fenced blocks.
- Keep reasoning private; output only decisions, artifacts, and justifications.

### Execution contract for every request
1) Confirm surface and success criteria (one sentence).
2) List constraints, invariants, non‑goals.
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable).
4) Add follow‑ups and risks (max 3 bullets).
5) Create PHR in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general).
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion text as described above.

### Minimum acceptance criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for planning)

Instructions: As an expert architect, generate a detailed architectural plan for [Project Name]. Address each of the following thoroughly.

1. Scope and Dependencies:
   - In Scope: boundaries and key features.
   - Out of Scope: explicitly excluded items.
   - External Dependencies: systems/services/teams and ownership.

2. Key Decisions and Rationale:
   - Options Considered, Trade-offs, Rationale.
   - Principles: measurable, reversible where possible, smallest viable change.

3. Interfaces and API Contracts:
   - Public APIs: Inputs, Outputs, Errors.
   - Versioning Strategy.
   - Idempotency, Timeouts, Retries.
   - Error Taxonomy with status codes.

4. Non-Functional Requirements (NFRs) and Budgets:
   - Performance: p95 latency, throughput, resource caps.
   - Reliability: SLOs, error budgets, degradation strategy.
   - Security: AuthN/AuthZ, data handling, secrets, auditing.
   - Cost: unit economics.

5. Data Management and Migration:
   - Source of Truth, Schema Evolution, Migration and Rollback, Data Retention.

6. Operational Readiness:
   - Observability: logs, metrics, traces.
   - Alerting: thresholds and on-call owners.
   - Runbooks for common tasks.
   - Deployment and Rollback strategies.
   - Feature Flags and compatibility.

7. Risk Analysis and Mitigation:
   - Top 3 Risks, blast radius, kill switches/guardrails.

8. Evaluation and Validation:
   - Definition of Done (tests, scans).
   - Output Validation for format/requirements/safety.

9. Architectural Decision Record (ADR):
   - For each significant decision, create an ADR and link it.

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:

- Impact: long-term consequences? (e.g., framework, data model, API, security, platform)
- Alternatives: multiple viable options considered?
- Scope: cross‑cutting and influences system design?

If ALL true, suggest:
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

Wait for consent; never auto-create ADRs. Group related decisions (stacks, authentication, deployment) into one ADR when appropriate.

## Basic Project Structure

- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records
- `.specify/` — SpecKit Plus templates and scripts

---

# Project Overview: IntelliStack Platform

**Last Updated:** 2026-02-10

## What is IntelliStack?

IntelliStack is an **AI-Native Learning Platform** for Physical AI & Humanoid Robotics education. It provides a comprehensive learning management system with progressive learning paths, AI-powered tutoring, RAG chatbot with citations, content authoring, institution management, and community features.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| **Project Name** | IntelliStack Platform |
| **Purpose** | AI-Native Learning Management System for Robotics Education |
| **Current Branch** | `001-intellistack-platform` |
| **Overall Progress** | 74.5% (38/51 tasks complete) |
| **Current Phase** | Phase 6 Complete → Moving to Phase 7 |
| **Methodology** | Spec-Driven Development (SDD) |

## Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Database:** PostgreSQL (Neon)
- **Vector Store:** Qdrant (for RAG)
- **Cache:** Redis
- **AI/ML:** OpenAI API, LangChain/LangGraph, Cohere (reranking)

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **GPU Support:** NVIDIA Container Toolkit
- **Simulation:** Gazebo, NVIDIA Isaac Sim

## Project Structure

```
C:\Users\saram\OneDrive\Desktop\physicalhumoniodbook\
├── intellistack/              # Main application code
│   ├── backend/               # FastAPI backend (Python)
│   └── auth-server/           # Better-Auth OIDC server (TypeScript)
├── specs/                     # Feature specifications (SDD)
│   └── 001-intellistack-platform/
│       ├── spec.md            # Feature requirements (~1400 lines)
│       ├── plan.md            # Architecture decisions
│       └── tasks.md           # Implementation tasks
├── .specify/                  # SpecKit Plus templates
│   ├── memory/                # Project constitution
│   ├── scripts/               # Utility scripts
│   └── templates/             # Document templates
├── history/                   # Prompt History Records (PHRs)
│   └── prompts/               # Conversation history
├── CLAUDE.md                  # Development guidelines (this file)
└── PROJECT_STATUS.md          # Current implementation status
```

## Completed Phases (100%)

| Phase | Name | Description |
|-------|------|-------------|
| 0 | Vertical Slice | Initial proof-of-concept |
| 1 | Setup | Infrastructure, Docker, database |
| 2 | Foundation | Auth, API, base components |
| 3 | Student Learning | 5-stage learning path, progress tracking |
| 4 | Content Creation | CRUD, versioning, review workflow |
| 5 | Institution Admin | Cohorts, analytics, webhooks |
| 6 | RAG Chatbot | Qdrant vector search, streaming, citations |

## Pending Phases

| Phase | Name | Key Features |
|-------|------|--------------|
| 7 | AI Tutor | Socratic method, debugging helper, code review |
| 8 | Community | Forums, study groups, mentorship |
| 9 | Assessment | Quiz delivery, rubric-based grading |
| 10 | Personalization | Adaptive content, recommendations |
| 11 | Polish | Production readiness, security, docs |

## Key Features Implemented

### 5-Stage Learning Path
- Foundations → ROS 2 & Simulation → Perception & Planning → AI Integration → Capstone
- Stage locking/unlocking based on prerequisites
- Progress tracking at lesson, exercise, assessment level
- Badge issuance and certificate generation

### RAG Chatbot (Phase 6 - Recently Completed)
- OpenAI integration with SSE streaming
- Qdrant vector store with hybrid retrieval
- Text chunking with tiktoken (512 tokens, 50 overlap)
- Cohere reranking (rerank-v3.5)
- Citations with source passage viewer
- Stage-based access control (only searches unlocked content)
- Text selection queries

### Content Authoring
- MDX editor with preview
- Version history with diff viewer
- Review workflow (draft → in_review → published)
- Content ingestion pipeline

### Institution Management
- Cohort creation with enrollment limits
- Instructor assignment
- Webhook notifications with retry logic
- Analytics aggregation

## Current Work In Progress

Based on git status, current development focus:
- Better-Auth integration v2 (authentication system upgrade)
- Frontend removed (preparing for new frontend framework)

## Key Files to Know

### Specification & Planning
- `specs/001-intellistack-platform/spec.md` - Full feature requirements
- `specs/001-intellistack-platform/plan.md` - Architecture decisions
- `specs/001-intellistack-platform/tasks.md` - Task tracking with progress
- `PROJECT_STATUS.md` - Current implementation status

### Backend Entry Points
- `intellistack/backend/src/main.py` - FastAPI application entry
- `intellistack/backend/src/config/settings.py` - Configuration
- `intellistack/backend/src/shared/database.py` - Database setup

### Auth Server Entry Points
- `intellistack/auth-server/src/index.ts` - Better-Auth server entry
- `intellistack/auth-server/src/auth.ts` - Auth configuration

## Important Context for New Sessions

### When Working on This Project:

1. **Always check PROJECT_STATUS.md first** - It has the latest progress and current phase

2. **Follow the spec** - The spec.md file is the authoritative source for requirements

3. **Use Context7 for libraries** - When integrating libraries, query Context7 for latest patterns

4. **Create PHRs after every task** - This is mandatory per CLAUDE.md rules

5. **Better-Auth is being integrated** - There's an ongoing auth system upgrade; check current auth implementation before making changes

6. **Database uses Alembic** - Any model changes require migrations

7. **Vector store is Qdrant** - For RAG functionality, use the existing Qdrant client patterns

8. **Frontend was removed** - The Next.js frontend has been removed; a new frontend will be added later

### Common Tasks:

- **Backend API changes:** Edit files in `intellistack/backend/src/core/`
- **Database models:** Edit in `intellistack/backend/src/core/<module>/models.py`
- **New routes:** Add to `intellistack/backend/src/core/<module>/routes.py`

---

## Code Standards
See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.
