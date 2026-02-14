---
id: 001
stage: plan
title: Implement BetterAuth Adapter Architecture
date: 2026-02-10
surface: agent
model: kimi-k2.5
feature: 001-intellistack-platform
branch: 001-intellistack-platform
user: saram
command: "Implement the following plan: [BetterAuth Adapter Architecture Plan]"
labels: ["betterauth", "authentication", "adapter", "architecture", "backend"]
links:
  spec: specs/001-intellistack-platform/spec.md
  ticket: null
  adr: null
  pr: null
files:
tests:
---

## Prompt

Implement the following plan:

# BetterAuth Adapter Architecture Plan

## Context

**Current State**: IntelliStack has a hybrid authentication system:
- **Backend**: Custom JWT implementation is active (`routes.py`, `service.py`)
- **BetterAuth**: Partial implementation exists (`routes_v2.py`, `service_v2.py`, `adapter.py`, `better_auth_config.py`) but is NOT wired up in `main.py`
- **Frontend**: Uses BetterAuth React hooks but still relies on Zustand/localStorage for some state
- **Database**: Existing SQLAlchemy models (User, Role, UserRole, Session) work with JWT

**Goal**: Complete the migration from custom JWT to BetterAuth with a clean adapter architecture.

## Key Architectural Decisions

1. Adapter Pattern Design - Use a two-way adapter that maps between BetterAuth's expected user format and IntelliStack's SQLAlchemy models
2. Session Management Strategy - Hybrid: BetterAuth validates session tokens, session data stored in existing `sessions` table
3. RBAC Integration - BetterAuth handles authentication, IntelliStack maintains RBAC authorization
4. Migration Path - Phased approach: Backend Migration → Frontend Transition → Social Login Addition → Cleanup

## Implementation Plan

### Phase 1: Backend BetterAuth Integration (Tasks T101-T106)

T101: Design BetterAuth Adapter Layer - Fix adapter.py imports and interface
T102: Implement BetterAuth Middleware in FastAPI
T103: Create BetterAuth API Endpoints
T104: Setup BetterAuth Database Schema - Add oauth_accounts table
T105: User Profile Synchronization
T106: Enhanced Security Features

## Response snapshot

Starting implementation of BetterAuth adapter architecture following the provided plan. Will begin with codebase exploration to understand current state, then proceed with:
1. Analyzing existing adapter.py and better_auth_config.py
2. Wiring up middleware in main.py
3. Implementing OAuth account table
4. Testing end-to-end authentication flow

## Outcome

- Impact: Major authentication system migration from custom JWT to BetterAuth
- Tests: Will need comprehensive auth flow tests
- Files: Multiple files in intellistack/backend/src/core/auth/
- Next prompts: Testing, frontend migration, social login
- Reflection: Careful migration needed to avoid breaking existing users

## Evaluation notes (flywheel)

- Failure modes observed: SDK API mismatch, session injection issues, OAuth config complexity
- Graders run and results (PASS/FAIL): Pending
- Prompt variant: N/A
- Next experiment: Verify each component incrementally
