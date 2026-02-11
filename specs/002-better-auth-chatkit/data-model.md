# Data Model: Better-Auth OIDC Server + ChatKit AI Tutor

**Feature Branch**: `002-better-auth-chatkit`
**Date**: 2026-02-11

## Entity Relationship Overview

```
┌───────────────────────────────────────────────────────────────────────┐
│  BETTER-AUTH MANAGED (Node.js auth server owns these tables)          │
│                                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐    ┌────────────┐  │
│  │   user   │◄──▶│ session  │    │   account    │    │verification│  │
│  │          │◄──▶│          │    │ (OAuth link) │    │            │  │
│  │          │◄──▶│          │    │              │    │            │  │
│  └────┬─────┘    └──────────┘    └──────────────┘    └────────────┘  │
│       │                                                               │
│  ┌────┴─────────┐                                                     │
│  │  user_role   │ (custom extension via admin plugin)                 │
│  └──────────────┘                                                     │
└───────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│  CHATKIT MANAGED (FastAPI ChatKit server owns these tables)           │
│                                                                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐    │
│  │ chatkit_     │◄──▶│ chatkit_     │    │ chatkit_rate_limit   │    │
│  │ thread       │    │ thread_item  │    │                      │    │
│  └──────────────┘    └──────────────┘    └──────────────────────┘    │
└───────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│  EXISTING (unchanged, FastAPI manages)                                │
│                                                                       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐    │
│  │ rag_         │    │ learning_    │    │ content, institution │    │
│  │ conversation │    │ progress     │    │ assessment, etc.     │    │
│  └──────────────┘    └──────────────┘    └──────────────────────┘    │
└───────────────────────────────────────────────────────────────────────┘
```

## Better-Auth Tables (Managed by auth server)

### `user` (Better-Auth core)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Better-Auth generates UUIDs |
| name | VARCHAR(255) | NOT NULL | Display name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login identifier |
| email_verified | BOOLEAN | DEFAULT false | FR-002 |
| image | TEXT | NULLABLE | Avatar URL |
| role | VARCHAR(20) | DEFAULT 'student' | student/instructor/admin (FR-009) |
| created_at | TIMESTAMP | NOT NULL | Registration time |
| updated_at | TIMESTAMP | NOT NULL | Last modification |
| banned | BOOLEAN | DEFAULT false | Admin ban (admin plugin) |
| ban_reason | TEXT | NULLABLE | Reason for ban |
| ban_expires | TIMESTAMP | NULLABLE | Temp ban expiry |

### `session` (Better-Auth core)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Session identifier |
| user_id | VARCHAR(36) | FK → user.id | Session owner |
| token | TEXT | NOT NULL, UNIQUE | Session token (hashed) |
| expires_at | TIMESTAMP | NOT NULL | 7-day expiry (FR-011) |
| ip_address | VARCHAR(45) | NULLABLE | Client IP |
| user_agent | TEXT | NULLABLE | Browser info |
| created_at | TIMESTAMP | NOT NULL | Session start |
| updated_at | TIMESTAMP | NOT NULL | Last activity |

### `account` (Better-Auth core — OAuth links)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Link identifier |
| user_id | VARCHAR(36) | FK → user.id | Account owner |
| account_id | VARCHAR(255) | NOT NULL | Provider's user ID |
| provider_id | VARCHAR(255) | NOT NULL | 'google', 'github', 'credential' |
| access_token | TEXT | NULLABLE | Provider access token |
| refresh_token | TEXT | NULLABLE | Provider refresh token |
| access_token_expires_at | TIMESTAMP | NULLABLE | Token expiry |
| scope | TEXT | NULLABLE | Granted scopes |
| id_token | TEXT | NULLABLE | OIDC ID token |
| password | TEXT | NULLABLE | Hashed password (for credential provider) |
| created_at | TIMESTAMP | NOT NULL | Link creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

### `verification` (Better-Auth core — email verification + password reset)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Token identifier |
| identifier | VARCHAR(255) | NOT NULL | Email address |
| value | TEXT | NOT NULL | Token value |
| expires_at | TIMESTAMP | NOT NULL | 1 hour for password reset (FR-008) |
| created_at | TIMESTAMP | NOT NULL | Token creation |
| updated_at | TIMESTAMP | NOT NULL | Last update |

### `jwks` (Better-Auth JWT plugin)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Key identifier |
| public_key | TEXT | NOT NULL | RSA public key (PEM) |
| private_key | TEXT | NOT NULL | RSA private key (PEM, encrypted) |
| created_at | TIMESTAMP | NOT NULL | Key creation |

### `oauth_application` (Better-Auth OIDC Provider plugin)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Application identifier |
| client_id | VARCHAR(255) | UNIQUE, NOT NULL | OAuth client ID |
| client_secret | TEXT | NULLABLE | NULL for public clients |
| name | VARCHAR(255) | NOT NULL | Application name |
| redirect_uris | TEXT | NOT NULL | JSON array of URIs |
| type | VARCHAR(20) | NOT NULL | 'public' or 'confidential' |
| disabled | BOOLEAN | DEFAULT false | Application status |
| icon | TEXT | NULLABLE | Application icon URL |
| metadata | TEXT | NULLABLE | JSON metadata |
| created_at | TIMESTAMP | NOT NULL | Registration time |
| updated_at | TIMESTAMP | NOT NULL | Last update |

### `auth_event_log` (Custom — FR-028)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | Event identifier |
| event_type | VARCHAR(50) | NOT NULL | login_success, login_failed, register, logout, password_reset, oauth_link, oauth_unlink |
| user_id | VARCHAR(36) | FK → user.id, NULLABLE | NULL for failed login with unknown email |
| email | VARCHAR(255) | NULLABLE | Attempted email |
| ip_address | VARCHAR(45) | NOT NULL | Client IP |
| user_agent | TEXT | NULLABLE | Browser info |
| details | JSONB | NULLABLE | Additional context (failure reason, provider) |
| created_at | TIMESTAMP | NOT NULL, INDEX | Event time |

## ChatKit Tables (Managed by FastAPI)

### `chatkit_thread`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Thread identifier |
| user_id | VARCHAR(36) | NOT NULL, INDEX | Thread owner (references Better-Auth user.id) |
| title | VARCHAR(255) | NULLABLE | Auto-generated or user-set |
| course_id | UUID | FK → content.id, NULLABLE | Associated course |
| lesson_stage | INTEGER | NULLABLE | Learning stage at creation |
| status | VARCHAR(20) | DEFAULT 'active' | active, archived, deleted |
| metadata | JSONB | NULLABLE | Additional context |
| created_at | TIMESTAMP | NOT NULL | Thread creation |
| updated_at | TIMESTAMP | NOT NULL, INDEX | Last activity (for ordering) |
| enrollment_ended_at | TIMESTAMP | NULLABLE | When student left/completed course |

**Indexes**: `(user_id, updated_at DESC)` for thread listing, `(enrollment_ended_at)` for retention cleanup.

**Retention**: Cron job deletes threads where `enrollment_ended_at + 30 days < NOW()`.

### `chatkit_thread_item`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | VARCHAR(36) | PK | Item identifier |
| thread_id | VARCHAR(36) | FK → chatkit_thread.id | Parent thread |
| type | VARCHAR(20) | NOT NULL | 'message', 'tool_call', 'tool_result', 'widget' |
| role | VARCHAR(20) | NOT NULL | 'user', 'assistant', 'system' |
| content | TEXT | NOT NULL | Message text or JSON |
| metadata | JSONB | NULLABLE | Page context, selected text, model info |
| created_at | TIMESTAMP | NOT NULL, INDEX | Message time |

**Indexes**: `(thread_id, created_at ASC)` for message loading.

### `chatkit_rate_limit`

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | Record identifier |
| user_id | VARCHAR(36) | NOT NULL | Student user ID |
| message_count | INTEGER | DEFAULT 0 | Messages in current window |
| window_start | TIMESTAMP | NOT NULL | Rolling 24h window start |
| updated_at | TIMESTAMP | NOT NULL | Last message time |

**Indexes**: `(user_id, window_start)` for rate limit checks.

### `ai_usage_metric` (FR-029)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | Metric identifier |
| user_id | VARCHAR(36) | NOT NULL, INDEX | User |
| date | DATE | NOT NULL | Metric date |
| message_count | INTEGER | DEFAULT 0 | Messages sent that day |
| total_response_time_ms | BIGINT | DEFAULT 0 | Sum of response times |
| error_count | INTEGER | DEFAULT 0 | Errors that day |
| created_at | TIMESTAMP | NOT NULL | Record creation |

**Indexes**: `(user_id, date)` UNIQUE for daily aggregation.

## State Transitions

### User Email Verification
```
unverified → (click email link) → verified
  ↓ access: browse dashboard, course listings
  ↓ verified: full access to lessons, AI tutor
```

### Account Lockout (FR-007)
```
normal → (5 failed attempts) → locked_30min → (cooldown expires) → normal
```

### Thread Lifecycle (FR-018)
```
active → (student completes/leaves course) → enrollment_ended_at set
  → (30 days pass) → deleted by retention cron
```

### OAuth Account Linking
```
email_only → (OAuth with same email) → email + OAuth linked
OAuth_only → (set password) → OAuth + credential
```

## Migration Mapping (Old → Better-Auth)

| Old Table | Better-Auth Table | Notes |
|-----------|-------------------|-------|
| user (existing) | user | Map id, email, name, image, email_verified; preserve UUIDs |
| user.password_hash | account (provider_id='credential') | Move password hash to account.password |
| oauth_account | account | Map provider → provider_id, provider_account_id → account_id |
| session | session | Recreate active sessions; expired ones can be dropped |
| user_role | user.role field | Flatten to single role string (student/instructor/admin) |
| password_reset_token | verification | Map to verification table format |
| login_attempt | auth_event_log | Historical data migration |
