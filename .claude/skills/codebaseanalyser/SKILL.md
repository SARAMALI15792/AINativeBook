---
name: codebaseanalyser
description: Performs comprehensive deep analysis of entire codebase and deployment pipeline to identify issues in production environment. Conducts systematic investigation across architecture, authentication, file connections, deployment, CI/CD, and stability.
---

# Codebase Analyser

Perform comprehensive deep analysis of entire codebase and deployment pipeline to identify why functionality is not working correctly in production. Execute systematic investigation across all aspects of the application including architecture, authentication, file-level connections, deployment, CI/CD pipeline, and stability improvements.

## When to Use This Skill

Use this skill when:
- Deployed application functionality is not working correctly in production
- Need comprehensive deep analysis of entire codebase
- Authentication system issues in production
- Deployment pipeline debugging is required
- CI/CD setup for auto-testing is needed
- Stability improvements and refactoring suggestions are required
- File-level and line-level connection audits are needed

## How to Execute the Skill

### Phase 1: Perform Full Codebase Architecture Analysis
1. Analyze the complete project structure
2. Identify:
   - Frontend framework and architecture
   - Backend framework and architecture
   - Database type and connection method
   - Authentication system implementation
   - API communication pattern
   - Environment configuration (.env usage)
   - Deployment configuration
3. Create a clear architecture map showing:
   - How frontend communicates with backend
   - How backend communicates with database
   - How authentication flows through the system

### Phase 2: Execute Authentication System Deep Trace
1. Identify:
   - Login route
   - Registration route
   - Token generation logic
   - Token validation middleware
   - Session or JWT handling
   - Password hashing method
   - Cookie handling (if any)
2. Trace authentication flow step-by-step:
   - User submits login form (frontend)
   - Request sent to backend
   - Backend processes credentials
   - Token created
   - Token returned to frontend
   - Token stored (localStorage/cookies)
   - Protected routes accessed
3. Check for:
   - CORS issues
   - Missing credentials in fetch/axios
   - Wrong base URLs
   - Environment variable misconfiguration
   - Production vs development differences
   - Missing middleware
   - Expired tokens
   - Wrong secret keys
   - API route mismatches

### Phase 3: Execute File-Level and Line-Level Connection Audit
1. Check every import/export
2. Verify that:
   - All API routes match frontend calls
   - All controllers are properly connected
   - All middleware is applied
   - Database models are properly registered
   - No circular dependencies exist
3. Identify any dead code or unused functions
4. Detect any runtime-only production errors

Provide a categorized issue list:
- Critical
- Major
- Minor

### Phase 4: Execute Deployment & Production Debugging
Analyze:
- Build process
- Environment variables in hosting platform
- Backend server configuration
- Reverse proxy (if any)
- Port binding
- Production logs
- CORS production policy
- HTTPS issues

Explain why it might work locally but fail after deployment.

### Phase 5: Implement CI/CD Pipeline Setup for Auto-Testing
Implement a CI/CD solution that:

1. Automatically runs tests on:
   - Every push
   - Every pull request
2. Tests:
   - API endpoints
   - Authentication flow
   - Database connection
   - Environment variable validation
   - Frontend build success
3. Fails deployment if tests fail
4. Runs linting and type-checking
5. Verifies that backend can start successfully
6. Verifies that frontend can build without errors

Provide:
- Suggested GitHub Actions (or CI provider) config
- Example workflow YAML file
- Suggested test structure
- Suggested test libraries

### Phase 6: Create Stability Improvement Plan
Create:

1. Refactoring suggestions
2. Security improvements
3. Logging improvements
4. Monitoring suggestions
5. Error handling improvements
6. Recommended production-grade best practices

## Resources Available

- Run `scripts/codebase_analysis.py` for automated codebase analysis
- Reference `references/production_debugging.md` for common production issues and debugging patterns
- Use `assets/github-workflow.yml` as a template for CI/CD workflow

## Important Guidelines

- Do not give generic advice
- Analyze the actual code deeply
- Explain root causes clearly
- Provide fixes with code examples
- Be systematic and structured
- Focus on production-specific issues
- Prioritize critical issues that prevent functionality
- Identify environment-specific configurations
- Ensure comprehensive coverage of all system components