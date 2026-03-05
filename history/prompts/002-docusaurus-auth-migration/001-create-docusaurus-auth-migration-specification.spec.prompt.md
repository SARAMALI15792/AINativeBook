---
id: 001
title: Create Docusaurus Auth Migration Specification
stage: spec
date: 2026-02-25
surface: agent
model: claude-sonnet-4.5
feature: 002-docusaurus-auth-migration
branch: 002-docusaurus-auth-migration
user: saram
command: /sp.specify
labels: ["specification", "authentication", "docusaurus", "onboarding", "migration"]
links:
  spec: specs/002-docusaurus-auth-migration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-docusaurus-auth-migration/spec.md
  - specs/002-docusaurus-auth-migration/checklists/requirements.md
tests:
  - Specification validation checklist (all items passed)
---

## Prompt

Create a complete and structured technical implementation plan for the following system architecture changes:

1. Fix Docusaurus Redirect Issue
- When redirecting from the main Next.js frontend to the Docusaurus book, it currently shows "Page Not Found" and broken link errors.
- Properly fix routing, baseUrl, deployment paths, and rewrite rules.
- Ensure the book loads correctly on first redirect without 404 errors.

2. Move Authentication to Docusaurus (Using Better Auth)
- Completely remove the Better Auth implementation from the main Next.js frontend.
- Implement the full Better Auth system inside the Docusaurus book application.
- When users land on Docusaurus, they must clearly see "Login" and "Signup" buttons.

3. Clean Multi-Step Authentication & Student Information Pipeline
- Use Better Auth for secure authentication (OAuth and/or email-password).
- After successful login, redirect users to a structured 4-step onboarding form.
- The onboarding UI must be clean, step-based, and visually clear at the top showing:
   Step 1 → Basic Information
   Step 2 → Educational Background
   Step 3 → Academic Interests / Goals
   Step 4 → Additional Student Details
- The step indicator must be visible at the top in a clear format: 1 → 2 → 3 → 4
- Each step must validate input before moving forward.
- Data must be stored properly in the database.
- After completing Step 4, redirect the user to the main book content.

4. Simplify Main Next.js Frontend
- Remove all authentication and personalization logic from Next.js.
- The navigation bar must ONLY contain: Login, Book, (Keep other static items unchanged)
- Clicking "Book" redirects to Docusaurus.
- Clicking "Login" redirects to Docusaurus authentication.

5. Database & Session Integrity
- Ensure Better Auth is properly connected to the database.
- Ensure sessions persist correctly.
- Prevent session validation errors.
- Verify OAuth providers (e.g., Google) function correctly.
- Ensure student onboarding data is securely linked to the authenticated user.

Provide:
- Step-by-step execution plan
- Architecture flow explanation
- Routing configuration fixes
- Required environment variables
- Better Auth integration details
- Database schema recommendations for student data
- Deployment considerations
- Testing checklist to validate correctness

## Response snapshot

Created comprehensive feature specification for Docusaurus Authentication Migration & Onboarding with the following components:

**Specification Structure:**
- 4 prioritized user stories (P1, P2) with 27 acceptance scenarios
- 40 functional requirements organized into 5 categories:
  - Authentication & Session Management (FR-001 to FR-010)
  - Onboarding Flow (FR-011 to FR-020)
  - Docusaurus Routing & Configuration (FR-021 to FR-028)
  - Next.js Simplification (FR-029 to FR-035)
  - Database Schema (FR-036 to FR-040)
- 10 measurable success criteria (technology-agnostic)
- 8 edge cases with resolution strategies
- 4 key entities (User, Session, OAuth Account, Onboarding Data)
- Assumptions, Dependencies, Out of Scope, and Notes sections

**User Stories:**
1. Student Authentication & Onboarding (P1) - Complete auth flow with 4-step onboarding
2. Simplified Next.js Navigation (P2) - Remove auth logic from Next.js
3. Docusaurus Routing & Deployment (P1) - Fix 404 errors and routing issues
4. Session & Database Integrity (P1) - Ensure data persistence and session management

**Key Requirements:**
- Better Auth integration within Docusaurus (not Next.js)
- 4-step onboarding collecting: Basic Info, Education, Interests, Additional Details
- Onboarding data stored in users.preferences JSON field
- Session persistence for 24 hours with automatic refresh
- Google OAuth with account linking
- Routing fix: baseUrl='/AINativeBook/', routeBasePath='/'
- Database migration to add missing user columns

**Validation:**
- Created specification quality checklist
- All checklist items passed on first validation
- No [NEEDS CLARIFICATION] markers (all requirements unambiguous)
- Ready for planning phase (/sp.plan)

## Outcome

- ✅ Impact: Complete feature specification created for authentication migration, defining 40 functional requirements, 4 user stories, and 10 success criteria. Provides clear roadmap for consolidating authentication into Docusaurus and implementing multi-step onboarding.
- 🧪 Tests: Specification validation checklist created and passed (all items ✅). 27 acceptance scenarios defined for testing.
- 📁 Files: Created spec.md (321 lines) and requirements.md checklist (58 lines)
- 🔁 Next prompts: Run `/sp.plan` to generate implementation architecture and design decisions, then `/sp.tasks` to create actionable task breakdown
- 🧠 Reflection: Specification successfully captures all 5 requirements from user input (routing fix, auth migration, onboarding, Next.js simplification, database integrity). No clarifications needed as all requirements were sufficiently detailed. Success criteria are measurable and technology-agnostic.

## Evaluation notes (flywheel)

- Failure modes observed: None. Specification created successfully on first attempt with all validation checks passing.
- Graders run and results (PASS/FAIL): Specification Quality Checklist - PASS (Content Quality ✅, Requirement Completeness ✅, Feature Readiness ✅)
- Prompt variant (if applicable): Standard /sp.specify workflow with detailed user requirements
- Next experiment (smallest change to try): Proceed to planning phase to validate that specification provides sufficient detail for architectural decisions
