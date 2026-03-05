# IntelliStack Authentication & Rate Limiting System Documentation

This document describes the authentication and rate limiting system implemented in the IntelliStack platform, including recent improvements made to enhance security, scalability, and consistency.

## Authentication System

The IntelliStack platform uses Better-Auth as its authentication provider with JWT tokens for stateless authentication.

### JWT Configuration

- **Algorithm**: EdDSA (Ed25519 curve) - Asymmetric signature algorithm
- **Token Format**: JWT with EdDSA signing
- **Key Distribution**: JWKS endpoint at `/.well-known/jwks.json`
- **Validation**: Performed by the `JWKSAuthMiddleware` in the backend

### Token Flow

1. User authenticates via Better-Auth server
2. Server issues JWT token with EdDSA signature
3. Token is stored in `better-auth.session_token` cookie
4. Frontend sends token in Authorization header or includes cookie
5. Backend `JWKSAuthMiddleware` validates token against JWKS keys

### Middleware Implementation

The `JWKSAuthMiddleware` handles:

- Token extraction from Authorization header or session cookie
- JWT validation against JWKS public keys
- User information injection into request context
- Error handling for invalid/expired tokens
- Caching of JWKS keys with fallback mechanisms

## Rate Limiting System

The rate limiting system was upgraded from an in-memory solution to a Redis-based solution for production readiness.

### Redis-Based Rate Limiter

- **Storage**: Redis sorted sets for sliding window counter
- **Algorithm**: Tracks request timestamps within specified window
- **Scalability**: Works across multiple server instances
- **Key Format**: `rate_limit:{client_ip}:{user_agent}`

### Rate Limit Configuration

- **Authenticated Users**: 60 requests per minute
- **Authentication Endpoints**: 10 requests per minute
- **Key Structure**: Uses sliding window with automatic cleanup

## Cookie Naming Consistency

### Before Changes

The cookie naming was inconsistent across services:
- Multiple possible names were being checked
- Potential for session confusion

### After Changes

- Standardized on `better-auth.session_token` across all services
- Frontend now checks for single, consistent cookie name
- Backend uses the same standardized name

## Security Considerations

### JWKS Validation

- Public keys are cached with 5-minute TTL
- Fallback to last-known-good keys if JWKS endpoint is unavailable
- Exponential backoff for failed JWKS requests

### SameSite Policy

- Auth server uses SameSite=None for cross-site OAuth flows
- Frontend handles authentication state appropriately
- Secure flag is enforced where required

## Error Handling

### JWT Validation Errors

- Expired tokens: Return 401 Unauthorized
- Invalid signatures: Return 401 Unauthorized
- Missing claims: Log error and continue without user context
- JWKS endpoint failures: Use fallback keys with warning

### Rate Limiting Errors

- Exceeded limits: Return 429 Too Many Requests
- Redis connection failures: May cause rate limiting to fail open (logging occurs)

## Testing

### Test Coverage

- JWT validation with EdDSA algorithm
- Rate limiter functionality
- Error handling scenarios
- Cookie name consistency

## Performance Considerations

- JWKS keys are cached to avoid repeated network calls
- Redis operations are efficient for rate limiting
- Middleware adds minimal overhead to each request