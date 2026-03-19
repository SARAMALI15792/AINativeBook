# IntelliStack Platform - Testing Suite

This directory contains the comprehensive testing suite for the IntelliStack Platform, an AI-Native Learning Platform for Physical AI & Humanoid Robotics education.

## Test Structure

### Unit Tests (`tests/unit/`)
- **Learning Module** (`tests/unit/learning/`): Models, services and business logic
  - `test_models.py`: SQLAlchemy model validation and relationships
  - `test_service.py`: Learning service business logic
- **Auth Module** (`tests/unit/auth/`): Authentication and authorization logic
  - `test_models.py`: User, Role, Session model tests
  - `test_dependencies.py`: Authentication dependencies and middleware
- **Shared Utilities** (`tests/unit/`)
  - `test_utils.py`: Utility functions (UUID generation, slugification, etc.)
  - `test_exceptions.py`: Custom exception classes

### Integration Tests (`tests/integration/`)
- **Learning Routes** (`tests/integration/learning/`): API endpoint integration
- **Auth Routes** (`tests/integration/auth/`): Authentication API integration

### Contract Tests (`tests/contract/`)
- **API Contract** (`tests/contract/test_api_contract.py`): API interface validation

### Test Fixtures and Factories
- **Factories** (`tests/factories.py`): Factory Boy models for test data
- **Fixtures** (`tests/conftest.py`): Pytest fixtures and test database setup

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- Coverage threshold: 80%
- Async mode enabled for async SQLAlchemy testing
- HTML and terminal coverage reporting
- Strict configuration and marker enforcement

### Database Configuration
- Uses in-memory SQLite database for testing
- Automatic schema creation and cleanup
- Transaction rollback after each test

### Environment Variables
The test suite automatically sets up the following environment variables:
```
SECRET_KEY=test-secret-key-for-testing
DATABASE_URL=sqlite+aiosqlite:///:memory:
REDIS_URL=redis://localhost:6379
QDRANT_HOST=localhost
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/callback/google
GITHUB_REDIRECT_URI=http://localhost:3000/api/auth/callback/github
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_JWKS_URL=http://localhost:3000/.well-known/jwks.json
ENVIRONMENT=test
DEBUG=True
LOG_LEVEL=DEBUG
```

## Running Tests

### Running All Tests
```bash
pytest
```

### Running Unit Tests
```bash
pytest tests/unit/
```

### Running with Coverage Report
```bash
pytest --cov=intellistack/backend/src
```

### Running Specific Test Files
```bash
pytest tests/unit/test_utils.py
```

### Running with Verbose Output
```bash
pytest -v
```

## Testing Philosophy

### Unit Tests
- Test individual components in isolation
- Cover all code paths including edge cases
- Fast execution with in-memory database
- Focus on business logic correctness

### Integration Tests
- Test API endpoints with real database connections
- Validate end-to-end functionality
- Check authentication and authorization flows
- Ensure database transaction integrity

### Contract Tests
- Validate API response schemas
- Ensure backward compatibility
- Check error response formats
- Validate endpoint contracts

## Test Coverage

The test suite aims for 80%+ code coverage with a focus on:
- Critical business logic paths
- Error handling and edge cases
- Database operations and relationships
- Authentication and authorization flows
- API request/response validation

## Dependencies

- pytest
- pytest-asyncio
- pytest-cov
- pytest-mock
- httpx
- factory-boy
- aiosqlite

## Future Testing Enhancements

- Performance tests for API endpoints
- Load testing scenarios
- Database migration testing
- End-to-end UI tests (when frontend is added)
- AI model response validation tests