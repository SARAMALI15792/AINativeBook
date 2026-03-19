# Planning Fixer Codebase - Reference Guide

This reference document provides detailed information that Claude should reference when performing deep root cause analysis and creating structured remediation plans for broken codebases.

## Phase 1: Deep Root Cause & System Gap Analysis

### Runtime & Functional Audit Checklist

#### Runtime Errors to Look For:
- Unhandled exceptions causing crashes
- Null pointer exceptions
- Memory leaks
- Stack overflow errors
- Type conversion errors
- Async/await issues
- Race conditions

#### Logical Errors to Look For:
- Incorrect conditional logic
- Off-by-one errors
- Infinite loops
- Bad state management
- Incorrect business logic implementation
- Improper data validation

#### API Contract Failures:
- Mismatched request/response schemas
- Incorrect HTTP status codes
- Missing authentication/authorization
- Inconsistent error handling
- Timeout and retry mechanism failures
- API versioning issues

#### Authentication Flow Failures:
- Insecure password handling
- Missing multi-factor authentication
- Session management issues
- Token expiration problems
- OAuth implementation flaws
- Password reset vulnerabilities

### Gap Analysis Categories

#### 1. Architecture Gaps
- Poor separation of concerns
- Tight coupling between modules
- Missing abstraction layers
- Incorrect layering (e.g., business logic in UI)
- Lack of design patterns implementation

#### 2. Authentication & Security Gaps
- Missing input validation
- SQL injection vulnerabilities
- XSS attack vectors
- Inadequate password policies
- Missing rate limiting
- Weak cryptography practices
- Insecure communication protocols

#### 3. Error Handling Gaps
- Silent failures without logging
- Generic error messages
- Inconsistent error response format
- Missing error boundaries
- Unhandled promise rejections
- Improper exception propagation

#### 4. Logging & Observability Gaps
- Lack of structured logging
- Missing performance metrics
- Insufficient monitoring
- No alerting mechanisms
- Poor audit trails
- Missing correlation IDs

#### 5. Testing Coverage Gaps
- Missing unit tests
- Lack of integration tests
- No end-to-end tests
- Insufficient edge case coverage
- Missing negative test cases
- No performance tests

#### 6. CI/CD Gaps
- No automated testing pipeline
- Missing security scanning
- No code quality checks
- Inadequate deployment validation
- Missing rollback mechanisms
- No environment-specific testing

#### 7. Code Quality & Technical Debt
- Large, monolithic functions
- Duplicate code blocks
- Inconsistent naming conventions
- Missing documentation
- Circular dependencies
- Unused imports and variables

#### 8. Performance & Scalability Gaps
- Blocking synchronous operations
- Inefficient database queries
- Missing caching strategies
- Poor resource management
- N+1 query problems
- Memory-intensive operations

#### 9. Configuration & Environment Risks
- Hardcoded secrets and API keys
- Missing environment validation
- Inconsistent configuration management
- Missing fallback mechanisms
- No configuration validation
- Exposed sensitive files

## Phase 2: Structured Remediation Plan Template

### Issue Classification Framework
- Critical: System failure, data loss, security breach
- Major: Feature broken, significant functionality impaired
- Minor: Non-breaking issue, minor optimization needed

### Fix Strategy Components
1. **Priority Order**: Critical → Major → Minor
2. **Dependency Chain**: Fix root causes before dependent issues
3. **Risk Assessment**: High/Medium/Low impact on system stability
4. **Validation Requirements**: What tests must pass after each fix

### Regression Prevention Checklist
- Unit tests for fixed functionality
- Integration tests for affected components
- End-to-end tests for user workflows
- Performance benchmarks comparison
- Security validation checks
- Compatibility verification

## Phase 3: Controlled Execution Guidelines

### Before Making Changes
1. Create a comprehensive backup
2. Document current system state
3. Ensure all tests pass in current state
4. Create feature branch for changes
5. Get change approval from stakeholders

### Change Implementation Process
1. Make minimal, targeted changes
2. Test each change in isolation
3. Verify dependent functionality still works
4. Update documentation as needed
5. Commit with clear, descriptive messages

### Post-Change Validation
1. Run full test suite
2. Perform manual testing of affected areas
3. Monitor system logs for new issues
4. Validate performance metrics
5. Confirm business requirements still met

## Phase 4: System Hardening Standards

### Security Enhancements
- Input validation middleware
- Rate limiting implementation
- Secure headers configuration
- Regular security audits
- Vulnerability scanning integration

### Error Handling Standardization
- Centralized error handling middleware
- Consistent error response format
- Structured logging format
- Error correlation tracking
- Automated error reporting

### Performance Optimizations
- Caching strategies
- Database query optimization
- Resource loading optimization
- Asynchronous processing implementation
- Load balancing configuration

## Phase 5: Success Criteria Definition

### Functional Validation
- [ ] All runtime errors resolved
- [ ] Authentication flows working
- [ ] API endpoints returning correct responses
- [ ] Database operations completing successfully
- [ ] Frontend components rendering properly

### Quality Validation
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Security vulnerabilities addressed
- [ ] Performance benchmarks met or exceeded
- [ ] Code quality metrics satisfied

### Observability Validation
- [ ] Structured logging implemented
- [ ] Error tracking system active
- [ ] Performance monitoring in place
- [ ] Health check endpoints functional
- [ ] Alerting thresholds configured
