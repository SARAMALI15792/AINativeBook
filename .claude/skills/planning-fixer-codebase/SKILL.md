---
name: planning-fixer-codebase
description: Perform deep root cause analysis and create structured remediation plans for broken codebases with multiple unstable features. Follow a 5-phase framework: deep analysis, structured roadmap, controlled execution, system hardening, and validation.
license: Complete terms in LICENSE.txt
---

# Planning Fixer Codebase

This skill provides a systematic 5-phase framework to analyze and remediate unstable codebases with multiple broken features. It enables deep root cause analysis, gap identification, and structured remediation planning before making any changes to the codebase.

## When to Use This Skill

This skill should be used when:
- A deployed project has multiple broken features and instability
- Runtime errors, logical errors, or broken API contracts are present
- Authentication flow failures or frontend-backend misalignment occur
- Production-only failures need investigation
- Build or deployment issues are causing system instability
- Database inconsistencies require systematic remediation
- Architecture, security, or error handling gaps need addressing
- No immediate code fixes should be made until proper analysis is completed

## How to Use This Skill

Execute the following 5-phase framework:

### Phase 1: Deep Root Cause & System Gap Analysis
1. Perform runtime and functional audit:
   - Identify runtime errors, logical errors, and broken API contracts
   - Detect authentication flow failures and frontend-backend misalignment
   - Identify environment variable inconsistencies and production-only failures
   - Identify build or deployment issues and database inconsistencies
   - Document file name, function name, exact lines, root cause explanation, and severity classification (Critical/Major/Minor)
2. Perform comprehensive gap analysis across architecture, authentication & security, error handling, logging & observability, testing coverage, CI/CD gaps, code quality, performance & scalability, and configuration risks
3. Create module dependency mapping and identify cascading failure risks

### Phase 2: Structured Remediation Roadmap
1. Define fixing strategy with execution order and risk justification
2. Create issue-by-issue plan with file, problem, proposed change, risk level, and validation requirements
3. Develop regression prevention plan with required test specifications
4. Establish rollback strategy for safe reversion if fixes fail

### Phase 3: Controlled Execution
1. Apply fixes in defined order after approval
2. For each fix, document BEFORE and AFTER code, modification explanation, and root cause resolution
3. Confirm no new side effects after each fix
4. Re-validate dependencies after each fix

### Phase 4: System Hardening & Stabilization
1. Improve security posture, validation layers, error handling, logging standardization, and configuration management
2. Introduce centralized error middleware, structured logging, environment validation, health checks, rate limiting, and request validation
3. Enhance CI/CD with auto tests, build verification, lint/type checks, and production readiness checks

### Phase 5: Success Criteria & Validation
1. Validate zero runtime errors, verified auth flows, validated endpoints, successful frontend builds
2. Confirm backend starts without warnings, tests pass, no security gaps, and properly structured logs
3. Verify no hardcoded secrets are present

## Resources Available

- Use files in `scripts/` for automated analysis tools
- Reference files in `references/` for best practices and checklists
- Use files in `assets/` for remediation templates and documentation

## Important Guidelines

- Do NOT apply random fixes or treat symptoms without confirming root cause
- Do NOT skip gap analysis or perform fixes before completing Phase 1 and 2
- Always justify technical decisions with risk assessment and impact analysis
- Think like a production engineer handling a live system
- Prioritize stability, security, and maintainability over quick fixes
- Wait for explicit approval before executing any Phase 3 fixes
- Document every issue with file, function, line numbers, and severity classification
