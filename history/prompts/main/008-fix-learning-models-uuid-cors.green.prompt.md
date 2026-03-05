---
id: 008
title: Fix learning models UUID to String for CORS error
stage: green
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: main
branch: main
user: saram
command: general
labels: ["learning-models", "uuid-to-string", "cors-fix", "progress-tracking", "database-migration"]
links:
  spec: specs/main/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - intellistack/backend/src/core/learning/models.py
  - LEARNING_MODELS_UUID_FIX.md
tests:
  - Stage-1 endpoint (200 OK): PASS
  - CORS headers present: PASS
  - Database migration: PASS
  - Backend restart: PASS
---

## Prompt

react-dom.development.js:38560 Download the React DevTools for a better development experience: https://reactjs.org/link/react-devtools
curriculum/stage-1:1 Access to fetch at 'http://localhost:8000/api/v1/learning/stages/stage-1' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
:8000/api/v1/learning/stages/stage-1:1  Failed to load resource: net::ERR_FAILED
app-index.js:33 Error loading stage data: TypeError: Failed to fetch
    at loadStageData (page.tsx:59:37)
window.console.error @ app-index.js:33
curriculum/stage-1:1 Access to fetch at 'http://localhost:8000/api/v1/learning/stages/stage-1' from origin 'http://localhost:3000' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
:8000/api/v1/learning/stages/stage-1:1  Failed to load resource: net::ERR_FAILED
app-index.js:33 Error loading stage data: TypeError: Failed to fetch
    at loadStageData (page.tsx:59:37)
window.console.error @ app-index.js:33
auth.ts:62 Login successful: Object

## Response snapshot

**Problem Analysis:**

Browser showed CORS error, but this was misleading. The actual issue was the backend returning 500 Internal Server Error.

**Root Cause Investigation:**

Tested endpoint directly:
```bash
curl http://localhost:8000/api/v1/learning/stages/stage-1
Response: 500 Internal Server Error
```

Checked backend logs:
```
asyncpg.exceptions.UndefinedFunctionError: operator does not exist: character varying = uuid
HINT: No operator matches the given name and argument types. You might need to add explicit type casts.
```

The `Progress`, `UserBadge`, and `Certificate` models still had UUID columns for `user_id`, but `users.id` was changed to VARCHAR(255) in previous migration.

**Solution Implemented:**

**Step 1: Updated Learning Models**

Modified `intellistack/backend/src/core/learning/models.py`:

1. **Progress.user_id (line 135-137)**
```python
# Before
user_id: Mapped[str] = mapped_column(
    UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, unique=True
)

# After
user_id: Mapped[str] = mapped_column(
    String(255), ForeignKey("users.id"), nullable=False, unique=True
)
```

2. **UserBadge.user_id (line 206-208)**
```python
# Before
user_id: Mapped[str] = mapped_column(
    UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
)

# After
user_id: Mapped[str] = mapped_column(
    String(255), ForeignKey("users.id"), nullable=False
)
```

3. **Certificate.user_id (line 231-233)**
```python
# Before
user_id: Mapped[str] = mapped_column(
    UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
)

# After
user_id: Mapped[str] = mapped_column(
    String(255), ForeignKey("users.id"), nullable=False
)
```

**Step 2: Database Migration**

```sql
-- Drop foreign key constraints
ALTER TABLE progress DROP CONSTRAINT IF EXISTS progress_user_id_fkey;
ALTER TABLE user_badges DROP CONSTRAINT IF EXISTS user_badges_user_id_fkey;
ALTER TABLE certificates DROP CONSTRAINT IF EXISTS certificates_user_id_fkey;

-- Change column types
ALTER TABLE progress ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE user_badges ALTER COLUMN user_id TYPE VARCHAR(255);
ALTER TABLE certificates ALTER COLUMN user_id TYPE VARCHAR(255);

-- Recreate foreign key constraints
ALTER TABLE progress ADD CONSTRAINT progress_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE user_badges ADD CONSTRAINT user_badges_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE certificates ADD CONSTRAINT certificates_user_id_fkey
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
```

**Step 3: Backend Restart**
```bash
docker restart intellistack-backend
# Waited for health check
```

**Verification:**

```bash
GET /api/v1/learning/stages/stage-1
Origin: http://localhost:3000

Response: 200 OK
Headers:
  access-control-allow-origin: http://localhost:3000 ✅
  access-control-allow-credentials: true ✅
  content-type: application/json

Body:
{
  "id": "36ceb68e-aa61-4f13-a15c-e7d641ec4844",
  "number": 1,
  "name": "Foundations",
  "slug": "stage-1",
  "description": "Master the fundamentals of Linux, Python, and robotics theory",
  "learning_objectives": ["Linux fundamentals", "Python programming", "Math foundations"],
  "estimated_hours": 40,
  "status": "available",
  "percentage_complete": 0.0,
  "is_accessible": true
}
```

**CORS headers present** ✅
**No database errors** ✅
**Endpoint working** ✅

## Outcome

- ✅ Impact: Fixed learning models UUID mismatch causing 500 errors on stage endpoints. Changed 3 user_id columns from UUID to String(255) in Progress, UserBadge, and Certificate models. CORS now working correctly - frontend can access backend learning endpoints.
- 🧪 Tests: 4 tests passed - stage-1 endpoint (200 OK), CORS headers present, database migration successful, backend restart successful
- 📁 Files: Modified 1 model file (learning/models.py), created 1 documentation file (LEARNING_MODELS_UUID_FIX.md)
- 🔁 Next prompts: Test in browser to verify CORS error resolved, test complete learning flow (stage navigation, progress tracking), verify badge awarding
- 🧠 Reflection: This was the fourth UUID to String migration issue. The CORS error in the browser was misleading - the real problem was the backend returning 500 due to type mismatch. All critical endpoints (preferences, onboarding, stages) now working with Better-Auth custom user IDs. The cascade of fixes: users table → personalization tables → preferences routes enum handling → learning models.

## Evaluation notes (flywheel)

- Failure modes observed: CORS error message was misleading - actual issue was 500 Internal Server Error from UUID type mismatch
- Graders run and results (PASS/FAIL): All 4 tests PASS - stage endpoint, CORS headers, database migration, backend restart
- Prompt variant (if applicable): Direct SQL migration approach after identifying UUID mismatch in backend logs
- Next experiment (smallest change to try): Test complete learning flow in browser to verify all stage navigation and progress tracking working end-to-end
