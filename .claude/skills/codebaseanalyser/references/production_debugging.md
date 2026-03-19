# Codebase Analysis Reference Guide

This reference contains common patterns and issues to look for when analyzing a codebase for production problems.

## Common Production Issues

### Authentication Issues
- CORS misconfiguration between frontend and backend domains
- Different environment variables between development and production
- Token expiration handling
- Session management differences
- HTTPS vs HTTP mixed content issues
- Authentication headers missing in production

### API Connection Issues
- Hardcoded development URLs in production code
- Missing API base URLs in environment variables
- Incorrect proxy configuration
- Timeout settings too low for production networks
- Missing authentication headers in API calls

### Database Connection Issues
- Database connection strings not configured for production
- Connection pooling not optimized for production load
- SSL required in production but not configured
- Database migration scripts not run in production
- Different database schema between environments

### Frontend Build Issues
- Assets not properly referenced after build
- Path resolution issues in subdirectories
- Minification breaking functionality
- Environment-specific code not properly configured
- Bundle size exceeding limits

### Performance Issues
- Unoptimized database queries
- Memory leaks in long-running applications
- Unnecessary re-renders in frontend
- Blocking operations in main thread
- Inefficient algorithms for production data volumes

## Environment-Specific Configurations to Check

### Development vs Production Differences
- Debug/development flags enabled in production
- Error reporting too verbose in production
- Logging levels not adjusted for production
- Third-party service credentials mixed between environments
- Local vs remote service endpoints

### Security Configuration
- Secrets stored in code instead of environment variables
- Authentication disabled or weak in development
- SSL/TLS configuration differences
- Security headers missing in production
- Input validation differences between environments

## Deployment Configuration Checklist

### Server Configuration
- Correct ports configured for production
- Reverse proxy properly configured
- Load balancer settings
- SSL/TLS certificates properly installed
- Domain/subdomain routing correctly configured

### Process Management
- Application startup properly configured
- Process monitoring and restart policies
- Resource limits and allocation
- Health check endpoints available
- Graceful shutdown handling

## Common CI/CD Testing Patterns

### API Testing Strategies
```
- Test authentication flow end-to-end
- Test database connection and basic CRUD
- Test environment variable validation
- Test error handling and logging
- Test performance under load
```

### Frontend Testing Strategies
```
- Test build process completes successfully
- Test all routes and navigation
- Test API integration
- Test responsive design
- Test browser compatibility
```

### Security Testing Strategies
```
- Test authentication bypasses
- Test authorization rules
- Test input validation
- Test for common vulnerabilities (OWASP Top 10)
- Test data sanitization
```

## Production Monitoring and Logging

### Essential Metrics to Monitor
- Response times (p95, p99)
- Error rates
- Resource utilization (CPU, memory)
- Database query performance
- User session counts
- Failed authentication attempts

### Logging Best Practices
- Structured logging for easier parsing
- Log levels properly configured
- Sensitive data not logged
- Log retention policies
- Centralized log aggregation

## Error Categorization

### Critical Issues (Production Down)
- Application fails to start
- Database connection failures
- Authentication completely broken
- Core functionality inaccessible
- Security vulnerabilities

### Major Issues (Feature Broken)
- API endpoints returning errors
- Data not saving or loading
- Performance degradation
- Authentication partially broken
- Third-party integrations failing

### Minor Issues (User Experience)
- UI display issues
- Minor functionality bugs
- Performance optimization opportunities
- Code quality improvements
- Documentation updates

## Common Debugging Commands

### Node.js Applications
```
# Check for unmet dependencies
npm ls

# Run with debugging
node --inspect app.js

# Check for security vulnerabilities
npm audit
```

### Python Applications
```
# Check for missing dependencies
pip list

# Run with verbose logging
python -v app.py

# Check for security issues
bandit -r .
```

### Database Connections
```
# Test connection directly
psql -h hostname -U username -d database

# Check connection pool settings
SHOW max_connections;
```

This reference guide should be used when performing codebase analysis to ensure common issues are not missed and to provide systematic approaches to problem identification.