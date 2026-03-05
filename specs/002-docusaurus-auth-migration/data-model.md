# Data Model: Docusaurus Authentication Migration & Onboarding

**Feature**: 002-docusaurus-auth-migration
**Date**: 2026-02-25
**Phase**: 1 - Data Model Design

---

## Overview

This document defines the data model for authentication, session management, and onboarding in the IntelliStack platform. The model supports Better Auth integration, multi-step onboarding, and user profile management.

---

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
│─────────────────│
│ id (PK)         │
│ email (unique)  │
│ password_hash   │
│ name            │
│ email_verified  │
│ onboarding_     │
│   completed     │
│ current_stage   │
│ role            │
│ preferences     │◄────┐
│ created_at      │     │
│ updated_at      │     │
└────────┬────────┘     │
         │              │
         │ 1:N          │
         │              │
┌────────▼────────┐     │
│    Session      │     │
│─────────────────│     │
│ id (PK)         │     │
│ user_id (FK)    │     │
│ token (indexed) │     │
│ expires_at      │     │
│ created_at      │     │
│ revoked_at      │     │
│ user_agent      │     │
│ ip_address      │     │
└─────────────────┘     │
                        │
         │ 1:N          │
         │              │
┌────────▼────────┐     │
│  OAuth Account  │     │
│─────────────────│     │
│ id (PK)         │     │
│ user_id (FK)    │     │
│ provider        │     │
│ provider_       │     │
│   account_id    │     │
│ access_token    │     │
│ refresh_token   │     │
│ expires_at      │     │
│ created_at      │     │
└─────────────────┘     │
                        │
                        │
         Onboarding Data│
         (JSON in       │
          preferences)──┘
```

---

## Entities

### 1. User

**Purpose**: Represents a platform user with authentication credentials, profile information, onboarding status, and learning progress.

**Table**: `users`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | string (255) | PRIMARY KEY | Unique user identifier (UUID) |
| email | string (255) | UNIQUE, NOT NULL, INDEXED | User email address |
| password_hash | string (255) | NOT NULL | Bcrypt hashed password |
| name | string (255) | NOT NULL | User full name |
| email_verified | boolean | DEFAULT false | Email verification status |
| onboarding_completed | boolean | DEFAULT false, INDEXED | Onboarding completion flag |
| current_stage | integer | DEFAULT 1 | Learning stage (1-5) |
| role | string (50) | DEFAULT 'student' | User role (student/instructor/admin) |
| preferences | JSON | NULLABLE | Onboarding data and user preferences |
| avatar_url | string (500) | NULLABLE | Profile picture URL |
| bio | text | NULLABLE | User biography |
| locale | string (10) | DEFAULT 'en' | Preferred language |
| is_active | boolean | DEFAULT true | Account active status |
| created_at | timestamp | NOT NULL, DEFAULT now() | Account creation timestamp |
| updated_at | timestamp | NOT NULL, DEFAULT now() | Last update timestamp |
| deleted_at | timestamp | NULLABLE, INDEXED | Soft delete timestamp |

**Indexes**:
- PRIMARY KEY: `id`
- UNIQUE: `email`
- INDEX: `onboarding_completed`
- INDEX: `current_stage`
- INDEX: `deleted_at`

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password must be at least 8 characters (enforced before hashing)
- Name must not be empty
- Current stage must be between 1 and 5
- Role must be one of: 'student', 'instructor', 'admin'
- Preferences must be valid JSON if not null

**State Transitions**:
```
[Created] → email_verified=false, onboarding_completed=false
    ↓
[Email Verified] → email_verified=true (optional in dev)
    ↓
[Onboarding Step 1] → preferences.basic_info populated
    ↓
[Onboarding Step 2] → preferences.education populated
    ↓
[Onboarding Step 3] → preferences.interests populated
    ↓
[Onboarding Step 4] → preferences.additional populated
    ↓
[Onboarding Complete] → onboarding_completed=true
    ↓
[Active Learner] → current_stage increments as stages unlock
```

**Relationships**:
- One-to-many with Session (user can have multiple active sessions)
- One-to-many with OAuth Account (user can link multiple providers)
- One-to-one with Onboarding Data (stored in preferences JSON)

---

### 2. Session

**Purpose**: Represents an authenticated user session with token, expiration, and device information.

**Table**: `sessions`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | string (255) | PRIMARY KEY | Unique session identifier (UUID) |
| user_id | string (255) | FOREIGN KEY (users.id), NOT NULL, INDEXED | Reference to user |
| token | string (1000) | NOT NULL, INDEXED | Session token (JWT or opaque) |
| expires_at | timestamp | NOT NULL | Session expiration timestamp |
| created_at | timestamp | NOT NULL, DEFAULT now() | Session creation timestamp |
| revoked_at | timestamp | NULLABLE | Session revocation timestamp |
| user_agent | string (500) | NULLABLE | Browser/device user agent |
| ip_address | string (45) | NULLABLE | Client IP address (IPv4/IPv6) |

**Indexes**:
- PRIMARY KEY: `id`
- INDEX: `user_id`
- INDEX: `token`
- INDEX: `expires_at` (for cleanup queries)

**Validation Rules**:
- Token must not be empty
- Expires_at must be in the future at creation
- User_id must reference existing user
- IP address must be valid IPv4 or IPv6 format if provided

**State Transitions**:
```
[Created] → revoked_at=null, expires_at=now()+24h
    ↓
[Active] → Used for authentication
    ↓
[Expired] → expires_at < now()
    OR
[Revoked] → revoked_at set (logout)
```

**Lifecycle**:
- Created on successful login
- Expires after 24 hours of inactivity
- Refreshed after 1 hour of activity (updates expires_at)
- Revoked on explicit logout
- Cleaned up periodically (delete expired sessions)

**Relationships**:
- Many-to-one with User (session belongs to one user)

---

### 3. OAuth Account

**Purpose**: Represents a linked social authentication provider account (Google, GitHub, etc.).

**Table**: `oauth_accounts`

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | string (255) | PRIMARY KEY | Unique OAuth account identifier (UUID) |
| user_id | string (255) | FOREIGN KEY (users.id), NOT NULL, INDEXED | Reference to user |
| provider | string (50) | NOT NULL, INDEXED | OAuth provider (google/github) |
| provider_account_id | string (255) | NOT NULL, INDEXED | Provider's user ID |
| access_token | text | NULLABLE | OAuth access token (encrypted) |
| refresh_token | text | NULLABLE | OAuth refresh token (encrypted) |
| expires_at | timestamp | NULLABLE | Token expiration timestamp |
| token_type | string (50) | NULLABLE | Token type (Bearer) |
| scope | string (500) | NULLABLE | Granted OAuth scopes |
| id_token | text | NULLABLE | OpenID Connect ID token |
| created_at | timestamp | NOT NULL, DEFAULT now() | Account linking timestamp |
| updated_at | timestamp | NOT NULL, DEFAULT now() | Last token refresh timestamp |

**Indexes**:
- PRIMARY KEY: `id`
- INDEX: `user_id`
- INDEX: `provider`
- UNIQUE: `(provider, provider_account_id)` (prevent duplicate links)

**Validation Rules**:
- Provider must be one of: 'google', 'github'
- Provider_account_id must not be empty
- User_id must reference existing user
- Access_token should be encrypted at rest

**State Transitions**:
```
[Linked] → OAuth account created and linked to user
    ↓
[Active] → Tokens valid, can be used for API calls
    ↓
[Expired] → expires_at < now(), needs refresh
    ↓
[Refreshed] → New access_token obtained, expires_at updated
    OR
[Unlinked] → Record deleted (user unlinks provider)
```

**Account Linking Logic**:
- If user signs up with email, then logs in with Google (same email):
  - System automatically links OAuth account to existing user
  - Requires email_verified=true for security
- If user signs up with Google first:
  - New user created with email from Google profile
  - OAuth account linked immediately
  - email_verified set to true (trusted provider)

**Relationships**:
- Many-to-one with User (OAuth account belongs to one user)

---

### 4. Onboarding Data (JSON Structure)

**Purpose**: Stores user onboarding responses in a flexible JSON structure within users.preferences field.

**Storage**: `users.preferences` (JSONB column)

**Schema**:

```typescript
interface OnboardingPreferences {
  basic_info: {
    full_name: string;              // User's full name
    preferred_language: 'en' | 'ur'; // English or Urdu
    timezone: string;                // IANA timezone (e.g., 'America/New_York')
  };
  education: {
    level: 'high_school' | 'undergraduate' | 'graduate' | 'professional';
    field_of_study: string;          // Free text (e.g., 'Computer Science')
    prior_experience: 'none' | 'beginner' | 'intermediate' | 'advanced';
  };
  interests: {
    learning_goals: Array<           // Multi-select
      'career_change' |
      'academic_research' |
      'hobby' |
      'professional_development'
    >;
    learning_style: 'visual' | 'reading' | 'hands_on' | 'mixed';
    topics_of_interest: Array<       // Multi-select
      'ros2' |
      'simulation' |
      'perception' |
      'ai_integration' |
      'hardware'
    >;
  };
  additional: {
    github_username?: string;        // Optional
    linkedin_url?: string;           // Optional, must be valid URL
    bio?: string;                    // Optional, max 500 chars
  };
}
```

**Example JSON**:
```json
{
  "basic_info": {
    "full_name": "John Doe",
    "preferred_language": "en",
    "timezone": "America/New_York"
  },
  "education": {
    "level": "undergraduate",
    "field_of_study": "Computer Science",
    "prior_experience": "beginner"
  },
  "interests": {
    "learning_goals": ["career_change", "professional_development"],
    "learning_style": "hands_on",
    "topics_of_interest": ["ros2", "simulation", "ai_integration"]
  },
  "additional": {
    "github_username": "johndoe",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "bio": "Aspiring robotics engineer interested in autonomous systems."
  }
}
```

**Validation Rules**:
- basic_info: All fields required
- education: All fields required
- interests: All fields required, arrays must have at least one item
- additional: All fields optional
- linkedin_url: Must be valid URL format if provided
- bio: Maximum 500 characters if provided

**Save Strategy**:
- Save on step completion (clicking "Next" or "Complete")
- Partial updates allowed (e.g., save basic_info after Step 1)
- Atomic updates to prevent race conditions
- No auto-save within steps (user loses unsaved field data if they close browser)

**Query Patterns**:
```sql
-- Get users who selected 'career_change' as a learning goal
SELECT * FROM users
WHERE preferences->'interests'->'learning_goals' ? 'career_change';

-- Get users with 'advanced' prior experience
SELECT * FROM users
WHERE preferences->'education'->>'prior_experience' = 'advanced';

-- Get users who prefer Urdu language
SELECT * FROM users
WHERE preferences->'basic_info'->>'preferred_language' = 'ur';
```

---

## Database Indexes

### Performance Optimization

**Critical Indexes** (already defined above):
- `users.email` (UNIQUE) - Login queries
- `users.onboarding_completed` - Content access checks
- `sessions.token` - Session validation
- `sessions.user_id` - User session lookup
- `oauth_accounts.user_id` - OAuth account lookup
- `oauth_accounts.provider` - Provider-specific queries

**Additional Indexes** (for analytics/reporting):
```sql
-- Index for finding users by current stage
CREATE INDEX idx_users_current_stage ON users(current_stage);

-- Index for finding active sessions
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at)
WHERE revoked_at IS NULL;

-- Composite index for OAuth provider + account ID
CREATE UNIQUE INDEX idx_oauth_provider_account
ON oauth_accounts(provider, provider_account_id);

-- JSON index for onboarding preferences queries
CREATE INDEX idx_users_preferences_language
ON users((preferences->'basic_info'->>'preferred_language'));
```

---

## Data Integrity Constraints

### Foreign Key Constraints

```sql
-- Session references User
ALTER TABLE sessions
ADD CONSTRAINT fk_sessions_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;

-- OAuth Account references User
ALTER TABLE oauth_accounts
ADD CONSTRAINT fk_oauth_accounts_user_id
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

### Check Constraints

```sql
-- Ensure current_stage is between 1 and 5
ALTER TABLE users
ADD CONSTRAINT chk_users_current_stage
CHECK (current_stage >= 1 AND current_stage <= 5);

-- Ensure role is valid
ALTER TABLE users
ADD CONSTRAINT chk_users_role
CHECK (role IN ('student', 'instructor', 'admin'));

-- Ensure provider is valid
ALTER TABLE oauth_accounts
ADD CONSTRAINT chk_oauth_provider
CHECK (provider IN ('google', 'github'));

-- Ensure expires_at is in the future at creation
ALTER TABLE sessions
ADD CONSTRAINT chk_sessions_expires_at
CHECK (expires_at > created_at);
```

---

## Migration Strategy

### Alembic Migration

**File**: `alembic/versions/20260225_add_onboarding_columns.py`

```python
"""Add onboarding columns to users table

Revision ID: 20260225_add_onboarding
Revises: previous_revision
Create Date: 2026-02-25 23:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '20260225_add_onboarding'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns if they don't exist (idempotent)
    op.execute("""
        DO $$
        BEGIN
            -- Add email_verified column
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='users' AND column_name='email_verified'
            ) THEN
                ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
            END IF;

            -- Add onboarding_completed column
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='users' AND column_name='onboarding_completed'
            ) THEN
                ALTER TABLE users ADD COLUMN onboarding_completed BOOLEAN DEFAULT FALSE;
            END IF;

            -- Add current_stage column
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='users' AND column_name='current_stage'
            ) THEN
                ALTER TABLE users ADD COLUMN current_stage INTEGER DEFAULT 1;
            END IF;

            -- Add role column
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='users' AND column_name='role'
            ) THEN
                ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'student';
            END IF;

            -- Add preferences column
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name='users' AND column_name='preferences'
            ) THEN
                ALTER TABLE users ADD COLUMN preferences JSONB;
            END IF;
        END $$;
    """)

    # Create indexes
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_onboarding_completed
        ON users(onboarding_completed);

        CREATE INDEX IF NOT EXISTS idx_users_current_stage
        ON users(current_stage);
    """)

    # Add check constraints
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'chk_users_current_stage'
            ) THEN
                ALTER TABLE users
                ADD CONSTRAINT chk_users_current_stage
                CHECK (current_stage >= 1 AND current_stage <= 5);
            END IF;

            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'chk_users_role'
            ) THEN
                ALTER TABLE users
                ADD CONSTRAINT chk_users_role
                CHECK (role IN ('student', 'instructor', 'admin'));
            END IF;
        END $$;
    """)


def downgrade():
    # Remove constraints
    op.drop_constraint('chk_users_role', 'users', type_='check')
    op.drop_constraint('chk_users_current_stage', 'users', type_='check')

    # Remove indexes
    op.drop_index('idx_users_current_stage', 'users')
    op.drop_index('idx_users_onboarding_completed', 'users')

    # Remove columns
    op.drop_column('users', 'preferences')
    op.drop_column('users', 'role')
    op.drop_column('users', 'current_stage')
    op.drop_column('users', 'onboarding_completed')
    op.drop_column('users', 'email_verified')
```

---

## Data Access Patterns

### Common Queries

**1. Check if user has completed onboarding**:
```sql
SELECT onboarding_completed
FROM users
WHERE id = :user_id;
```

**2. Get user with onboarding preferences**:
```sql
SELECT id, email, name, onboarding_completed, preferences
FROM users
WHERE id = :user_id;
```

**3. Validate session token**:
```sql
SELECT s.id, s.user_id, u.email, u.name, u.onboarding_completed
FROM sessions s
JOIN users u ON s.user_id = u.id
WHERE s.token = :token
  AND s.expires_at > NOW()
  AND s.revoked_at IS NULL;
```

**4. Get user's OAuth accounts**:
```sql
SELECT provider, provider_account_id, created_at
FROM oauth_accounts
WHERE user_id = :user_id;
```

**5. Find user by OAuth provider account**:
```sql
SELECT u.*
FROM users u
JOIN oauth_accounts oa ON u.id = oa.user_id
WHERE oa.provider = :provider
  AND oa.provider_account_id = :provider_account_id;
```

**6. Get users by learning goal**:
```sql
SELECT id, email, name
FROM users
WHERE preferences->'interests'->'learning_goals' ? :goal
  AND onboarding_completed = true;
```

---

## Data Model Complete

**Phase 1 Status**: Data model defined
**Next Step**: API contracts definition
