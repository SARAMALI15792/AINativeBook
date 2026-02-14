# FastAPI Auth Middleware Contract

**Purpose**: Validate Better-Auth JWTs in FastAPI resource server using JWKS.

## Token Validation Flow

```
Request → Extract Bearer token → Fetch JWKS (cached) → Verify RS256 signature
  → Decode claims → Check expiry → Extract role → Inject into request state
```

## Middleware Interface

### `get_current_user` Dependency

```python
async def get_current_user(request: Request) -> AuthenticatedUser:
    """
    Extract and validate JWT from Authorization header.
    Returns AuthenticatedUser or raises HTTPException(401).
    """
```

**Returns**:
```python
@dataclass
class AuthenticatedUser:
    id: str           # user UUID
    email: str        # user email
    name: str         # display name
    role: str         # student | instructor | admin
    email_verified: bool
```

### `require_role` Dependency Factory

```python
def require_role(*roles: str) -> Callable:
    """
    Returns a FastAPI dependency that checks the user has one of the required roles.
    Raises HTTPException(403) if role check fails.
    """
```

**Usage**:
```python
@router.get("/admin/users")
async def list_users(user: AuthenticatedUser = Depends(require_role("admin"))):
    ...

@router.post("/content/create")
async def create_content(user: AuthenticatedUser = Depends(require_role("instructor", "admin"))):
    ...
```

### `require_verified_email` Dependency

```python
async def require_verified_email(user: AuthenticatedUser = Depends(get_current_user)):
    """
    Ensures the user's email is verified. Required for lesson access and AI tutor.
    Raises HTTPException(403, "Email verification required") if not verified.
    """
```

## JWKS Cache Strategy

```python
class JWKSManager:
    """
    Manages JWKS key fetching and caching.
    - Primary: fetch from auth server /.well-known/jwks.json
    - Cache TTL: 5 minutes
    - Fallback: last known good keys (survives auth server downtime)
    - Error: if no cached keys and server unreachable → 503 with Retry-After
    """

    jwks_url: str
    cache_ttl: int = 300  # seconds
    _cached_keys: dict | None
    _last_fetch: float
```

## Error Responses

| Status | When | Body |
|--------|------|------|
| 401 | Missing/invalid/expired token | `{"detail": "Invalid or expired token"}` |
| 403 | Insufficient role | `{"detail": "Insufficient permissions"}` |
| 403 | Email not verified | `{"detail": "Email verification required"}` |
| 503 | Auth server unreachable, no cached keys | `{"detail": "Authentication service temporarily unavailable", "retry_after": 30}` |
