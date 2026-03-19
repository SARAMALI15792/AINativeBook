# Data Model: IntelliStack Platform

**Branch**: `001-intellistack-platform` | **Date**: 2026-02-07

## Overview

This document defines the core entities, their attributes, relationships, and validation rules derived from the feature specification and constitution requirements.

---

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              INTELLISTACK DATA MODEL                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────┐      ┌──────────────┐      ┌─────────────┐                        │
│  │   User   │──────│   UserRole   │──────│    Role     │                        │
│  └────┬─────┘      └──────────────┘      └─────────────┘                        │
│       │                                                                          │
│       │ 1:1                                                                      │
│       ▼                                                                          │
│  ┌──────────┐      ┌──────────────┐      ┌─────────────┐                        │
│  │ Progress │──────│  UserBadge   │──────│   Badge     │                        │
│  └────┬─────┘      └──────────────┘      └─────────────┘                        │
│       │                                                                          │
│       │ 1:N                                                                      │
│       ▼                                                                          │
│  ┌──────────────┐      ┌──────────────┐      ┌─────────────┐                    │
│  │  Submission  │──────│  Assessment  │──────│    Stage    │                    │
│  └──────────────┘      └──────────────┘      └──────┬──────┘                    │
│                                                      │                           │
│                                                      │ 1:N                       │
│                                                      ▼                           │
│  ┌──────────────┐                           ┌─────────────┐                     │
│  │ContentVersion│───────────────────────────│   Content   │                     │
│  └──────────────┘                           └──────┬──────┘                     │
│                                                    │                             │
│                                                    │ 1:N (embeddings)            │
│                                                    ▼                             │
│  ┌──────────────┐      ┌──────────────┐    ┌─────────────┐                      │
│  │ RAGContext   │──────│ RAGRetrieval │────│ContentChunk │ (Qdrant)             │
│  └──────────────┘      └──────────────┘    └─────────────┘                      │
│                                                                                  │
│  ┌──────────────┐      ┌──────────────┐    ┌─────────────┐                      │
│  │AIConversation│──────│  AIMessage   │────│  AITutor    │                      │
│  └──────────────┘      └──────────────┘    │  Guardrails │                      │
│                                            └─────────────┘                      │
│                                                                                  │
│  ┌──────────────┐      ┌──────────────┐    ┌─────────────┐                      │
│  │ Institution  │──────│    Cohort    │────│   Cohort    │                      │
│  └──────────────┘      └──────────────┘    │  Enrollment │                      │
│                                            └─────────────┘                      │
│                                                                                  │
│  ┌──────────────┐      ┌──────────────┐    ┌─────────────┐                      │
│  │ForumCategory │──────│ ForumThread  │────│  ForumPost  │                      │
│  └──────────────┘      └──────────────┘    └─────────────┘                      │
│                                                                                  │
│  ┌──────────────┐      ┌──────────────┐                                         │
│  │  StudyGroup  │──────│StudyGroup    │                                         │
│  └──────────────┘      │   Member     │                                         │
│                        └──────────────┘                                         │
│                                                                                  │
│  ┌──────────────┐                                                               │
│  │  Mentorship  │ (mentor_id ↔ mentee_id)                                       │
│  └──────────────┘                                                               │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Entities

### 1. User

Represents any person interacting with IntelliStack.

**Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| name | VARCHAR(255) | NOT NULL | Display name |
| avatar_url | VARCHAR(500) | NULL | Profile image URL |
| bio | TEXT | NULL | User biography |
| learning_style | ENUM | NULL | preferred_video, preferred_text, preferred_interactive |
| notification_settings | JSONB | DEFAULT '{}' | Notification preferences |
| locale | VARCHAR(10) | DEFAULT 'en' | Preferred language |
| created_at | TIMESTAMP | NOT NULL | Account creation time |
| updated_at | TIMESTAMP | NOT NULL | Last modification |
| deleted_at | TIMESTAMP | NULL | Soft delete (30-day recovery) |

**Relationships**:
- Has many `UserRole` (many-to-many with Role)
- Has one `Progress` (as Student)
- Has many `AIConversation`
- Has many `Submission`
- Belongs to many `Institution` (through `InstitutionMember`)
- Belongs to many `Cohort` (through `CohortEnrollment`)

**Validation Rules**:
- Email must be valid format
- Name: 2-100 characters
- Soft delete: data purged after 30 days (FR-090)

---

### 2. Role

System roles for access control.

**Table**: `roles`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Role name |
| description | TEXT | NULL | Role description |
| permissions | JSONB | NOT NULL | Permission set |

**Predefined Roles** (FR-036):
- `student` - Learning access, community participation
- `author` - Content creation, review participation
- `instructor` - Cohort management, assessment grading
- `institution_admin` - Institution management, analytics
- `platform_admin` - Full system access

---

### 3. UserRole

Join table for user-role assignment.

**Table**: `user_roles`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users | User reference |
| role_id | UUID | FK → roles | Role reference |
| granted_by | UUID | FK → users | Admin who granted |
| granted_at | TIMESTAMP | NOT NULL | Grant timestamp |
| revoked_at | TIMESTAMP | NULL | Revocation timestamp |

**Validation Rules**:
- User may have multiple roles (FR-038)
- Audit trail required (FR-040)

---

### 4. Stage

Course stage definition (5 stages mapping to constitution's 9 stages).

**Table**: `stages`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| number | INTEGER | UNIQUE, NOT NULL | Stage number (1-5) |
| name | VARCHAR(100) | NOT NULL | Stage name |
| description | TEXT | NOT NULL | Stage description |
| constitution_stages | INTEGER[] | NOT NULL | Mapped constitution stages |
| learning_objectives | JSONB | NOT NULL | Stage objectives |
| estimated_hours | INTEGER | NOT NULL | Estimated completion time |
| badge_id | UUID | FK → badges | Completion badge |
| prerequisite_stage_id | UUID | FK → stages | Required prior stage |

**Stage Mapping** (from spec):
| Course Stage | Constitution Stages | Focus |
|--------------|---------------------|-------|
| 1 | 0-1 | Foundations: Python, Linux, Math |
| 2 | 2-3 | ROS 2 Basics, Gazebo, Isaac Sim |
| 3 | 4-5 | Perception & Planning |
| 4 | 6-7 | AI Integration, Sim-to-Real |
| 5 | 8 | Capstone |

---

### 5. Content

Learning materials (lessons, exercises, simulations).

**Table**: `content`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| stage_id | UUID | FK → stages, NOT NULL | Stage assignment |
| content_type | ENUM | NOT NULL | lesson, exercise, simulation, resource |
| title | VARCHAR(255) | NOT NULL | Content title |
| description | TEXT | NULL | Content description |
| learning_objectives | UUID[] | NOT NULL | Objectives addressed |
| order_index | INTEGER | NOT NULL | Display order within stage |
| format_variants | JSONB | DEFAULT '[]' | Available formats |
| mdx_path | VARCHAR(500) | NOT NULL | Path to MDX file |
| current_version_id | UUID | FK → content_versions | Active version |
| review_status | ENUM | NOT NULL | draft, in_review, published, archived |
| created_by | UUID | FK → users | Author |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update |
| published_at | TIMESTAMP | NULL | Publication time |

**Content Types**:
- `lesson` - Instructional content
- `exercise` - Practice problems
- `simulation` - Embedded simulation exercises
- `resource` - Supplementary materials

---

### 6. ContentVersion

Version history for content.

**Table**: `content_versions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| content_id | UUID | FK → content, NOT NULL | Parent content |
| version | VARCHAR(20) | NOT NULL | Semantic version |
| mdx_content_hash | VARCHAR(64) | NOT NULL | SHA-256 of MDX content |
| change_summary | TEXT | NOT NULL | What changed |
| created_by | UUID | FK → users | Editor |
| created_at | TIMESTAMP | NOT NULL | Version creation time |
| reviewed_by | UUID | FK → users | Reviewer (if approved) |
| reviewed_at | TIMESTAMP | NULL | Review timestamp |

---

### 7. ContentChunk (Qdrant Vector Collection)

Vector embeddings for RAG retrieval.

**Qdrant Collection**: `textbook_content`

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Chunk identifier |
| content_id | UUID | Source content reference |
| stage_id | UUID | Stage for access control |
| chapter | VARCHAR(100) | Chapter reference |
| section | VARCHAR(100) | Section reference |
| paragraph_index | INTEGER | Paragraph number |
| text | TEXT | Chunk text |
| code_language | VARCHAR(50) | If code block, the language |
| embedding | VECTOR(1536) | OpenAI ada-002 embedding |

**Chunking Strategy**:
- 512 tokens per chunk
- 50 token overlap
- Preserve code blocks as single chunks
- Metadata includes citation path

---

### 8. Progress

Student's advancement through curriculum.

**Table**: `progress`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, UNIQUE, NOT NULL | Student reference |
| current_stage_id | UUID | FK → stages | Current stage |
| challenge_pathway_used | BOOLEAN | DEFAULT false | Used challenge pathway |
| stages_skipped | INTEGER[] | DEFAULT '[]' | Skipped stage numbers |
| total_time_on_task | INTEGER | DEFAULT 0 | Total seconds |
| started_at | TIMESTAMP | NOT NULL | Learning start date |
| certificate_id | UUID | FK → certificates | If completed |

---

### 9. ContentCompletion

Tracks completion of individual content items.

**Table**: `content_completions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| progress_id | UUID | FK → progress, NOT NULL | Progress reference |
| content_id | UUID | FK → content, NOT NULL | Content reference |
| completed_at | TIMESTAMP | NOT NULL | Completion time |
| time_spent | INTEGER | NOT NULL | Seconds spent |

**Constraint**: UNIQUE (progress_id, content_id)

---

### 10. Assessment

Evaluation instruments.

**Table**: `assessments`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| stage_id | UUID | FK → stages, NOT NULL | Stage assignment |
| assessment_type | ENUM | NOT NULL | quiz, project, peer_review, demonstration, safety_assessment |
| title | VARCHAR(255) | NOT NULL | Assessment title |
| instructions | TEXT | NOT NULL | Instructions |
| rubric | JSONB | NOT NULL | Rubric criteria and weights |
| learning_objectives | UUID[] | NOT NULL | Objectives assessed |
| passing_threshold | DECIMAL(5,2) | DEFAULT 70.00 | Pass percentage |
| max_attempts | INTEGER | DEFAULT 3 | Attempt limit |
| cooldown_hours | INTEGER | DEFAULT 24 | Hours between attempts |
| time_limit_minutes | INTEGER | NULL | Time limit if timed |
| is_safety_required | BOOLEAN | DEFAULT false | Gates hardware access |

**Assessment Types**:
- `quiz` - Multiple choice, short answer
- `project` - Practical demonstration
- `peer_review` - Review of peer work
- `demonstration` - Live/recorded demonstration
- `safety_assessment` - 10-item safety check (FR-052)

---

### 11. Submission

Student assessment submissions.

**Table**: `submissions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | Student |
| assessment_id | UUID | FK → assessments, NOT NULL | Assessment |
| attempt_number | INTEGER | NOT NULL | Attempt # |
| submission_data | JSONB | NOT NULL | Answers/artifacts |
| auto_score | DECIMAL(5,2) | NULL | Automated portion |
| manual_score | DECIMAL(5,2) | NULL | Human-reviewed portion |
| final_score | DECIMAL(5,2) | NULL | Combined score |
| feedback | TEXT | NULL | Feedback text |
| similarity_score | DECIMAL(5,2) | NULL | Plagiarism check result |
| flagged_for_review | BOOLEAN | DEFAULT false | Needs instructor review |
| status | ENUM | NOT NULL | pending, graded, flagged |
| submitted_at | TIMESTAMP | NOT NULL | Submission time |
| graded_at | TIMESTAMP | NULL | Grading completion |
| graded_by | UUID | FK → users | Grader (if manual) |

---

### 12. Badge

Digital achievement badges.

**Table**: `badges`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(100) | NOT NULL | Badge name |
| description | TEXT | NOT NULL | What it represents |
| image_url | VARCHAR(500) | NOT NULL | Badge image |
| criteria | JSONB | NOT NULL | Earning criteria |
| stage_id | UUID | FK → stages | Associated stage (if stage badge) |

---

### 13. UserBadge

Earned badges.

**Table**: `user_badges`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | Badge holder |
| badge_id | UUID | FK → badges, NOT NULL | Badge |
| earned_at | TIMESTAMP | NOT NULL | When earned |
| verification_hash | VARCHAR(64) | NOT NULL | Verification code |

**Constraint**: UNIQUE (user_id, badge_id)

---

### 14. Certificate

Capstone completion certificates.

**Table**: `certificates`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | Certificate holder |
| issued_at | TIMESTAMP | NOT NULL | Issue date |
| verification_code | VARCHAR(64) | UNIQUE, NOT NULL | Public verification |
| capstone_submission_id | UUID | FK → submissions | Capstone project |
| portfolio_url | VARCHAR(500) | NULL | Portfolio link |

---

### 15. AIConversation

AI tutor/RAG conversation sessions.

**Table**: `ai_conversations`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | User |
| conversation_type | ENUM | NOT NULL | tutor, rag_chatbot |
| context_content_id | UUID | FK → content | If context-specific |
| started_at | TIMESTAMP | NOT NULL | Session start |
| ended_at | TIMESTAMP | NULL | Session end |
| guardrail_attempts | INTEGER | DEFAULT 0 | Direct answer attempts |
| escalated_at | TIMESTAMP | NULL | If escalated to instructor |

**Retention**: 30 days (FR-033), then purged

---

### 16. AIMessage

Individual messages in AI conversations.

**Table**: `ai_messages`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| conversation_id | UUID | FK → ai_conversations, NOT NULL | Conversation |
| role | ENUM | NOT NULL | user, assistant, system |
| content | TEXT | NOT NULL | Message content |
| citations | JSONB | NULL | RAG citations if applicable |
| token_usage | JSONB | NULL | Token consumption |
| created_at | TIMESTAMP | NOT NULL | Message time |

---

### 17. RAGRetrieval

Retrieved passages for RAG answers.

**Table**: `rag_retrievals`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| message_id | UUID | FK → ai_messages, NOT NULL | Associated answer |
| chunk_id | UUID | NOT NULL | Qdrant chunk reference |
| content_id | UUID | FK → content | Source content |
| relevance_score | DECIMAL(5,4) | NOT NULL | Retrieval score |
| citation_text | TEXT | NOT NULL | Excerpt used |
| chapter | VARCHAR(100) | NOT NULL | Citation chapter |
| section | VARCHAR(100) | NOT NULL | Citation section |

---

### 18. Institution

Organizations using IntelliStack.

**Table**: `institutions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Institution name |
| logo_url | VARCHAR(500) | NULL | Branding logo |
| primary_color | VARCHAR(7) | DEFAULT '#000000' | Brand color |
| welcome_message | TEXT | NULL | Custom welcome |
| webhook_url | VARCHAR(500) | NULL | Event notification URL |
| simulation_quota_hours | INTEGER | DEFAULT 25 | Custom quota (if negotiated) |
| created_at | TIMESTAMP | NOT NULL | Registration time |

---

### 19. InstitutionMember

User-Institution association.

**Table**: `institution_members`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| institution_id | UUID | FK → institutions, NOT NULL | Institution |
| user_id | UUID | FK → users, NOT NULL | Member |
| role | ENUM | NOT NULL | admin, instructor, student |
| joined_at | TIMESTAMP | NOT NULL | Membership start |

---

### 20. Cohort

Learning cohorts within institutions.

**Table**: `cohorts`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| institution_id | UUID | FK → institutions, NOT NULL | Parent institution |
| name | VARCHAR(255) | NOT NULL | Cohort name (e.g., "Spring 2026") |
| start_date | DATE | NOT NULL | Cohort start |
| end_date | DATE | NOT NULL | Cohort end |
| enrollment_limit | INTEGER | NULL | Max students |
| created_by | UUID | FK → users | Creator |
| created_at | TIMESTAMP | NOT NULL | Creation time |

---

### 21. CohortEnrollment

Student enrollment in cohorts.

**Table**: `cohort_enrollments`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| cohort_id | UUID | FK → cohorts, NOT NULL | Cohort |
| user_id | UUID | FK → users, NOT NULL | Student |
| enrolled_at | TIMESTAMP | NOT NULL | Enrollment time |
| enrolled_by | UUID | FK → users | Admin who enrolled |

**Constraint**: UNIQUE (cohort_id, user_id)

---

### 22. CohortInstructor

Instructor assignment to cohorts.

**Table**: `cohort_instructors`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| cohort_id | UUID | FK → cohorts, NOT NULL | Cohort |
| user_id | UUID | FK → users, NOT NULL | Instructor |
| assigned_at | TIMESTAMP | NOT NULL | Assignment time |

---

### 23. ForumCategory

Forum organization by stage/topic.

**Table**: `forum_categories`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| stage_id | UUID | FK → stages | Stage-specific (NULL = general) |
| name | VARCHAR(100) | NOT NULL | Category name |
| description | TEXT | NULL | Category description |
| order_index | INTEGER | NOT NULL | Display order |

---

### 24. ForumThread

Discussion threads.

**Table**: `forum_threads`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| category_id | UUID | FK → forum_categories, NOT NULL | Parent category |
| title | VARCHAR(255) | NOT NULL | Thread title |
| created_by | UUID | FK → users, NOT NULL | Thread author |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| is_pinned | BOOLEAN | DEFAULT false | Pinned thread |
| is_locked | BOOLEAN | DEFAULT false | Locked (no new posts) |
| last_post_at | TIMESTAMP | NOT NULL | Last activity |

---

### 25. ForumPost

Posts within threads.

**Table**: `forum_posts`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| thread_id | UUID | FK → forum_threads, NOT NULL | Parent thread |
| parent_post_id | UUID | FK → forum_posts | Reply-to (threading) |
| content | TEXT | NOT NULL | Post content |
| created_by | UUID | FK → users, NOT NULL | Author |
| created_at | TIMESTAMP | NOT NULL | Post time |
| edited_at | TIMESTAMP | NULL | Last edit |
| is_moderated | BOOLEAN | DEFAULT false | Hidden by moderator |

---

### 26. StudyGroup

Self-organized study groups.

**Table**: `study_groups`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Group name |
| description | TEXT | NULL | Group description |
| created_by | UUID | FK → users, NOT NULL | Organizer |
| created_at | TIMESTAMP | NOT NULL | Creation time |
| is_public | BOOLEAN | DEFAULT true | Discoverable |

---

### 27. StudyGroupMember

Membership in study groups.

**Table**: `study_group_members`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| study_group_id | UUID | FK → study_groups, NOT NULL | Group |
| user_id | UUID | FK → users, NOT NULL | Member |
| role | ENUM | DEFAULT 'member' | organizer, member |
| joined_at | TIMESTAMP | NOT NULL | Join time |

---

### 28. Mentorship

Mentor-mentee pairings.

**Table**: `mentorships`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| mentor_id | UUID | FK → users, NOT NULL | Mentor (Stage 5+) |
| mentee_id | UUID | FK → users, NOT NULL | Mentee |
| status | ENUM | NOT NULL | pending, active, completed, declined |
| matched_at | TIMESTAMP | NOT NULL | Match proposal time |
| accepted_at | TIMESTAMP | NULL | Acceptance time |
| completed_at | TIMESTAMP | NULL | Completion time |

**Validation**:
- Mentor must have completed Stage 5 (Capstone)
- Both parties must accept (Assumption #10)

---

### 29. SimulationQuota

Track simulation usage per user.

**Table**: `simulation_quotas`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | User |
| billing_period_start | DATE | NOT NULL | Period start |
| billing_period_end | DATE | NOT NULL | Period end |
| quota_hours | DECIMAL(6,2) | NOT NULL | Allocated hours |
| used_hours | DECIMAL(6,2) | DEFAULT 0 | Used hours |
| notified_80pct | BOOLEAN | DEFAULT false | 80% notification sent |
| notified_95pct | BOOLEAN | DEFAULT false | 95% notification sent |

**Default Quota**: 25 hours/month (FR-019)

---

### 30. SimulationState

Saved simulation states.

**Table**: `simulation_states`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | Owner |
| content_id | UUID | FK → content, NOT NULL | Related exercise |
| name | VARCHAR(255) | NOT NULL | State name |
| state_data | JSONB | NOT NULL | Serialized state |
| is_shared | BOOLEAN | DEFAULT false | Shareable (FR-022) |
| created_at | TIMESTAMP | NOT NULL | Save time |

---

### 31. WebhookEvent

Outbound event notifications for institutions.

**Table**: `webhook_events`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| institution_id | UUID | FK → institutions, NOT NULL | Target institution |
| event_type | VARCHAR(50) | NOT NULL | enrollment, progress, completion |
| payload | JSONB | NOT NULL | Event data |
| status | ENUM | NOT NULL | pending, delivered, failed |
| attempts | INTEGER | DEFAULT 0 | Delivery attempts |
| last_attempt_at | TIMESTAMP | NULL | Last try |
| delivered_at | TIMESTAMP | NULL | Success time |
| created_at | TIMESTAMP | NOT NULL | Event time |

---

### 32. AuditLog

Administrative action audit trail.

**Table**: `audit_logs`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique identifier |
| user_id | UUID | FK → users, NOT NULL | Actor |
| action | VARCHAR(100) | NOT NULL | Action performed |
| resource_type | VARCHAR(50) | NOT NULL | Entity type |
| resource_id | UUID | NOT NULL | Entity ID |
| changes | JSONB | NULL | Before/after data |
| ip_address | VARCHAR(45) | NULL | Client IP |
| created_at | TIMESTAMP | NOT NULL | Action time |

---

## Indexes

### Performance-Critical Indexes

```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;

-- Progress queries
CREATE INDEX idx_progress_user ON progress(user_id);
CREATE INDEX idx_content_completions_progress ON content_completions(progress_id);

-- Content by stage
CREATE INDEX idx_content_stage ON content(stage_id, order_index) WHERE review_status = 'published';

-- Submissions
CREATE INDEX idx_submissions_user_assessment ON submissions(user_id, assessment_id);
CREATE INDEX idx_submissions_flagged ON submissions(flagged_for_review) WHERE flagged_for_review = true;

-- AI conversations (retention)
CREATE INDEX idx_ai_conversations_created ON ai_conversations(created_at);
CREATE INDEX idx_ai_messages_conversation ON ai_messages(conversation_id);

-- Forum activity
CREATE INDEX idx_forum_threads_category ON forum_threads(category_id, last_post_at DESC);
CREATE INDEX idx_forum_posts_thread ON forum_posts(thread_id, created_at);

-- Institution/Cohort
CREATE INDEX idx_cohort_enrollments_cohort ON cohort_enrollments(cohort_id);
CREATE INDEX idx_cohort_enrollments_user ON cohort_enrollments(user_id);

-- Webhook delivery
CREATE INDEX idx_webhook_events_pending ON webhook_events(status, institution_id) WHERE status = 'pending';
```

---

## State Machines

### Content Review Status

```
draft → in_review → published → archived
         ↓                ↑
       rejected ──────────┘ (with revisions)
```

### Submission Status

```
pending → graded
    ↓
 flagged → graded (after review)
```

### Mentorship Status

```
pending → active → completed
    ↓
 declined
```

---

## Validation Summary

| Entity | Key Validations |
|--------|-----------------|
| User | Email format, soft delete policy |
| Progress | One per user, stages_skipped max 3 consecutive |
| Submission | Max attempts enforced, cooldown checked |
| AIConversation | 30-day retention limit |
| SimulationQuota | Default 25 hrs/month |
| Badge | Unique per user |
| Mentorship | Mentor must be Stage 5+, both accept |

---

*Data model completed: 2026-02-07*
