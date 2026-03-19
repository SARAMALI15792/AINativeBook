# IntelliStack Remediation - Detailed Implementation Tasks

**Project:** IntelliStack Architecture Fixes
**Timeline:** 4-8 weeks
**Status:** Ready for Sprint Planning

---

## 🔴 PHASE 1: SECURITY HARDENING (Week 1)

### Task 1.1: Fix Hardcoded User ID in Learning Routes
**Priority:** CRITICAL
**Effort:** 4 hours
**Owner:** [Engineer 1]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 1.1.1: Create test file `tests/integration/test_learning_auth.py`
  - Test GET /learning/stages without auth → 401
  - Test GET /learning/stages with valid token → 200
  - Test user isolation: User1's progress != User2's progress
  - Effort: 1 hour

- [ ] 1.1.2: Update `src/core/learning/routes.py`
  - Remove `get_current_user_id()` function
  - Import `AuthenticatedUser` from auth.dependencies
  - Update all route handlers to use `Depends(get_current_user)`
  - Affected routes:
    - GET /learning/stages
    - GET /learning/stages/{stage_id}
    - GET /learning/progress
    - GET /learning/progress/{stage_id}
    - POST /learning/content/{content_id}/complete
    - All other learning endpoints
  - Effort: 2 hours

- [ ] 1.1.3: Update `src/core/learning/service.py`
  - Update method signatures to accept `user_id: str`
  - Ensure all queries filter by `user_id`
  - Verify no leakage of data between users
  - Effort: 1 hour

- [ ] 1.1.4: Run tests and verify
  - Run new auth tests
  - Run existing learning tests
  - Verify no regressions
  - Effort: 0.5 hours

**Definition of Done:**
- ✅ Learning routes require authentication
- ✅ Hardcoded user ID removed
- ✅ User isolation verified in tests
- ✅ All learning tests passing
- ✅ Code review approved

---

### Task 1.2: Fix Algorithm Mismatch in Middleware
**Priority:** CRITICAL
**Effort:** 3 hours
**Owner:** [Engineer 1]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 1.2.1: Create test file `tests/unit/test_jwt_algorithms.py`
  - Test valid EdDSA token → accepted
  - Test invalid RS256 token → 401 (not silent failure)
  - Test missing algorithm in header → 401
  - Effort: 1 hour

- [ ] 1.2.2: Update `src/shared/middleware.py` (JWKSAuthMiddleware)
  - Line 284-288: Change silent failure to exception
  - Add algorithm to log messages
  - Verify error message is clear
  - Effort: 0.5 hours

- [ ] 1.2.3: Update `src/core/auth/dependencies.py`
  - Ensure get_current_user also validates algorithm
  - Make error message consistent with middleware
  - Effort: 0.5 hours

- [ ] 1.2.4: Run tests and verify
  - Run JWT algorithm tests
  - Verify error responses are correct
  - Test with staging auth server
  - Effort: 0.5 hours

**Definition of Done:**
- ✅ EdDSA tokens accepted
- ✅ Other algorithms rejected with proper 401 error
- ✅ No silent failures
- ✅ Error messages clear and logged
- ✅ Tests passing

---

### Task 1.3: Fix CORS Configuration
**Priority:** HIGH
**Effort:** 4 hours
**Owner:** [Engineer 2]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 1.3.1: Create `src/config/environments.py` (NEW FILE)
  - Define CORS_CONFIG_DEV with localhost origins
  - Define CORS_CONFIG_PROD with empty defaults
  - Include documentation
  - Effort: 0.5 hours

- [ ] 1.3.2: Update `src/config/settings.py`
  - Change default cors_origins to empty list
  - Add CORS_ALLOW_CREDENTIALS as env var
  - Add validation for CORS origins
  - Effort: 1 hour

- [ ] 1.3.3: Update `src/main.py`
  - Load CORS config from environments.py
  - Use environment-based config
  - Add logging of CORS configuration on startup
  - Effort: 0.5 hours

- [ ] 1.3.4: Update `.env.example`
  - Add CORS_ORIGINS variable
  - Add CORS_ALLOW_CREDENTIALS variable
  - Add examples for dev and prod
  - Effort: 0.5 hours

- [ ] 1.3.5: Create `.env.production.example`
  - Show example production CORS config
  - Document required values
  - Effort: 0.5 hours

- [ ] 1.3.6: Test CORS
  - Test requests from allowed origin → success
  - Test requests from disallowed origin → CORS error
  - Test credentials handling
  - Effort: 0.5 hours

**Definition of Done:**
- ✅ CORS config environment-specific
- ✅ Hardcoded localhost removed from code
- ✅ Configuration via .env files
- ✅ Proper error messages for CORS violations
- ✅ Production config documented

---

### Task 1.4: Add Request ID Tracing
**Priority:** MEDIUM
**Effort:** 3 hours
**Owner:** [Engineer 2]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 1.4.1: Create `src/shared/tracing.py` (NEW FILE)
  - Define request_id_context ContextVar
  - Create RequestIDMiddleware
  - Effort: 1 hour

- [ ] 1.4.2: Update `src/main.py`
  - Add RequestIDMiddleware as FIRST middleware
  - Verify ordering (before other middleware)
  - Effort: 0.5 hours

- [ ] 1.4.3: Update `src/config/logging.py`
  - Add RequestIDFilter
  - Update log format to include request_id
  - Effort: 1 hour

- [ ] 1.4.4: Update all error handlers
  - Include request_id in error response
  - Update exception handler in main.py
  - Effort: 0.5 hours

- [ ] 1.4.5: Test request ID tracing
  - Make request and verify ID in response header
  - Verify ID in logs
  - Test concurrent requests have different IDs
  - Effort: 0.5 hours

**Definition of Done:**
- ✅ All requests have unique ID
- ✅ Request ID in response headers (X-Request-ID)
- ✅ Request ID in all logs
- ✅ Can trace request through system
- ✅ Error responses include request ID

---

## Phase 1 Validation Gate

**Acceptance Criteria (MUST ALL PASS):**
- [ ] No hardcoded user IDs in code
- [ ] All learning routes require valid authentication
- [ ] Algorithm validation doesn't fail silently
- [ ] CORS configuration environment-aware
- [ ] All requests have unique ID for tracing
- [ ] All Phase 1 tests passing (>95%)
- [ ] Code review approved
- [ ] Staging environment tested
- [ ] Security scan: no vulnerabilities

**Gate Review Meeting:** Friday of Week 1
**Attendees:** Project Lead, Security Lead, Tech Lead

---

## 🟡 PHASE 2: ARCHITECTURE CONSOLIDATION (Weeks 2-3)

### Task 2.1: Consolidate JWT Validation
**Priority:** HIGH
**Effort:** 8 hours
**Owner:** [Engineer 1]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 2.1.1: Refactor `src/shared/middleware.py` (JWKSAuthMiddleware)
  - Change role: Inject token only, don't validate
  - Remove JWT validation logic
  - Remove JWKS fetch
  - Remove claims extraction
  - Effort: 1 hour

- [ ] 2.1.2: Refactor `src/core/auth/dependencies.py`
  - Consolidate all validation logic into get_current_user
  - Remove middleware-based validation
  - Improve error messages
  - Effort: 2 hours

- [ ] 2.1.3: Create comprehensive tests `tests/integration/test_jwt_validation.py`
  - Test valid JWT → authenticated
  - Test expired JWT → 401
  - Test malformed JWT → 401
  - Test missing JWT → 401
  - Test session token fallback
  - Effort: 2 hours

- [ ] 2.1.4: Performance testing
  - Measure auth latency before
  - Apply changes
  - Measure auth latency after
  - Verify 2x improvement (no double validation)
  - Effort: 1 hour

- [ ] 2.1.5: Update documentation
  - Update ARCHITECTURE.md
  - Document auth flow
  - Update code comments
  - Effort: 1 hour

- [ ] 2.1.6: Review and testing
  - Code review
  - Run full test suite
  - Staging test
  - Effort: 1 hour

**Definition of Done:**
- ✅ JWT validated once per request
- ✅ Middleware only injects context
- ✅ Dependency does single validation
- ✅ Auth latency improved (2x faster)
- ✅ All tests passing
- ✅ No duplicate code

---

### Task 2.2: Fix Router Prefix Inconsistencies
**Priority:** HIGH
**Effort:** 4 hours
**Owner:** [Engineer 2]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 2.2.1: Audit all routers
  - List all routers and their current prefixes
  - Identify inconsistencies
  - Document current routing
  - Effort: 1 hour

- [ ] 2.2.2: Create test file `tests/integration/test_routes.py`
  - Test all routes accessible at correct URLs
  - Test route prefixes
  - Test overlapping routes don't conflict
  - Effort: 1 hour

- [ ] 2.2.3: Update `src/main.py`
  - Remove ALL `prefix=` parameters from include_router()
  - Verify all routers define their own prefix
  - Effort: 0.5 hours

- [ ] 2.2.4: Verify routers have prefixes
  - `src/core/content/routes.py`: `/api/v1/content`
  - `src/core/learning/routes.py`: `/api/v1/learning`
  - `src/core/users/routes.py`: `/api/v1/users`
  - `src/ai/chatkit/routes.py`: `/api/v1/chatkit`
  - All others documented
  - Effort: 1 hour

- [ ] 2.2.5: Update OpenAPI docs
  - Regenerate OpenAPI schema
  - Verify all routes in docs
  - Check no duplicate paths
  - Effort: 0.5 hours

**Definition of Done:**
- ✅ All routers have explicit prefixes
- ✅ main.py is clean (no prefix params)
- ✅ All routes accessible at correct URLs
- ✅ OpenAPI docs updated
- ✅ Tests verify routing

---

### Task 2.3: Standardize Error Handling
**Priority:** MEDIUM
**Effort:** 5 hours
**Owner:** [Engineer 1]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 2.3.1: Create `src/core/auth/errors.py` (NEW FILE)
  - Define custom exception classes
  - Map errors to HTTP status codes
  - Effort: 1 hour

- [ ] 2.3.2: Update `src/core/auth/dependencies.py`
  - Replace generic exceptions with custom ones
  - Add context to error logs
  - Include request ID in error context
  - Effort: 2 hours

- [ ] 2.3.3: Update `src/main.py`
  - Add exception handlers for custom errors
  - Return consistent error format
  - Include request_id in error response
  - Effort: 1 hour

- [ ] 2.3.4: Create test file `tests/unit/test_auth_errors.py`
  - Test error responses
  - Test error messages
  - Test HTTP status codes
  - Effort: 1 hour

**Definition of Done:**
- ✅ Custom exception classes defined
- ✅ Consistent error response format
- ✅ All errors include request_id
- ✅ Error messages are clear
- ✅ Tests verify error handling

---

### Task 2.4: Standardize Logging
**Priority:** MEDIUM
**Effort:** 3 hours
**Owner:** [Engineer 2]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 2.4.1: Update `src/config/logging.py`
  - Add RequestIDFilter
  - Update log format
  - Effort: 1 hour

- [ ] 2.4.2: Update all logging calls
  - Ensure all loggers use correct format
  - Add structured logging where appropriate
  - Effort: 1 hour

- [ ] 2.4.3: Test logging
  - Make requests and verify logs
  - Verify request ID in all logs
  - Parse logs for clarity
  - Effort: 1 hour

**Definition of Done:**
- ✅ Request ID in all logs
- ✅ Consistent log format
- ✅ Structured logging enabled
- ✅ Logs easily searchable by request ID

---

## Phase 2 Validation Gate

**Acceptance Criteria (MUST ALL PASS):**
- [ ] JWT validated exactly once per request
- [ ] Middleware only injects context
- [ ] No duplicate validation code
- [ ] Auth latency measured and improved
- [ ] All routers have explicit prefixes
- [ ] All routes accessible at correct URLs
- [ ] Error handling consistent and clear
- [ ] Request ID in all logs and errors
- [ ] All Phase 2 tests passing (>95%)
- [ ] Code review approved
- [ ] Staging environment fully tested

**Gate Review Meeting:** Friday of Week 3
**Attendees:** Project Lead, Tech Lead

---

## 🟢 PHASE 3: TESTING & HARDENING (Weeks 4-8)

### Task 3.1: Comprehensive Testing Suite
**Priority:** HIGH
**Effort:** 15-20 hours
**Owner:** [QA/Engineer]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 3.1.1: Unit tests for auth module
  - JWT validation
  - Token parsing
  - Claims extraction
  - Error handling
  - Target: >90% coverage
  - Effort: 5 hours

- [ ] 3.1.2: Integration tests for learning routes
  - Auth required
  - User isolation
  - Progress tracking
  - Stage unlocking
  - Target: >85% coverage
  - Effort: 5 hours

- [ ] 3.1.3: Security tests
  - No hardcoded credentials
  - CORS validation
  - Rate limiting
  - SQL injection prevention
  - Target: 100% coverage of security code
  - Effort: 5 hours

- [ ] 3.1.4: Load testing
  - 100 concurrent users
  - Measure latency
  - Measure throughput
  - Effort: 3-5 hours

- [ ] 3.1.5: Establish CI/CD
  - Run tests on every commit
  - Block merge if tests fail
  - Generate coverage reports
  - Effort: 3 hours

**Definition of Done:**
- ✅ >80% overall test coverage
- ✅ >90% auth module coverage
- ✅ All security paths tested
- ✅ Load test successful
- ✅ CI/CD pipeline operational

---

### Task 3.2: Monitoring & Observability
**Priority:** MEDIUM
**Effort:** 8-10 hours
**Owner:** [DevOps/Engineer]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 3.2.1: Add Prometheus metrics
  - Auth attempt counters
  - Auth latency histogram
  - Active user gauge
  - Learning progress counters
  - Effort: 3 hours

- [ ] 3.2.2: Create Grafana dashboards
  - Auth success/failure rates
  - Token validation latency
  - JWT error distribution
  - User login patterns
  - Effort: 3 hours

- [ ] 3.2.3: Configure alerts
  - High failure rate alert
  - High latency alert
  - Service unavailable alert
  - Effort: 2 hours

- [ ] 3.2.4: Test monitoring
  - Trigger alerts
  - Verify notifications
  - Test dashboard queries
  - Effort: 2 hours

**Definition of Done:**
- ✅ Metrics collected from all critical paths
- ✅ Dashboards show key metrics
- ✅ Alerts configured and tested
- ✅ Team can interpret metrics

---

### Task 3.3: Rate Limiting & Security Hardening
**Priority:** MEDIUM
**Effort:** 5 hours
**Owner:** [Engineer 1]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 3.3.1: Implement rate limiting
  - Apply to auth endpoints
  - Apply to learning endpoints
  - Configure limits in settings
  - Effort: 2 hours

- [ ] 3.3.2: Test rate limiting
  - Verify limits enforced
  - Verify error messages
  - Test Redis-based counting
  - Effort: 1 hour

- [ ] 3.3.3: Security hardening
  - Run security scan (e.g., bandit)
  - Fix any vulnerabilities
  - Review dependencies
  - Effort: 2 hours

**Definition of Done:**
- ✅ Rate limiting functional
- ✅ Security scan: no high-severity issues
- ✅ Dependencies up to date
- ✅ No hardcoded secrets

---

### Task 3.4: Documentation
**Priority:** HIGH
**Effort:** 10 hours
**Owner:** [Tech Writer/Senior Engineer]
**Status:** NOT STARTED

#### Subtasks:
- [ ] 3.4.1: ARCHITECTURE.md
  - System diagram
  - Auth flow
  - Data models
  - API conventions
  - Effort: 3 hours

- [ ] 3.4.2: AUTH_GUIDE.md
  - JWT structure
  - Token validation process
  - Error codes and meanings
  - Debugging guide
  - Effort: 2 hours

- [ ] 3.4.3: DEPLOYMENT.md
  - Environment variables
  - CORS configuration
  - Monitoring setup
  - Scaling considerations
  - Effort: 2 hours

- [ ] 3.4.4: TROUBLESHOOTING.md
  - Common auth errors
  - Debug using request ID
  - Log analysis
  - FAQ
  - Effort: 2 hours

- [ ] 3.4.5: Code documentation
  - Update docstrings
  - Add comments to complex logic
  - Effort: 1 hour

**Definition of Done:**
- ✅ All documentation complete and accurate
- ✅ Diagrams clear and up-to-date
- ✅ Code examples working
- ✅ Team can use docs to understand system

---

## Phase 3 Validation Gate

**Acceptance Criteria (MUST ALL PASS):**
- [ ] >80% overall test coverage
- [ ] All auth modules >90% covered
- [ ] Load test: 100+ concurrent users
- [ ] Monitoring dashboards operational
- [ ] Alerts tested and working
- [ ] Rate limiting enforced
- [ ] Security scan: no vulnerabilities
- [ ] Documentation complete
- [ ] Staging environment matches production
- [ ] Team trained on new system

**Gate Review Meeting:** End of Week 8
**Attendees:** Project Lead, Tech Lead, Security Lead, Ops Lead

---

## SUMMARY METRICS

### By Phase

| Phase | Tasks | Hours | Weeks | Risk |
|-------|-------|-------|-------|------|
| 1 | 4 | 14 | 1 | 🟢 LOW |
| 2 | 4 | 20 | 2 | 🟢 LOW |
| 3 | 4 | 30-40 | 4-5 | 🟢 LOW |
| **Total** | **12** | **64-74** | **4-8** | 🟢 **LOW** |

### By Owner Type

- **Backend Engineer (2):** 55+ hours
- **QA/Test Engineer:** 15-20 hours
- **DevOps/Ops Engineer:** 8-10 hours
- **Tech Lead/Architect:** 10-15 hours (oversight)

---

## DEPENDENCIES

### No External Dependencies

All changes are internal to the codebase. No external systems or services need to change.

### Internal Dependencies

- Phase 1 must complete before Phase 2
- Phase 2 must complete before Phase 3
- Task 1.1 must complete before learning routes can be fully tested
- Task 2.1 must complete before performance improvements visible

---

## RISKS & MITIGATION

### Risk 1: Breaking Authentication Flow
**Likelihood:** Medium
**Mitigation:** Comprehensive testing at each phase, staging environment

### Risk 2: User Isolation Not Working
**Likelihood:** Low
**Mitigation:** Specific tests for user isolation, code review focus

### Risk 3: Performance Regression
**Likelihood:** Low
**Mitigation:** Before/after metrics, load testing

### Risk 4: Deployment Issues
**Likelihood:** Medium
**Mitigation:** Staged rollout, rollback plan

---

## NEXT STEPS

1. **Week of 2026-03-16:** Kickoff Phase 1
2. **2026-03-21:** Phase 1 Validation Gate
3. **2026-03-22:** Start Phase 2
4. **2026-04-04:** Phase 2 Validation Gate
5. **2026-04-05:** Start Phase 3
6. **2026-05-02:** Phase 3 Validation Gate
7. **2026-05-05:** Production Deployment

---

**Document Version:** 1.0
**Status:** Ready for Sprint Planning
**Last Updated:** 2026-03-16
