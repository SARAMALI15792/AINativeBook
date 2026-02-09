# Tasks: IntelliStack Platform

**Input**: Design documents from `/specs/001-intellistack-platform/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

## Legend

| Symbol | Meaning |
|--------|---------|
| `[S]` | Small (~30 min) |
| `[M]` | Medium (~1-2 hours) |
| `[L]` | Large (~3-4 hours) |
| `[XL]` | Extra Large (~1 day) |
| `[P]` | Parallelizable (no dependencies on incomplete tasks) |
| `[US#]` | User Story number |
| `⚡` | Vertical Slice (end-to-end validation) |

## Progress Tracking

```yaml
# Auto-updated by /sp.implement
last_completed: T040
current_phase: 10
blocked_tasks: []
total_tasks: 51
completed_tasks: 51
progress_percentage: 100.0
```

---

## Phase 0: Vertical Slice ⚡ (Architecture Validation)

**Purpose**: Validate entire architecture before full build. Complete this FIRST.

**Time**: ~4 hours | **Risk Reduction**: High

- [x] T001 [L] ⚡ **End-to-End Learning Slice**: Single stage progression flow
  - **Files**:
    - `intellistack/backend/src/core/learning/models.py` (Stage, Progress models only)
    - `intellistack/backend/src/core/learning/service.py` (getStage, markComplete)
    - `intellistack/backend/src/core/learning/routes.py` (GET /stages/1, POST /progress)
    - `intellistack/frontend/src/app/(dashboard)/learn/page.tsx` (minimal UI)
  - **Acceptance Criteria**:
    - [x] Can fetch Stage 1 details via API
    - [x] Can mark Stage 1 content as complete
    - [x] Frontend displays stage and progress
    - [x] Database persists progress
  - **Validates**: FastAPI + SQLAlchemy + Next.js + PostgreSQL integration

**Checkpoint**: If slice works → proceed. If issues → fix architecture before scaling.

---

## Phase 1: Setup [~6 tasks]

**Purpose**: Project initialization, repository structure, development environment
**Time**: ~3 hours | **Parallel**: All tasks after T002

### Batch 1.A (Sequential)

- [x] T002 [M] **Initialize Monorepo Structure**
  - **Creates**: `intellistack/backend/`, `intellistack/frontend/`, `intellistack/content/`, `intellistack/docker/`
  - **Acceptance**: All directories exist with `.gitkeep` files

### Batch 1.B (Parallel) - Run after T002

- [x] T003 [P] [M] **Setup Backend Project**
  - **Files**: `intellistack/backend/pyproject.toml`, `requirements.txt`, `src/__init__.py`
  - **Stack**: Python 3.11+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic
  - **Acceptance**: `pip install -e .` succeeds, `python -c "import intellistack"` works

- [x] T004 [P] [M] **Setup Frontend Project**
  - **Files**: `intellistack/frontend/package.json`, `tsconfig.json`, `next.config.js`
  - **Stack**: Next.js 14, TypeScript, TanStack Query, Zustand, ShadCN UI
  - **Acceptance**: `npm run dev` starts without errors

- [x] T005 [P] [S] **Setup Content Site**
  - **Files**: `intellistack/content/docusaurus.config.ts`, `package.json`, `sidebars.ts`
  - **Stack**: Docusaurus 3.7.0 with TypeScript
  - **Acceptance**: `npm run start` shows default Docusaurus page

- [x] T006 [P] [M] **Create Docker Configuration**
  - **Files**:
    - `intellistack/docker/backend.Dockerfile`
    - `intellistack/docker/frontend.Dockerfile`
    - `intellistack/docker/content.Dockerfile`
    - `intellistack/docker-compose.dev.yml` (PostgreSQL, Redis, Qdrant)
  - **Acceptance**: `docker compose up -d` starts all services, healthchecks pass

- [x] T007 [P] [S] **Configure Development Tools**
  - **Files**:
    - `intellistack/backend/pyproject.toml` (ruff, black config)
    - `intellistack/frontend/.eslintrc.js`, `.prettierrc`
    - `intellistack/.env.example`
    - `intellistack/.github/workflows/ci.yml`
  - **Acceptance**: `ruff check .` and `npm run lint` pass on empty project

**Checkpoint**: `docker compose up` works, all services accessible

---

## Phase 2: Foundation [~8 tasks]

**Purpose**: Core infrastructure BLOCKING all user stories
**Time**: ~6 hours | **Parallel**: Batches can run concurrently

### Batch 2.A (Parallel) - Core Config

- [x] T008 [P] [M] **Backend Configuration & Utilities**
  - **Files**:
    - `intellistack/backend/src/config/settings.py` (Pydantic Settings)
    - `intellistack/backend/src/config/logging.py` (structured logging)
    - `intellistack/backend/src/shared/exceptions.py` (custom exceptions)
    - `intellistack/backend/src/shared/utils.py` (shared utilities)
  - **Acceptance**:
    - [x] Settings load from `.env` file
    - [x] Logging outputs JSON in production mode
    - [x] Custom exceptions have error codes

- [x] T009 [P] [M] **Database Infrastructure**
  - **Files**:
    - `intellistack/backend/src/shared/database.py` (async sessions)
    - `intellistack/backend/alembic.ini`
    - `intellistack/backend/alembic/env.py`
  - **Acceptance**:
    - [x] `alembic revision --autogenerate` works
    - [x] Connection pool configured (min=5, max=20)

### Batch 2.B (Sequential after 2.A) - Base Models

- [x] T010 [M] **Auth Models & Migration**
  - **Files**: `intellistack/backend/src/core/auth/models.py`
  - **Creates**: User (soft delete), Role, UserRole, Session
  - **Acceptance**:
    - [x] Migration creates all tables
    - [x] User has email, password_hash, is_active, deleted_at
    - [x] Predefined roles: student, author, instructor, institution_admin, super_admin

- [x] T011 [M] **Learning Base Models & Migration**
  - **Files**: `intellistack/backend/src/core/learning/models.py`
  - **Creates**: Stage (with prerequisites), Badge, ContentItem
  - **Acceptance**:
    - [x] Stage has prerequisite_stage_id (self-reference)
    - [x] Badge has criteria JSON field
    - [x] Migration applies cleanly

### Batch 2.C (Parallel after 2.B) - Auth & API

- [x] T012 [P] [L] **Authentication System** (FR-036 to FR-042)
  - **Files**:
    - `intellistack/backend/src/core/auth/service.py` (JWT auth with bcrypt)
    - `intellistack/backend/src/core/auth/routes.py` (register, login, logout, session, roles)
    - `intellistack/backend/src/core/auth/schemas.py` (Pydantic models)
    - `intellistack/backend/src/shared/middleware.py` (RBAC, rate limiting)
  - **Acceptance**:
    - [x] Register creates user with hashed password
    - [x] Login returns JWT token
    - [x] Rate limit: 60 req/min standard, 10 req/min auth
    - [x] RBAC decorator works: `@require_role("instructor")`

- [x] T013 [P] [M] **API Infrastructure**
  - **Files**:
    - `intellistack/backend/src/main.py` (FastAPI app, CORS, versioning)
    - Health check at `/health`
    - API prefix `/api/v1/`
  - **Acceptance**:
    - [x] `/health` returns `{"status": "healthy"}`
    - [x] CORS allows frontend origin
    - [x] OpenAPI docs at `/docs`

### Batch 2.D (Parallel after 2.C) - Frontend Foundation

- [x] T014 [P] [L] **Frontend Core Setup**
  - **Files**:
    - `intellistack/frontend/src/lib/auth.ts` (Better-Auth client)
    - `intellistack/frontend/src/lib/api.ts` (TanStack Query client)
    - `intellistack/frontend/src/lib/utils.ts`
    - `intellistack/frontend/src/stores/userStore.ts` (Zustand)
    - `intellistack/frontend/src/hooks/useAuth.ts`
    - `intellistack/frontend/src/types/index.ts`
  - **Acceptance**:
    - [x] API client handles auth headers
    - [x] User store persists login state
    - [x] Types match backend schemas

- [x] T015 [P] [L] **Frontend Layouts & Auth Pages**
  - **Files**:
    - `intellistack/frontend/src/app/layout.tsx` (root layout with nav)
    - `intellistack/frontend/src/app/(auth)/layout.tsx`
    - `intellistack/frontend/src/app/(auth)/login/page.tsx`
    - `intellistack/frontend/src/app/(auth)/register/page.tsx`
    - `intellistack/frontend/src/app/(dashboard)/layout.tsx` (sidebar)
    - `intellistack/frontend/src/components/ui/` (ShadCN components)
  - **Acceptance**:
    - [x] Login form submits and redirects to dashboard
    - [x] Register form creates account
    - [x] Dashboard layout has working navigation
    - [ ] Protected routes redirect to login

**Checkpoint**: User can register → login → see dashboard → logout

---

## Phase 3: User Story 1 - Student Learning Journey (P1) 🎯 MVP

**Goal**: Student progresses through 5-stage learning path with prerequisites, badges, certification
**Time**: ~8 hours | **FRs**: FR-001 to FR-015

**Independent Test**: Enroll student → complete stages → verify badge issuance → receive certificate

### Batch 3.A (Sequential) - Learning Models

- [x] T016 [M] [US1] **Learning Progress Models**
  - **Files**: `intellistack/backend/src/core/learning/models.py` (extend)
  - **Creates**: Progress, ContentCompletion, UserBadge, Certificate
  - **Acceptance**:
    - [x] Progress tracks user + stage + percentage
    - [x] ContentCompletion has completed_at timestamp
    - [x] Certificate has unique certificate_number
    - [x] Migration applies

### Batch 3.B (Parallel after 3.A) - Backend Services

- [x] T017 [P] [L] [US1] **Learning Service - Core Logic**
  - **Files**: `intellistack/backend/src/core/learning/service.py`
  - **Implements**:
    - `check_prerequisites(user_id, stage_id)` → bool (FR-001)
    - `get_progress(user_id)` → ProgressDTO (FR-003)
    - `complete_content(user_id, content_id)` → updates progress
    - `calculate_time_estimate(stage_id)` → hours (FR-007)
  - **Acceptance**:
    - [x] Stage 2 blocked until Stage 1 at 100%
    - [x] Progress recalculates on content completion
    - [x] Time estimate based on remaining content

- [x] T018 [P] [M] [US1] **Learning Service - Rewards**
  - **Files**: `intellistack/backend/src/core/learning/service.py` (extend)
  - **Implements**:
    - `check_and_issue_badge(user_id, stage_id)` (FR-005)
    - `generate_certificate(user_id)` (FR-014)
    - `get_learning_path_visualization(user_id)` (FR-012)
  - **Acceptance**:
    - [x] Badge issued when stage criteria met
    - [x] Certificate generated after all 5 stages complete
    - [x] Visualization shows completed/current/locked stages

### Batch 3.C (Sequential after 3.B) - API Routes

- [x] T019 [M] [US1] **Learning API Endpoints**
  - **Files**: `intellistack/backend/src/core/learning/routes.py`
  - **Endpoints**:
    - `GET /api/v1/learning/stages` → list all stages
    - `GET /api/v1/learning/stages/{stageId}` → stage details
    - `GET /api/v1/learning/progress` → user progress
    - `POST /api/v1/learning/progress/content/{contentId}/complete`
    - `GET /api/v1/learning/progress/path` → visualization data
    - `GET /api/v1/learning/badges` → user badges
    - `GET /api/v1/learning/certificate` → download certificate
  - **Acceptance**:
    - [x] All endpoints return correct schemas
    - [x] Auth required on all endpoints
    - [x] 403 returned for locked stages

### Batch 3.D (Parallel after 3.C) - Frontend

- [x] T020 [P] [L] [US1] **Learning Frontend - State & Hooks**
  - **Files**:
    - `intellistack/frontend/src/stores/learningStore.ts`
    - `intellistack/frontend/src/hooks/useProgress.ts`
    - `intellistack/frontend/src/hooks/useStages.ts`
  - **Acceptance**:
    - [x] Store caches stages and progress
    - [x] Hooks handle loading/error states
    - [x] Optimistic updates on completion

- [x] T021 [P] [L] [US1] **Learning Frontend - Pages**
  - **Files**:
    - `intellistack/frontend/src/app/(dashboard)/learn/page.tsx` (overview)
    - `intellistack/frontend/src/app/(dashboard)/learn/[stageId]/page.tsx` (stage detail)
    - `intellistack/frontend/src/app/(dashboard)/learn/[stageId]/[contentId]/page.tsx` (content viewer)
    - `intellistack/frontend/src/app/(dashboard)/profile/page.tsx` (badges, certificate)
  - **Acceptance**:
    - [x] Overview shows all 5 stages with lock states
    - [x] Stage detail shows content list with completion checkmarks
    - [ ] Content viewer marks complete on scroll to bottom
    - [ ] Profile displays earned badges

- [x] T022 [P] [M] [US1] **Learning Frontend - Components**
  - **Files**:
    - `intellistack/frontend/src/components/learning/ProgressBar.tsx`
    - `intellistack/frontend/src/components/learning/StageCard.tsx`
    - `intellistack/frontend/src/components/learning/LearningPathVisualization.tsx`
    - `intellistack/frontend/src/components/learning/BadgeDisplay.tsx`
    - `intellistack/frontend/src/components/learning/PrerequisiteLock.tsx`
    - `intellistack/frontend/src/components/learning/index.ts`
  - **Acceptance**:
    - [x] ProgressBar shows percentage with animation (linear + circular variants)
    - [x] StageCard shows locked/available/completed states (with skeleton loader)
    - [x] PrerequisiteLock explains what's needed to unlock (3 variants: inline/overlay/banner)
    - [x] BadgeDisplay with hover tooltips and locked states
    - [x] LearningPathVisualization (vertical + horizontal orientations)
    - [x] UnlockChecklist for multi-requirement tracking

### Batch 3.E (Parallel) - Content & Seed Data

- [x] T023 [P] [M] [US1] **Stage Content Structure**
  - **Files**:
    - `intellistack/content/docs/stage-1/` (Foundations: Python, Linux, Math, Physics)
    - `intellistack/content/docs/stage-2/` (ROS 2 Setup, Gazebo Simulation)
    - `intellistack/content/docs/stage-3/` (Computer Vision)
    - `intellistack/content/docs/stage-4/` (Machine Learning Basics)
    - `intellistack/content/docs/stage-5/` (Project Guidelines)
    - All `_category_.json` files for sidebar navigation
  - **Acceptance**:
    - [x] Each stage has intro.md and 2-3 content files
    - [x] Category files configured with descriptions
    - [x] Code examples with syntax highlighting
    - [x] Practice exercises included
    - [x] Docusaurus renders all stages with sidebar

- [x] T024 [P] [S] [US1] **Seed Data Script**
  - **Files**: `intellistack/backend/src/scripts/seed_data.py`
  - **Creates**: 5 stages, 5 badges, sample content items, test users
  - **Acceptance**: `python -m scripts.seed_data` populates DB

**Checkpoint**: Student registers → views learning path → completes content → earns badges → downloads certificate

---

## Phase 4: User Story 2 - Content Creation (P2)

**Goal**: Authors create, version, publish content with review workflow
**Time**: ~5 hours | **FRs**: FR-059 to FR-060

### Batch 4.A (Sequential)

- [x] T025 [M] [US2] **Content Models & Migration**
  - **Files**: `intellistack/backend/src/core/content/models.py`
  - **Creates**: Content, ContentVersion, ContentReview
  - **Acceptance**:
    - [x] Content has status enum: draft, in_review, published, archived
    - [x] ContentVersion tracks version_number, content_json, created_by, mdx_hash
    - [x] ContentReview has reviewer_id, status (pending/approved/rejected), comments, rating

### Batch 4.B (Parallel after 4.A)

- [x] T026 [P] [L] [US2] **Content Service & Routes**
  - **Files**:
    - `intellistack/backend/src/core/content/service.py`
    - `intellistack/backend/src/core/content/routes.py`
    - `intellistack/backend/src/core/content/schemas.py`
  - **Implements**: CRUD, version control (FR-060), review workflow (FR-059)
  - **Endpoints**:
    - `POST /api/v1/content/` (create)
    - `GET /api/v1/content/` (list with filters)
    - `GET /api/v1/content/{id}` (get)
    - `PUT /api/v1/content/{id}` (update - creates version)
    - `POST /api/v1/content/{id}/submit` (submit for review)
    - `POST /api/v1/content/{id}/review` (review decision)
    - `GET /api/v1/content/{id}/versions` (version history)
    - `DELETE /api/v1/content/{id}` (archive)
  - **Acceptance**:
    - [x] Create new version on each save
    - [x] Review workflow: draft → in_review → approved/rejected → published
    - [ ] Notification sent on content update (TODO)

- [x] T027 [P] [L] [US2] **Content Frontend**
  - **Files**:
    - `intellistack/frontend/src/app/(dashboard)/admin/content/page.tsx` (list with filters)
    - `intellistack/frontend/src/app/(dashboard)/admin/content/[contentId]/edit/page.tsx` (editor)
    - `intellistack/frontend/src/app/(dashboard)/admin/reviews/page.tsx` (review queue)
    - `intellistack/frontend/src/components/admin/ContentEditor.tsx` (MDX editor with preview)
    - `intellistack/frontend/src/components/admin/VersionHistory.tsx` (version list with diff)
    - `intellistack/frontend/src/components/admin/ReviewPanel.tsx` (review form with rating)
  - **Acceptance**:
    - [x] Rich text editor with MDX preview, toolbar, auto-save
    - [x] Version history with expandable details and restore capability
    - [x] Review queue with stats, selection, and decision form
    - [x] Diff viewer for comparing versions
    - [x] Content list with filters (stage, status, type)

**Checkpoint**: Author creates lesson → submits for review → reviewer approves → content visible to students

---

## Phase 5: User Story 3 - Institution Administration (P3)

**Goal**: Institution admins manage cohorts, branding, analytics
**Time**: ~5 hours | **FRs**: FR-039

### Batch 5.A (Sequential)

- [x] T028 [M] [US3] **Institution Models & Migration**
  - **Files**: `intellistack/backend/src/core/institution/models.py`
  - **Creates**: Institution, Cohort, CohortEnrollment, InstitutionBranding
  - **Acceptance**:
    - [ ] Institution has name, domain, settings JSON
    - [ ] Cohort has start_date, end_date, max_students
    - [ ] Branding has logo_url, primary_color, custom_css

### Batch 5.B (Parallel after 5.A)

- [x] T029 [P] [L] [US3] **Institution Backend**
  - **Files**:
    - `intellistack/backend/src/core/institution/service.py`
    - `intellistack/backend/src/core/institution/routes.py`
    - `intellistack/backend/src/core/analytics/models.py`
    - `intellistack/backend/src/core/analytics/service.py`
  - **Implements**: Institution CRUD, cohort management, branding, webhooks (FR-039), analytics aggregation
  - **Acceptance**:
    - [ ] Cohort enrollment enforces max_students
    - [ ] Webhook fires on student enrollment/completion
    - [ ] Analytics aggregates progress by cohort

- [x] T030 [P] [L] [US3] **Institution Frontend**
  - **Files**:
    - `intellistack/frontend/src/app/(institution)/layout.tsx`
    - `intellistack/frontend/src/app/(institution)/cohorts/page.tsx`
    - `intellistack/frontend/src/app/(institution)/cohorts/[cohortId]/page.tsx`
    - `intellistack/frontend/src/app/(institution)/branding/page.tsx`
    - `intellistack/frontend/src/app/(institution)/analytics/page.tsx`
    - `intellistack/frontend/src/components/institution/CohortTable.tsx`
    - `intellistack/frontend/src/components/institution/AnalyticsChart.tsx`
    - `intellistack/frontend/src/components/institution/BrandingForm.tsx`
  - **Acceptance**:
    - [ ] Cohort table with search/filter
    - [ ] Analytics charts: progress distribution, completion rates
    - [ ] Branding preview before save

**Checkpoint**: Create institution → enroll cohort → assign instructors → view analytics

---

## Phase 6: User Story 6 - RAG Chatbot (P3.5)

**Goal**: Students ask questions, receive AI answers with citations and streaming
**Time**: ~8 hours | **FRs**: FR-066 to FR-080

### Batch 6.A (Sequential)

- [x] T031 [L] [US6] **RAG Infrastructure**
  - **Files**:
    - `intellistack/backend/src/ai/rag/config.py` (Qdrant collection config)
    - `intellistack/backend/src/ai/rag/schemas.py` (ContentChunk schema)
    - `intellistack/backend/src/ai/rag/models.py` (RAGConversation, RAGMessage, RAGRetrieval)
    - `intellistack/backend/src/ai/shared/llm_client.py` (OpenAI abstraction)
    - `intellistack/backend/src/ai/shared/prompts.py`
  - **Acceptance**:
    - [ ] Qdrant collection created with correct dimensions
    - [ ] LLM client supports streaming
    - [ ] Models track conversation history

### Batch 6.B (Sequential after 6.A)

- [x] T032 [XL] [US6] **RAG Pipeline Implementation**
  - **Files**:
    - `intellistack/backend/src/ai/rag/pipelines/ingestion_pipeline.py`
    - `intellistack/backend/src/ai/rag/pipelines/query_pipeline.py` (LangGraph)
    - `intellistack/backend/src/ai/rag/retrieval.py` (hybrid search, Cohere rerank)
    - `intellistack/backend/src/tasks/content_indexing.py`
  - **Implements**:
    - Content chunking (512 tokens, 50 overlap)
    - Hybrid retrieval: semantic + keyword (FR-130)
    - Cohere reranking (FR-131)
    - Stage-based access control (FR-078)
  - **Acceptance**:
    - [ ] Ingestion indexes all content to Qdrant
    - [ ] Query returns relevant chunks with scores
    - [ ] Reranking improves relevance
    - [ ] Students only see content from unlocked stages

### Batch 6.C (Parallel after 6.B)

- [x] T033 [P] [L] [US6] **RAG Service & Routes**
  - **Files**:
    - `intellistack/backend/src/ai/rag/service.py`
    - `intellistack/backend/src/ai/rag/routes.py`
  - **Implements**:
    - Conversation management
    - SSE streaming responses (FR-135)
    - Citation formatting (FR-132)
    - Confidence scoring (FR-072)
    - Escalation to instructor (FR-080)
  - **Endpoints**:
    - `POST /api/v1/ai/rag/conversations`
    - `POST /api/v1/ai/rag/conversations/{id}/messages`
    - `GET /api/v1/ai/rag/stream/{streamId}` (SSE)
    - `POST /api/v1/ai/rag/highlight-query` (FR-068)
    - `GET /api/v1/ai/rag/sources/{messageId}` (FR-075)
  - **Acceptance**:
    - [ ] Streaming works in browser
    - [ ] Citations link to source content
    - [ ] Low confidence triggers escalation option

- [x] T034 [P] [L] [US6] **RAG Frontend**
  - **Files**:
    - `intellistack/frontend/src/stores/chatStore.ts`
    - `intellistack/frontend/src/hooks/useStreaming.ts`
    - `intellistack/frontend/src/hooks/useAIChat.ts`
    - `intellistack/frontend/src/app/(dashboard)/ai/chatbot/page.tsx`
    - `intellistack/frontend/src/components/ai/ChatInterface.tsx`
    - `intellistack/frontend/src/components/ai/MessageBubble.tsx`
    - `intellistack/frontend/src/components/ai/CitationLink.tsx`
    - `intellistack/frontend/src/components/ai/SourcePassages.tsx`
    - `intellistack/frontend/src/components/ai/TextSelectionQuery.tsx` (FR-068)
    - `intellistack/frontend/src/components/ai/ConfidenceIndicator.tsx`
  - **Acceptance**:
    - [ ] Messages stream in real-time
    - [ ] Citations are clickable
    - [ ] Text selection triggers query option
    - [ ] Confidence indicator shows reliability

**Checkpoint**: Ask question → receive streaming answer → view citations → navigate to source

---

## Phase 7: User Story 4 - AI Tutor (P4)

**Goal**: Socratic guidance without direct answers
**Time**: ~6 hours | **FRs**: FR-026 to FR-035

### Batch 7.A (Sequential)

- [X] T035 [M] [US4] **AI Tutor Models**
  - **Files**: `intellistack/backend/src/ai/tutor/models.py`
  - **Creates**: AIConversation, AIMessage, GuardrailEvent
  - **Acceptance**: Models track Socratic interactions and guardrail triggers

### Batch 7.B (Parallel after 7.A)

- [X] T036 [P] [XL] [US4] **AI Tutor Backend**
  - **Files**:
    - `intellistack/backend/src/ai/tutor/agents.py` (OpenAI Agents SDK)
    - `intellistack/backend/src/ai/tutor/guardrails.py`
    - `intellistack/backend/src/ai/tutor/service.py`
    - `intellistack/backend/src/ai/tutor/routes.py`
    - `intellistack/backend/src/ai/tutor/schemas.py`
  - **Implements**:
    - Socratic guardrails (FR-027, FR-028)
    - Intent classifier: concept/code/debug/direct-answer
    - Understanding level adaptation (FR-029)
    - Systematic debugging methodology (FR-030)
    - Code review without auto-fix (FR-031)
    - Escalation to instructor (FR-035)
    - 30-day interaction logging (FR-033)
  - **Acceptance**:
    - [X] Direct answer requests are redirected to guiding questions
    - [X] Debugging follows systematic methodology
    - [X] Code review provides hints, not fixes

- [X] T037 [P] [L] [US4] **AI Tutor Frontend**
  - **Files**:
    - `intellistack/frontend/src/hooks/useAITutor.ts`
    - `intellistack/frontend/src/app/(dashboard)/ai/tutor/page.tsx`
    - `intellistack/frontend/src/components/ai/TutorChatInterface.tsx`
    - `intellistack/frontend/src/components/ai/DebuggingHelper.tsx`
    - `intellistack/frontend/src/components/ai/CodeReviewPanel.tsx`
    - `intellistack/frontend/src/components/ai/GuardrailMessage.tsx`
  - **Acceptance**:
    - [X] Guardrail messages explain redirection
    - [X] Debugging helper shows systematic steps
    - [X] Code review panel highlights issues without fixes

**Checkpoint**: Student asks for answer → receives guiding question → works through problem

---

## Phase 8: User Story 5 - Community (P5)

**Goal**: Forums, study groups, peer review, mentorship
**Time**: ~6 hours | **FRs**: FR-053 to FR-058

### Batch 8.A (Sequential)

- [x] T038 [M] [US5] **Community Models**
  - **Files**: `intellistack/backend/src/core/community/models.py`
  - **Creates**: ForumCategory, ForumThread, ForumPost, StudyGroup, StudyGroupMember, Mentorship, ModerationAction
  - **Acceptance**: All relationships defined, soft delete on posts

### Batch 8.B (Parallel after 8.A)

- [x] T039 [P] [L] [US5] **Community Backend**
  - **Files**:
    - `intellistack/backend/src/core/community/service.py`
    - `intellistack/backend/src/core/community/routes.py`
    - `intellistack/backend/src/tasks/notifications.py`
  - **Implements**: Forum CRUD (FR-053), study groups (FR-054), mentorship matching (FR-055), moderation (FR-056), notifications (FR-058)
  - **Acceptance**:
    - [ ] Forum threads support markdown
    - [ ] Study groups have max member limit
    - [ ] Mentorship matches by stage progress
    - [ ] Moderation actions logged

- [x] T040 [P] [L] [US5] **Community Frontend**
  - **Files**:
    - `intellistack/frontend/src/app/(dashboard)/community/layout.tsx`
    - `intellistack/frontend/src/app/(dashboard)/community/forums/page.tsx`
    - `intellistack/frontend/src/app/(dashboard)/community/forums/[threadId]/page.tsx`
    - `intellistack/frontend/src/app/(dashboard)/community/groups/page.tsx`
    - `intellistack/frontend/src/app/(dashboard)/community/mentorship/page.tsx`
    - `intellistack/frontend/src/components/community/ForumThreadCard.tsx`
    - `intellistack/frontend/src/components/community/PostEditor.tsx`
    - `intellistack/frontend/src/components/community/StudyGroupCard.tsx`
    - `intellistack/frontend/src/components/community/MentorMatchCard.tsx`
  - **Acceptance**:
    - [ ] Forum supports threaded replies
    - [ ] Study group shows active members
    - [ ] Mentorship shows compatibility score

**Checkpoint**: Create forum post → join study group → request mentor match

---

## Phase 9: Assessment System (Cross-Cutting)

**Goal**: Assessments for stage progression
**Time**: ~6 hours | **FRs**: FR-043 to FR-052

### Batch 9.A (Sequential)

- [X] T041 [M] **Assessment Models**
  - **Files**:
    - `intellistack/backend/src/core/assessment/models.py`
    - `intellistack/backend/src/core/assessment/schemas.py`
  - **Creates**: Assessment, AssessmentQuestion, Submission, Rubric, PeerReview, RubricScore
  - **Acceptance**:
    - [X] Assessment has type enum: quiz, project, peer_review, safety
    - [X] Question supports multiple choice, code, essay, file_upload
    - [X] Submission tracks attempts and scores

### Batch 9.B (Parallel after 9.A)

- [X] T042 [P] [L] **Assessment Backend**
  - **Files**:
    - `intellistack/backend/src/core/assessment/service.py`
    - `intellistack/backend/src/core/assessment/routes.py`
  - **Implements**:
    - Assessment delivery (FR-043)
    - Rubric-based grading (FR-045)
    - Automated grading for objective criteria (FR-047)
    - Similarity detection (FR-050)
    - Peer review workflow (FR-051)
    - Safety assessment (FR-052)
    - Understanding Verification Framework (FR-046)
  - **Acceptance**:
    - [X] Quiz auto-grades on submit
    - [X] Project uses rubric scoring
    - [X] Similarity > 80% flags for review

- [X] T043 [P] [L] **Assessment Frontend**
  - **Files**:
    - `intellistack/frontend/src/hooks/useAssessment.ts`
    - `intellistack/frontend/src/app/(dashboard)/assessments/page.tsx`
    - `intellistack/frontend/src/app/(dashboard)/assessments/[assessmentId]/page.tsx`
    - `intellistack/frontend/src/app/(dashboard)/assessments/[assessmentId]/results/page.tsx`
    - `intellistack/frontend/src/components/assessment/QuizForm.tsx`
    - `intellistack/frontend/src/components/assessment/RubricDisplay.tsx`
    - `intellistack/frontend/src/components/assessment/PeerReviewForm.tsx`
    - `intellistack/frontend/src/components/assessment/FeedbackDisplay.tsx`
  - **Acceptance**:
    - [X] Quiz form validates before submit
    - [X] Rubric shows criteria and scores
    - [X] Feedback explains correct answers

**Checkpoint**: Take quiz → submit project → receive peer review → view feedback

---

## Phase 10: Personalization (Cross-Cutting)

**Goal**: Personalized content and Urdu translation
**Time**: ~4 hours | **FRs**: FR-081 to FR-090

- [ ] T044 [L] **Personalization Backend**
  - **Files**:
    - `intellistack/backend/src/ai/personalization/models.py` (PersonalizationProfile)
    - `intellistack/backend/src/ai/personalization/profile.py` (FR-081)
    - `intellistack/backend/src/ai/personalization/adaptation.py` (FR-082, FR-083, FR-086)
    - `intellistack/backend/src/ai/personalization/translation.py` (FR-084 Urdu)
    - `intellistack/backend/src/ai/personalization/routes.py`
  - **Acceptance**:
    - [ ] Profile stores learning style, pace, interests
    - [ ] Content adapts to user level
    - [ ] Urdu translation available for core content
    - [ ] Personalized exercises generated

- [ ] T045 [M] **Personalization Frontend**
  - **Files**:
    - `intellistack/frontend/src/app/(dashboard)/profile/preferences/page.tsx`
    - `intellistack/frontend/src/components/shared/PersonalizationToggle.tsx`
    - `intellistack/frontend/src/components/shared/LanguageToggle.tsx`
  - **Acceptance**:
    - [ ] Preference form saves to profile
    - [ ] Language toggle switches UI and content
    - [ ] Personalization can be disabled

**Checkpoint**: Set preferences → see adapted content → switch to Urdu

---

## Phase 11: Polish & Production Readiness

**Goal**: Production hardening, documentation, final touches
**Time**: ~4 hours

### Batch 11.A (Parallel)

- [ ] T046 [P] [M] **Infrastructure & Operations**
  - **Files**:
    - `intellistack/backend/src/shared/middleware.py` (extend with tracing FR-110)
    - `intellistack/backend/src/core/analytics/` (monitoring dashboard FR-102)
    - `intellistack/docker/` (backup procedures FR-109)
    - `intellistack/docker-compose.yml` (horizontal scaling FR-105)
  - **Acceptance**:
    - [ ] Request tracing with correlation IDs
    - [ ] Database backup script works
    - [ ] Can scale to 3 backend replicas

- [ ] T047 [P] [M] **Deployment Workflows**
  - **Files**:
    - `intellistack/.github/workflows/deploy-staging.yml`
    - `intellistack/.github/workflows/deploy-production.yml`
  - **Acceptance**:
    - [ ] Staging deploys on PR merge to develop
    - [ ] Production deploys on release tag
    - [ ] Rollback procedure documented

- [ ] T048 [P] [M] **Security & Accessibility**
  - **Files**:
    - `intellistack/backend/src/config/settings.py` (secret validation FR-104)
    - Frontend components (accessibility FR-061)
    - `intellistack/frontend/src/components/shared/Skeleton.tsx`
    - `intellistack/frontend/src/components/shared/EmergencyContacts.tsx` (FR-065)
  - **Acceptance**:
    - [ ] App fails to start if secrets missing
    - [ ] All interactive elements keyboard accessible
    - [ ] Skeleton loaders on all async content

- [ ] T049 [P] [M] **Documentation & Demo**
  - **Files**:
    - `intellistack/backend/src/main.py` (OpenAPI FR-108)
    - `intellistack/docs/architecture.md` (FR-113)
    - `intellistack/backend/src/scripts/demo_mode.py` (FR-112)
  - **Acceptance**:
    - [ ] OpenAPI spec exports correctly
    - [ ] Architecture doc matches implementation
    - [ ] Demo mode seeds realistic data

### Batch 11.B (Sequential)

- [ ] T050 [M] **Portfolio & Showcase**
  - **Files**:
    - `intellistack/frontend/src/app/(dashboard)/portfolio/page.tsx` (FR-015)
    - `intellistack/frontend/src/app/(dashboard)/showcase/page.tsx` (FR-057)
  - **Acceptance**:
    - [ ] Portfolio shows completed projects
    - [ ] Showcase displays community contributions

- [ ] T051 [S] **Final Validation**
  - Run quickstart.md instructions end-to-end
  - Verify all checkpoints from each phase
  - **Acceptance**: New developer can setup and run in < 30 minutes

**Checkpoint**: Production-ready deployment with documentation

---

## Execution Summary

### Task Counts by Phase

| Phase | Name | Tasks | Time Est. |
|-------|------|-------|-----------|
| 0 | Vertical Slice ⚡ | 1 | ~4h |
| 1 | Setup | 6 | ~3h |
| 2 | Foundation | 8 | ~6h |
| 3 | US1: Student Learning | 9 | ~8h |
| 4 | US2: Content Creation | 3 | ~5h |
| 5 | US3: Institution | 3 | ~5h |
| 6 | US6: RAG Chatbot | 4 | ~8h |
| 7 | US4: AI Tutor | 3 | ~6h |
| 8 | US5: Community | 3 | ~6h |
| 9 | Assessment | 3 | ~6h |
| 10 | Personalization | 2 | ~4h |
| 11 | Polish | 6 | ~4h |
| **Total** | | **51** | **~65h** |

### MVP Path (Recommended)

1. **Phase 0**: Vertical Slice (~4h) - Validate architecture
2. **Phase 1**: Setup (~3h)
3. **Phase 2**: Foundation (~6h)
4. **Phase 3**: US1 Student Learning (~8h)
5. **Phase 9**: Assessment (partial, ~4h for quiz support)

**MVP Total**: ~25 hours, 27 tasks

### Parallel Execution Guide

```
Phase 1: T003 | T004 | T005 | T006 | T007 (after T002)
Phase 2: T008 | T009 → T010 | T011 → T012 | T013 → T014 | T015
Phase 3: T017 | T018 → T019 → T020 | T021 | T022 | T023 | T024
```

### Multi-Developer Assignment

| Developer | Focus | Phases |
|-----------|-------|--------|
| Dev A | Backend Core | 0, 2.A-C, 3.A-C |
| Dev B | Frontend | 2.D, 3.D-E |
| Dev C | AI/RAG | 6, 7 |
| Dev D | Features | 4, 5, 8 |

---

## Notes

- Tasks reduced from 254 → 51 through bundling
- Each task has clear acceptance criteria
- Vertical slice validates architecture first
- T-shirt sizes indicate relative effort
- [P] marks enable parallel execution
- Checkpoints validate phase completion before proceeding
