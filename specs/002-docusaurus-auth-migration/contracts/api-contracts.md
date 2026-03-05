# API Contracts: Authentication & Onboarding

**Feature**: 002-docusaurus-auth-migration
**Date**: 2026-02-25
**Phase**: 1 - API Contracts

---

## Overview

This document defines the API contracts for authentication, session management, and onboarding endpoints. All endpoints are provided by the Better Auth server with custom extensions for onboarding.

**Base URL**: `http://localhost:3001` (development), `https://auth.intellistack.com` (production)
**API Prefix**: `/api/auth`

---

## Authentication Endpoints

### 1. Sign Up (Email/Password)

**Endpoint**: `POST /api/auth/sign-up/email`

**Description**: Create a new user account with email and password.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "email_verified": false,
    "onboarding_completed": false,
    "current_stage": 1,
    "role": "student",
    "created_at": "2026-02-25T23:42:00Z"
  },
  "session": {
    "token": "sess_xyz789",
    "expires_at": "2026-02-26T23:42:00Z"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid email format or password too short
  ```json
  {
    "error": "VALIDATION_ERROR",
    "message": "Password must be at least 8 characters",
    "field": "password"
  }
  ```
- `409 Conflict`: Email already registered
  ```json
  {
    "error": "EMAIL_EXISTS",
    "message": "Email already registered"
  }
  ```

**Cookies Set**:
- `better-auth.session_token`: Session token (HttpOnly, Secure in prod, SameSite=Lax)

---

### 2. Sign In (Email/Password)

**Endpoint**: `POST /api/auth/sign-in/email`

**Description**: Authenticate user with email and password.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "rememberMe": false
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "email_verified": true,
    "onboarding_completed": false,
    "current_stage": 1,
    "role": "student"
  },
  "session": {
    "token": "sess_xyz789",
    "expires_at": "2026-02-26T23:42:00Z"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid credentials
  ```json
  {
    "error": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
  ```
- `403 Forbidden`: Account locked
  ```json
  {
    "error": "ACCOUNT_LOCKED",
    "message": "Account locked due to too many failed login attempts",
    "locked_until": "2026-02-25T23:52:00Z"
  }
  ```

**Cookies Set**:
- `better-auth.session_token`: Session token

---

### 3. Sign Out

**Endpoint**: `POST /api/auth/sign-out`

**Description**: Revoke current session and clear cookies.

**Request**: Empty body

**Response** (200 OK):
```json
{
  "success": true
}
```

**Cookies Cleared**:
- `better-auth.session_token`: Removed

---

### 4. Get Session

**Endpoint**: `GET /api/auth/get-session`

**Description**: Retrieve current authenticated user session.

**Request**: No body (session token in cookie)

**Response** (200 OK):
```json
{
  "user": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "email_verified": true,
    "onboarding_completed": true,
    "current_stage": 2,
    "role": "student",
    "avatar_url": null
  },
  "session": {
    "expires_at": "2026-02-26T23:42:00Z"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: No valid session
  ```json
  {
    "error": "UNAUTHORIZED",
    "message": "No valid session found"
  }
  ```

---

### 5. OAuth Sign In (Google)

**Endpoint**: `POST /api/auth/oauth/google`

**Description**: Initiate Google OAuth flow.

**Request**:
```json
{
  "callbackURL": "http://localhost:3005/AINativeBook/auth/callback"
}
```

**Response** (200 OK):
```json
{
  "url": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&scope=openid+email+profile",
  "state": "state_abc123"
}
```

**Client Action**: Redirect user to `url`

---

### 6. OAuth Callback

**Endpoint**: `GET /api/auth/callback/google`

**Description**: Handle OAuth callback from Google (automatic redirect).

**Query Parameters**:
- `code`: Authorization code from Google
- `state`: State parameter for CSRF protection

**Response**: Redirect to `callbackURL` with session cookie set

**Error Responses**:
- Redirect to `/auth/login?error=oauth_failed` on failure

---

### 7. Get JWT Token

**Endpoint**: `GET /api/auth/token`

**Description**: Exchange session cookie for JWT token (for backend API authentication).

**Request**: No body (session token in cookie)

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9...",
  "expires_at": "2026-02-26T23:42:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: No valid session

---

## Onboarding Endpoints

### 8. Get Onboarding Status

**Endpoint**: `GET /api/auth/onboarding/status`

**Description**: Get user's onboarding completion status and current step.

**Request**: No body (session token in cookie)

**Response** (200 OK):
```json
{
  "onboarding_completed": false,
  "current_step": 2,
  "completed_steps": ["basic_info", "education"],
  "preferences": {
    "basic_info": {
      "full_name": "John Doe",
      "preferred_language": "en",
      "timezone": "America/New_York"
    },
    "education": {
      "level": "undergraduate",
      "field_of_study": "Computer Science",
      "prior_experience": "beginner"
    }
  }
}
```

**Error Responses**:
- `401 Unauthorized`: No valid session

---

### 9. Save Onboarding Step

**Endpoint**: `POST /api/auth/onboarding/step`

**Description**: Save data for a specific onboarding step.

**Request** (Step 1 - Basic Information):
```json
{
  "step": "basic_info",
  "data": {
    "full_name": "John Doe",
    "preferred_language": "en",
    "timezone": "America/New_York"
  }
}
```

**Request** (Step 2 - Educational Background):
```json
{
  "step": "education",
  "data": {
    "level": "undergraduate",
    "field_of_study": "Computer Science",
    "prior_experience": "beginner"
  }
}
```

**Request** (Step 3 - Academic Interests):
```json
{
  "step": "interests",
  "data": {
    "learning_goals": ["career_change", "professional_development"],
    "learning_style": "hands_on",
    "topics_of_interest": ["ros2", "simulation", "ai_integration"]
  }
}
```

**Request** (Step 4 - Additional Details):
```json
{
  "step": "additional",
  "data": {
    "github_username": "johndoe",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "bio": "Aspiring robotics engineer."
  }
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "onboarding_completed": false,
  "next_step": "interests"
}
```

**Response** (200 OK - Final Step):
```json
{
  "success": true,
  "onboarding_completed": true,
  "redirect_url": "/stage-1/intro"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid step data
  ```json
  {
    "error": "VALIDATION_ERROR",
    "message": "Invalid timezone format",
    "field": "timezone"
  }
  ```
- `401 Unauthorized`: No valid session

---

### 10. Complete Onboarding

**Endpoint**: `POST /api/auth/onboarding/complete`

**Description**: Mark onboarding as complete (called after Step 4).

**Request**: Empty body

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "id": "usr_abc123",
    "onboarding_completed": true,
    "current_stage": 1
  }
}
```

**Error Responses**:
- `400 Bad Request`: Onboarding steps incomplete
  ```json
  {
    "error": "INCOMPLETE_ONBOARDING",
    "message": "All onboarding steps must be completed",
    "missing_steps": ["interests", "additional"]
  }
  ```
- `401 Unauthorized`: No valid session

---

## User Profile Endpoints

### 11. Get User Profile

**Endpoint**: `GET /api/auth/user/profile`

**Description**: Get authenticated user's full profile.

**Request**: No body (session token in cookie)

**Response** (200 OK):
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar_url": null,
  "bio": "Aspiring robotics engineer.",
  "locale": "en",
  "email_verified": true,
  "onboarding_completed": true,
  "current_stage": 2,
  "role": "student",
  "preferences": {
    "basic_info": { ... },
    "education": { ... },
    "interests": { ... },
    "additional": { ... }
  },
  "created_at": "2026-02-25T23:42:00Z"
}
```

**Error Responses**:
- `401 Unauthorized`: No valid session

---

### 12. Update User Profile

**Endpoint**: `PATCH /api/auth/user/profile`

**Description**: Update user profile fields (name, bio, avatar_url).

**Request**:
```json
{
  "name": "John Smith",
  "bio": "Updated bio text",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "id": "usr_abc123",
    "name": "John Smith",
    "bio": "Updated bio text",
    "avatar_url": "https://example.com/avatar.jpg"
  }
}
```

**Error Responses**:
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: No valid session

---

## Session Management Endpoints

### 13. List User Sessions

**Endpoint**: `GET /api/auth/sessions`

**Description**: Get all active sessions for authenticated user.

**Request**: No body (session token in cookie)

**Response** (200 OK):
```json
{
  "sessions": [
    {
      "id": "sess_xyz789",
      "created_at": "2026-02-25T23:42:00Z",
      "expires_at": "2026-02-26T23:42:00Z",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
      "ip_address": "192.168.1.100",
      "is_current": true
    },
    {
      "id": "sess_abc456",
      "created_at": "2026-02-24T10:30:00Z",
      "expires_at": "2026-02-25T10:30:00Z",
      "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0...)...",
      "ip_address": "192.168.1.101",
      "is_current": false
    }
  ]
}
```

**Error Responses**:
- `401 Unauthorized`: No valid session

---

### 14. Revoke Session

**Endpoint**: `DELETE /api/auth/sessions/:session_id`

**Description**: Revoke a specific session (logout from specific device).

**Request**: No body

**Response** (200 OK):
```json
{
  "success": true,
  "revoked_session_id": "sess_abc456"
}
```

**Error Responses**:
- `403 Forbidden`: Cannot revoke current session (use /sign-out instead)
- `404 Not Found`: Session not found or doesn't belong to user
- `401 Unauthorized`: No valid session

---

## OIDC Discovery Endpoints

### 15. OpenID Configuration

**Endpoint**: `GET /.well-known/openid-configuration`

**Description**: OpenID Connect discovery endpoint.

**Response** (200 OK):
```json
{
  "issuer": "http://localhost:3001",
  "authorization_endpoint": "http://localhost:3001/api/auth/authorize",
  "token_endpoint": "http://localhost:3001/api/auth/token",
  "userinfo_endpoint": "http://localhost:3001/api/auth/userinfo",
  "jwks_uri": "http://localhost:3001/.well-known/jwks.json",
  "scopes_supported": ["openid", "profile", "email"],
  "response_types_supported": ["code", "id_token"],
  "subject_types_supported": ["public"],
  "id_token_signing_alg_values_supported": ["EdDSA"]
}
```

---

### 16. JWKS (JSON Web Key Set)

**Endpoint**: `GET /.well-known/jwks.json`

**Description**: Public keys for JWT verification.

**Response** (200 OK):
```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "base64-encoded-public-key",
      "alg": "EdDSA",
      "use": "sig",
      "kid": "key-id-123"
    }
  ]
}
```

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "ERROR_CODE",
  "message": "Human-readable error message",
  "field": "field_name",  // Optional, for validation errors
  "details": {}           // Optional, additional error context
}
```

**Common Error Codes**:
- `VALIDATION_ERROR`: Invalid request data
- `UNAUTHORIZED`: No valid session or invalid credentials
- `FORBIDDEN`: Action not allowed
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Resource already exists
- `RATE_LIMITED`: Too many requests
- `SERVER_ERROR`: Internal server error

---

## Authentication Flow

### Email/Password Registration Flow

```
1. User submits signup form
   POST /api/auth/sign-up/email

2. Server creates user, sets session cookie
   Response: 201 Created with user data

3. Client redirects to onboarding Step 1
   GET /onboarding/step-1

4. User completes Step 1, clicks "Next"
   POST /api/auth/onboarding/step

5. Repeat for Steps 2, 3, 4

6. After Step 4, mark onboarding complete
   POST /api/auth/onboarding/complete

7. Client redirects to book content
   GET /stage-1/intro
```

### OAuth (Google) Flow

```
1. User clicks "Login with Google"
   POST /api/auth/oauth/google

2. Server returns Google OAuth URL
   Response: { url: "https://accounts.google.com/..." }

3. Client redirects to Google
   window.location.href = url

4. User authorizes on Google

5. Google redirects to callback
   GET /api/auth/callback/google?code=...&state=...

6. Server exchanges code for tokens, creates/links account

7. Server redirects to Docusaurus with session cookie
   Redirect: /AINativeBook/auth/callback

8. Client checks onboarding status
   GET /api/auth/onboarding/status

9. If incomplete, redirect to onboarding
   If complete, redirect to book content
```

### Session Validation Flow

```
1. User navigates to protected route
   GET /stage-1/intro

2. Client checks session
   GET /api/auth/get-session

3. If valid session:
   - Check onboarding_completed
   - If true: render content
   - If false: redirect to /onboarding/step-1

4. If no valid session:
   - Redirect to /auth/login?returnUrl=/stage-1/intro
```

---

## Rate Limiting

All authentication endpoints are rate-limited:

- **Sign Up**: 5 requests per hour per IP
- **Sign In**: 10 requests per 15 minutes per IP
- **OAuth**: 20 requests per hour per IP
- **Other endpoints**: 100 requests per 15 minutes per user

Rate limit headers:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1708905600
```

---

## CORS Configuration

**Allowed Origins** (development):
- `http://localhost:3000` (Next.js)
- `http://localhost:3005` (Docusaurus)
- `http://localhost:8000` (Backend API)

**Allowed Origins** (production):
- `https://intellistack.com` (Next.js)
- `https://intellistack.com` (Docusaurus - same domain)
- `https://api.intellistack.com` (Backend API)

**Allowed Methods**: GET, POST, PATCH, DELETE, OPTIONS

**Allowed Headers**: Content-Type, Authorization

**Credentials**: true (cookies included)

---

## Security Headers

All responses include:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains (production only)
```

---

## API Contracts Complete

**Phase 1 Status**: API contracts defined
**Next Step**: Quickstart guide
