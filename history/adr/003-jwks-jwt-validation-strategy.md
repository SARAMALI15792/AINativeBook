# ADR-003: JWKS-Based JWT Validation in FastAPI Resource Server

**Date**: 2026-02-11
**Status**: Accepted
**Initiated By**: Feature 002-better-auth-chatkit

---

## Context

FastAPI backend acts as a **resource server** — it needs to validate JWT tokens issued by the Better-Auth OIDC server but does not issue tokens itself. A decision was needed on how to implement this validation strategy.

**Constraints**:
- FastAPI is Python-based; must use Python libraries for JWT handling
- Tokens are RS256-signed by Better-Auth (asymmetric RSA keypair)
- Better-Auth exposes public keys via `/.well-known/jwks.json` endpoint
- FastAPI serves ~10-50 requests/second at 500 concurrent users; cannot afford per-request latency
- Better-Auth server may be temporarily unavailable; FastAPI must continue serving requests
- Role claims and email verification status must be extracted from JWT payload

**Drivers**:
- Standards-based token validation (OAuth 2.0, OIDC specs require JWKS for asymmetric signing verification)
- Minimize coupling between FastAPI and auth server
- Resilience: FastAPI should not fail if auth server is down (with reasonable fallback)
- Performance: JWKS fetch should be cached; should not add latency per request

---

## Decision

**Implement JWKS-based RS256 JWT validation in FastAPI with 5-minute caching and fallback to last-known-good keys**:

1. **JWKS Fetcher** (`core/auth/jwks.py`):
   - Fetch public keys from `https://{BETTER_AUTH_URL}/.well-known/jwks.json`
   - Cache keys for 5 minutes (TTL: 300 seconds)
   - On cache miss or expiry: attempt fresh fetch
   - Fallback: if fetch fails and cache exists, use cached keys and log warning
   - If fetch fails and no cache: return 503 Service Unavailable with Retry-After header

2. **JWT Validation** (`core/auth/dependencies.py`):
   - Extract Bearer token from `Authorization: Bearer <token>` header
   - Use PyJWT with `jwt.decode()` to verify RS256 signature using public key
   - Check token expiry (`exp` claim), issuer (`iss` claim), and audience (`aud` claim)
   - Extract user claims: `sub` (user ID), `email`, `name`, `role`, `email_verified`
   - Return `AuthenticatedUser` dataclass or raise HTTPException(401)

3. **Role-Based Access Control** (`core/auth/dependencies.py`):
   - `require_role(*roles: str)` dependency factory checks `user.role` against allowed roles
   - Raise HTTPException(403) if role check fails
   - Usage: `@router.get("/admin/users", dependencies=[Depends(require_role("admin"))])`

4. **Email Verification Check** (`core/auth/dependencies.py`):
   - `require_verified_email(user: AuthenticatedUser)` checks `email_verified` claim
   - Raise HTTPException(403) if email not verified
   - Required for lesson access and AI tutor

5. **Middleware Integration** (`shared/middleware.py`):
   - Update request flow to call `get_current_user` dependency at route level (not middleware)
   - Remove old `BetterAuthSessionMiddleware`
   - Add JWKS manager initialization on app startup

---

## Consequences

### ✅ Advantages

1. **Standards Compliance**: JWKS is OIDC standard; enables other services to validate same tokens (mobile app, CLI, webhooks)
2. **Low Latency**: JWKS keys cached 5 minutes; no per-request auth server calls
3. **Resilience**: FastAPI continues serving requests even if auth server is temporarily down (using cached keys)
4. **Decoupling**: FastAPI does not depend on auth server availability per request; only periodic JWKS fetch
5. **Scalability**: Token validation is CPU-bound (RSA signature verification), not network-bound; can handle 1000s of requests/sec
6. **Flexibility**: Public key validation allows token generation and validation to evolve independently
7. **Security**: Private key never leaves auth server; FastAPI uses only public key (defensible in code review)

### ⚠️ Tradeoffs

1. **JWKS Fetch Latency**: First request on app startup or after 5-min cache expiry adds ~50-200ms (mitigated by background refresh task)
2. **Cache Invalidation**: If auth server rotates RSA key pair, FastAPI may use stale keys for up to 5 minutes (mitigated by cache-control headers, monitoring)
3. **Token Revocation Latency**: If admin revokes user token, revocation is not visible to FastAPI until next JWKS fetch or token expiry (mitigated by short token TTL: 6 hours)
4. **Operational Debugging**: If JWKS endpoint unreachable, requires troubleshooting across two services (auth server + FastAPI)
5. **Fallback Complexity**: Implementing fallback to last-known-good keys adds code complexity (mitigated by clear error handling)

### 🚨 Risks

1. **JWKS Fetch Failure**: If FastAPI cannot reach auth server JWKS endpoint:
   - **Scenario**: Auth server network unreachable, DNS down, or endpoint broken
   - **Impact**: New users cannot authenticate; existing users with valid tokens continue (using cached keys)
   - **Mitigation**:
     - Health check monitoring on JWKS endpoint
     - Alert on fetch failures
     - Graceful degradation: log warning, serve using cached keys
     - Last resort (no cache): return 503 with Retry-After: 30 seconds

2. **RSA Key Rotation**: If auth server rotates keys without proper cache-control headers:
   - **Scenario**: Auth server generates new RSA key pair; old FastAPI cache still using old key
   - **Impact**: Tokens signed with new key rejected as "invalid signature" for up to 5 minutes
   - **Mitigation**:
     - Auth server must set `Cache-Control: public, max-age=300` header on JWKS endpoint
     - Implement cache invalidation on `X-Key-Rotated` header (if auth server supports)
     - Monitor token validation error rates; alert if spikes

3. **Token Replay / Revocation**: If admin revokes user token (e.g., for security incident):
   - **Scenario**: Token is still valid (not expired), FastAPI verifies signature successfully
   - **Impact**: User cannot be immediately logged out; must wait for token to expire (6 hours)
   - **Mitigation**:
     - Short token TTL (6 hours) acceptable for learning platform
     - Implement token blacklist API (future feature) if per-request revocation needed
     - Leverage refresh token expiry (7 days) as secondary revocation point

4. **Man-in-the-Middle (MITM)**: If JWKS fetch over HTTP (not HTTPS):
   - **Scenario**: Attacker intercepts JWKS response, injects malicious keys
   - **Impact**: FastAPI accepts forged tokens
   - **Mitigation**:
     - Always use HTTPS for JWKS URL in production (`https://auth.intellistack.app/.well-known/jwks.json`)
     - Validate certificate in PyJWT configuration
     - Use certificate pinning (advanced) if high-risk environment

---

## Alternatives Considered

### Alternative 1: Per-Request Auth Server Calls (Stateless Validation)

**Approach**: FastAPI calls auth server `/api/auth/verify-token` endpoint for every request.

**Components**:
```python
async def get_current_user(request: Request):
    token = extract_bearer_token(request)
    response = await httpx.get(
        f"{BETTER_AUTH_URL}/api/auth/verify-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()  # user object
```

**Rationale for rejection**:
- **Latency**: Adds 50-200ms per request (network round-trip to auth server)
- **Coupling**: FastAPI tightly coupled to auth server availability; if auth server down, all requests fail
- **Scalability**: At 10 req/sec with 100ms latency = 1 extra second of blocking per request
- **Reliability**: Network flakiness causes cascading failures
- **Cost**: 10 req/sec × 86,400 sec/day = 864,000 auth server calls/day (unnecessary load)

**Score**: ❌ Rejected — latency, coupling, reliability issues

---

### Alternative 2: Shared Secret (HS256 Symmetric Signing)

**Approach**: Auth server and FastAPI share a secret key; tokens signed with HS256 (symmetric algorithm).

**Components**:
```python
import jwt
secret = os.getenv("JWT_SECRET")
decoded = jwt.decode(token, secret, algorithms=["HS256"])
```

**Rationale for rejection**:
- **Security**: Shared secret must exist in FastAPI codebase (in env var); if FastAPI is compromised, attacker has secret
- **Key Management**: Secret rotation complex; must update both auth server and all FastAPI instances
- **Non-Standard**: HS256 not recommended for multi-service architectures; RS256 is standard (public key verification)
- **Third-Party Validation**: Cannot allow third-party services to validate tokens without giving them the secret
- **Future Scaling**: If add mobile app or CLI, they need the secret too; shared secret becomes liability

**Score**: ❌ Rejected — security, standards, scalability issues

---

### Alternative 3: Session Cookie-Based (No JWT)

**Approach**: Use HTTP-only session cookies; FastAPI stores session data in Redis or database.

**Components**:
```python
@router.get("/api/data")
async def get_data(session: Session = Depends(get_session)):
    user = await db.query(User).filter(User.id == session.user_id).first()
    return user.data
```

**Rationale for rejection**:
- **Statefulness**: Requires server-side session store (Redis or database); cannot stateless scale
- **CSRF Complexity**: Session cookies require CSRF tokens for state-changing requests
- **Interoperability**: Cannot easily share sessions across auth server and FastAPI
- **Mobile/API Clients**: Session cookies don't work well for mobile apps or API clients (no cookie jar)
- **CORS**: Cross-origin cookie sharing complex and security-risky

**Score**: ❌ Rejected — statefulness, complexity, poor for distributed systems

---

### Alternative 4: API Keys (Not Suitable)

**Approach**: Issue static API keys to clients; FastAPI validates against database lookup.

**Components**:
```python
# Only for long-lived API clients, not user sessions
api_key = "sk_live_abc123def456"
```

**Rationale for rejection**:
- **Not for User Sessions**: API keys suitable for server-to-server communication, not interactive user auth
- **Rotation Complexity**: If user compromised, API key must be revoked; requires per-user database lookup per request
- **Expiry**: API keys typically long-lived (weeks/months); not suitable for session TTL (6 hours)
- **Scope**: Cannot implement role-based access with API keys as easily as JWT claims

**Score**: ⚠️ Defer — valid pattern for API clients, but not for user authentication

---

## Compatibility & Dependencies

- **PyJWT**: RS256 JWT verification (Python package)
- **jwcrypto**: Alternative library if PyJWT inadequate (optional)
- **httpx**: Async HTTP client for JWKS fetch (already in FastAPI stack)
- **FastAPI**: Dependency injection system for `get_current_user`
- **Python**: 3.11+

**Environment Variables**:
```
BETTER_AUTH_URL=https://auth.intellistack.app
BETTER_AUTH_JWKS_URL=https://auth.intellistack.app/.well-known/jwks.json
```

---

## Implementation Roadmap

### Phase 2 (Foundational)
- [ ] Create `core/auth/jwks.py` with JWKS manager (fetch, cache, fallback)
- [ ] Create `core/auth/dependencies.py` with `get_current_user`, `require_role`, `require_verified_email`
- [ ] Update `shared/middleware.py` to remove old auth middleware
- [ ] Update `requirements.txt` to add PyJWT, jwcrypto

### Phase 3+ (Per User Story)
- [ ] Update all routes to use `Depends(get_current_user)` instead of old auth
- [ ] Add `require_verified_email` to lesson and AI tutor routes
- [ ] Add `require_role("instructor", "admin")` to content creation routes

### Monitoring & Alerting
- [ ] Monitor JWKS fetch latency (should be < 200ms)
- [ ] Alert on JWKS fetch failures
- [ ] Monitor JWT validation error rate (should be ~0% for valid tokens)
- [ ] Alert if token signature verification fails > 1% of requests

---

## Testing Strategy

1. **Unit Tests**:
   - Valid token decoding with public key
   - Expired token rejection
   - Invalid signature rejection
   - Role claim extraction
   - Email verification check

2. **Integration Tests**:
   - Request with valid token → success
   - Request with invalid token → 401
   - Request with insufficient role → 403
   - Request without Authorization header → 401
   - JWKS cache hits (no re-fetch within 5 min)

3. **Resilience Tests**:
   - JWKS endpoint down → FastAPI uses cached keys
   - JWKS endpoint down + no cache → FastAPI returns 503
   - Auth server key rotation → FastAPI fetches new keys within 5 min

---

## Related ADRs

- ADR-001: Three-Service Architecture (this server is one of three)
- ADR-002: Better-Auth as Standalone OIDC Server (issues tokens validated here)

---

## References

- OAuth 2.0 Bearer Token Usage: https://tools.ietf.org/html/rfc6750
- OIDC Core Spec (JWKS): https://openid.net/specs/openid-connect-core-1_0.html#IDToken
- RFC 7517 (JSON Web Key): https://tools.ietf.org/html/rfc7517
- RFC 7518 (JSON Web Algorithms - RSA): https://tools.ietf.org/html/rfc7518
- PyJWT Documentation: https://pyjwt.readthedocs.io/
- `specs/002-better-auth-chatkit/plan.md` § Phase 3, Contracts
- `specs/002-better-auth-chatkit/research.md` § R-003

---

## Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-02-11 | SDD Agent | Initial decision record |
