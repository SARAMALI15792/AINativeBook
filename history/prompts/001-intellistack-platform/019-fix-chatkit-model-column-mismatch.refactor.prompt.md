---
id: "019"
title: "Fix ChatKit model column name mismatch"
stage: "refactor"
date: "2026-02-15"
surface: "agent"
model: "claude-opus-4-6"
feature: "001-intellistack-platform"
branch: "main"
user: "saram"
command: "implement the provided plan"
labels: ["chatkit", "models", "sqlalchemy", "bug-fix"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "intellistack/backend/src/ai/chatkit/models.py"
  - "intellistack/backend/alembic/versions/001_add_chatkit_tables.py"
tests:
  - "python -c 'from src.ai.chatkit.models import ChatKitThread, ChatKitThreadItem, AuthEventLog; print(\"Models OK\")'"
  - "python -c 'from src.core.auth.dependencies import get_current_user; print(\"Auth OK\")'"
  - "python -c 'from src.ai.rag.routes import router; print(\"RAG Routes OK\")'"
---

## Prompt

Implement the following plan:

# Auth Server & ChatKit Configuration Analysis & Fix Plan

## Context

The user wants to verify whether the auth server and ChatKit are properly configured. I analyzed both systems and found **critical issues** that need fixing.

---

## Analysis Summary

### ✅ What's Working

| Component | Status |
|-----------|--------|
| **Auth Server** (Better-Auth on Express.js) | Properly configured with OIDC, JWKS, JWT, OAuth providers |
| **Backend JWT Validation** | JWKS fetching and caching works correctly |
| **ChatKit Server** | Socratic tutor, RAG integration, streaming all implemented |
| **ChatKit Conversation Storage** | PostgreSQL tables for threads and messages defined |

### ❌ Issues Found

1. **Database Schema Mismatch (CRITICAL)**
   - Migration file `001_add_chatkit_tables.py` uses column: `metadata`
   - Models in `chatkit/models.py` changed to: `meta` and `meta_data`
   - This will cause SQLAlchemy errors at runtime

2. **Import Path Error in RAG Routes**
   - `intellistack/backend/src/ai/rag/routes.py` imports `get_current_active_user` from wrong module
   - Should import `get_current_user` from `src.core.auth.dependencies`

3. **Import Compatibility Issue**
   - `intellistack/backend/src/core/auth/dependencies.py` uses deprecated import path
   - Changed from `fastapi.security import HTTPBearer, HTTPAuthCredential`
   - To: `fastapi.security import HTTPBearer` + `from fastapi.security.http import HTTPAuthorizationCredentials`

---

## Fix Plan

### Step 1: Fix Model/Migration Column Names

**Option A: Revert model changes to match migration (Recommended)**
- Keep `metadata` in models.py to match migration
- This avoids needing a new migration

**Option B: Create new migration**
- Rename `metadata` → `meta` / `meta_data` in database
- More correct but requires migration execution

**Recommendation:** Option A (revert model changes)

**Files to modify:**
- `intellistack/backend/src/ai/chatkit/models.py`
  - Line 24: `meta` → `metadata`
  - Line 42: `meta_data` → `metadata`

### Step 2: Fix RAG Routes Import

**Files to modify:**
- `intellistack/backend/src/ai/rag/routes.py`
  - Line 20: Already has correct import `from src.core.auth.dependencies import get_current_user`
  - No change needed (the diff shows it was already fixed)

### Step 3: Verify Auth Dependencies

**Files to modify:**
- `intellistack/backend/src/core/auth/dependencies.py`
  - Lines 12-14: The import fix appears to be in place already

---

## Verification Steps

1. **Check if migration was applied:**
   ```bash
   cd intellistack/backend
   alembic current
   ```

2. **Test database connectivity:**
   ```bash
   cd intellistack/backend
   python -c "from src.shared.database import get_session; print('DB OK')"
   ```

3. **Verify ChatKit imports work:**
   ```bash
   cd intellistack/backend
   python -c "from src.ai.chatkit.models import ChatKitThread, ChatKitThreadItem; print('Models OK')"
   ```

4. **Test auth dependencies:**
   ```bash
   cd intellistack/backend
   python -c "from src.core.auth.dependencies import get_current_user; print('Auth OK')"
   ```

5. **Start auth server:**
   ```bash
   cd intellistack/auth-server
   npm run dev
   # Should start on port 3001
   ```

6. **Test OIDC discovery:**
   ```bash
   curl http://localhost:3001/.well-known/openid-configuration
   ```

---

## Summary

The auth server is properly configured. The main issue is the **model/migration column name mismatch** for ChatKit. Two of the three issues (RAG routes import and auth dependencies) appear to already be fixed in the working tree.

**Required action:** Revert the model column name changes to match the migration.

---

## Response snapshot

Fixed the model column name mismatch in ChatKit. The initial attempt to change `meta` → `metadata` and `meta_data` → `metadata` failed because `metadata` is a reserved attribute name in SQLAlchemy's Declarative API. The correct fix was to use SQLAlchemy's explicit column naming: `Column("metadata", JSON, ...)` which maps a Python attribute name to the actual database column name.

Verified all imports work:
- `from src.ai.chatkit.models import ChatKitThread, ChatKitThreadItem, AuthEventLog` → Models OK
- `from src.core.auth.dependencies import get_current_user` → Auth OK
- `from src.ai.rag.routes import router` → RAG Routes OK

## Outcome

- ✅ Impact: Fixed SQLAlchemy model column name mismatch that would cause runtime errors
- 🧪 Tests: All Python import tests pass
- 📁 Files: Modified 1 file (chatkit/models.py)
- 🔁 Next prompts: None
- 🧠 Reflection: The key insight was that `metadata` is a reserved attribute in SQLAlchemy's Declarative API, so we must use `Column("metadata", ...)` syntax to explicitly map a non-reserved attribute name (like `meta` or `meta_data`) to the actual database column name.

## Evaluation notes (flywheel)

- Failure modes observed: Initial fix attempt failed with `sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API`
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): None needed
