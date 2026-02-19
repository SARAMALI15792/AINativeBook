# API Contracts: Frontend Redesign & Experience Enhancement

**Feature**: 001-frontend-redesign | **Date**: 2026-02-18 | **Version**: 1.0.0

## Purpose

This document defines the API contracts between the Next.js frontend and the backend services (Better Auth + FastAPI). It specifies request/response formats, authentication requirements, error handling, and validation rules.

---

## Base URLs

| Service | Environment | Base URL |
|---------|-------------|----------|
| Auth Server | Development | `http://localhost:3001` |
| Auth Server | Production | `https://auth.intellistack.com` |
| Backend API | Development | `http://localhost:8000` |
| Backend API | Production | `https://api.intellistack.com` |

---

## Authentication

### Authentication Method

All API requests (except public endpoints) require authentication via Better Auth session cookie.

**Cookie Name**: `better-auth.session_token`
**Cookie Attributes**:
- `HttpOnly`: true
- `Secure`: true (production only)
- `SameSite`: Lax
- `Domain`: `.intellistack.com` (production) or `localhost` (development)
- `Path`: `/`
- `Max-Age`: 2592000 (30 days) or session-based

**Alternative**: Bearer token in Authorization header (for API clients)
```
Authorization: Bearer <session_token>
```

---

## Better Auth Endpoints

### 1. Register User

**Endpoint**: `POST /api/auth/signup`
**Authentication**: None (public)

**Request**:
```typescript
interface SignupRequest {
  email: string;        // Valid email format
  password: string;     // Min 8 chars, 1 uppercase, 1 lowercase, 1 number
  name: string;         // Min 2 chars, max 100 chars
}
```

**Response (Success - 201)**:
```typescript
interface SignupResponse {
  user: {
    id: string;
    email: string;
    name: string;
    emailVerified: boolean;
    image: string | null;
    createdAt: string;  // ISO 8601 timestamp
    updatedAt: string;  // ISO 8601 timestamp
  };
  session: {
    token: string;
    expiresAt: string;  // ISO 8601 timestamp
  };
}
```

**Response (Error - 400)**:
```typescript
interface SignupError {
  error: string;
  message: string;
  code: 'VALIDATION_ERROR' | 'EMAIL_EXISTS' | 'WEAK_PASSWORD';
  fields?: {
    email?: string;
    password?: string;
    name?: string;
  };
}
```

**Validation Rules**:
- Email: RFC 5322 compliant, max 255 chars
- Password: Min 8 chars, max 128 chars, must contain uppercase, lowercase, and number
- Name: Min 2 chars, max 100 chars, alphanumeric + spaces

**Example**:
```typescript
const response = await fetch('http://localhost:3001/api/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    name: 'John Doe',
  }),
  credentials: 'include', // Important: include cookies
});
```

---

### 2. Login User

**Endpoint**: `POST /api/auth/signin`
**Authentication**: None (public)

**Request**:
```typescript
interface SigninRequest {
  email: string;
  password: string;
  rememberMe?: boolean; // Optional: extend session duration
}
```

**Response (Success - 200)**:
```typescript
interface SigninResponse {
  user: {
    id: string;
    email: string;
    name: string;
    emailVerified: boolean;
    image: string | null;
    createdAt: string;
    updatedAt: string;
  };
  session: {
    token: string;
    expiresAt: string;
  };
}
```

**Response (Error - 401)**:
```typescript
interface SigninError {
  error: string;
  message: string;
  code: 'INVALID_CREDENTIALS' | 'ACCOUNT_LOCKED' | 'EMAIL_NOT_VERIFIED';
}
```

**Example**:
```typescript
const response = await fetch('http://localhost:3001/api/auth/signin', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    rememberMe: true,
  }),
  credentials: 'include',
});
```

---

### 3. Logout User

**Endpoint**: `POST /api/auth/signout`
**Authentication**: Required

**Request**: Empty body

**Response (Success - 200)**:
```typescript
interface SignoutResponse {
  success: true;
}
```

**Example**:
```typescript
const response = await fetch('http://localhost:3001/api/auth/signout', {
  method: 'POST',
  credentials: 'include',
});
```

---

### 4. Get Current Session

**Endpoint**: `GET /api/auth/session`
**Authentication**: Optional (returns null if not authenticated)

**Response (Success - 200)**:
```typescript
interface SessionResponse {
  user: {
    id: string;
    email: string;
    name: string;
    emailVerified: boolean;
    image: string | null;
    createdAt: string;
    updatedAt: string;
  } | null;
  session: {
    token: string;
    expiresAt: string;
  } | null;
}
```

**Example**:
```typescript
const response = await fetch('http://localhost:3001/api/auth/session', {
  credentials: 'include',
});
const { user, session } = await response.json();
```

---

## Backend API Endpoints

### 5. Save Personalization Preferences

**Endpoint**: `POST /api/v1/personalization/preferences`
**Authentication**: Required

**Request**:
```typescript
interface SavePreferencesRequest {
  learningGoal: 'career_transition' | 'academic_research' | 'hobby_project' | 'skill_enhancement';
  experienceLevel: 'beginner' | 'intermediate' | 'advanced';
  weeklyCommitment: number;  // 1-20
  interests: string[];       // Max 10 items, each max 50 chars
  preferredLanguage: string; // ISO 639-1 code (e.g., 'en', 'ur')
}
```

**Response (Success - 200)**:
```typescript
interface SavePreferencesResponse {
  success: true;
  data: {
    userId: string;
    learningGoal: string;
    experienceLevel: string;
    weeklyCommitment: number;
    interests: string[];
    preferredLanguage: string;
    createdAt: string;
    updatedAt: string;
  };
}
```

**Response (Error - 400)**:
```typescript
interface SavePreferencesError {
  success: false;
  error: {
    code: 'VALIDATION_ERROR' | 'INVALID_ENUM' | 'OUT_OF_RANGE';
    message: string;
    fields?: {
      learningGoal?: string;
      experienceLevel?: string;
      weeklyCommitment?: string;
      interests?: string;
      preferredLanguage?: string;
    };
  };
}
```

**Response (Error - 401)**:
```typescript
interface UnauthorizedError {
  success: false;
  error: {
    code: 'UNAUTHORIZED';
    message: 'Authentication required';
  };
}
```

**Validation Rules**:
- `learningGoal`: Must be one of enum values
- `experienceLevel`: Must be one of enum values
- `weeklyCommitment`: Integer between 1 and 20 (inclusive)
- `interests`: Array with max 10 items, each string max 50 chars
- `preferredLanguage`: Must be valid ISO 639-1 code

**Example**:
```typescript
const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`, // Or use credentials: 'include'
  },
  body: JSON.stringify({
    learningGoal: 'career_transition',
    experienceLevel: 'beginner',
    weeklyCommitment: 10,
    interests: ['robotics', 'ai', 'computer-vision'],
    preferredLanguage: 'en',
  }),
});
```

---

### 6. Get Personalization Preferences

**Endpoint**: `GET /api/v1/personalization/preferences`
**Authentication**: Required

**Response (Success - 200)**:
```typescript
interface GetPreferencesResponse {
  success: true;
  data: {
    userId: string;
    learningGoal: string;
    experienceLevel: string;
    weeklyCommitment: number;
    interests: string[];
    preferredLanguage: string;
    createdAt: string;
    updatedAt: string;
  } | null; // null if preferences not set
}
```

**Response (Error - 401)**:
```typescript
interface UnauthorizedError {
  success: false;
  error: {
    code: 'UNAUTHORIZED';
    message: 'Authentication required';
  };
}
```

**Example**:
```typescript
const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
  headers: {
    'Authorization': `Bearer ${sessionToken}`,
  },
});
const { data } = await response.json();
```

---

### 7. Update Personalization Preferences

**Endpoint**: `PATCH /api/v1/personalization/preferences`
**Authentication**: Required

**Request** (all fields optional):
```typescript
interface UpdatePreferencesRequest {
  learningGoal?: 'career_transition' | 'academic_research' | 'hobby_project' | 'skill_enhancement';
  experienceLevel?: 'beginner' | 'intermediate' | 'advanced';
  weeklyCommitment?: number;  // 1-20
  interests?: string[];       // Max 10 items
  preferredLanguage?: string; // ISO 639-1 code
}
```

**Response**: Same as Save Preferences

**Example**:
```typescript
const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${sessionToken}`,
  },
  body: JSON.stringify({
    weeklyCommitment: 15, // Only update weekly commitment
  }),
});
```

---

### 8. Delete Personalization Preferences

**Endpoint**: `DELETE /api/v1/personalization/preferences`
**Authentication**: Required

**Response (Success - 200)**:
```typescript
interface DeletePreferencesResponse {
  success: true;
  message: 'Preferences deleted successfully';
}
```

**Response (Error - 404)**:
```typescript
interface NotFoundError {
  success: false;
  error: {
    code: 'NOT_FOUND';
    message: 'Preferences not found';
  };
}
```

**Example**:
```typescript
const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${sessionToken}`,
  },
});
```

---

## Error Response Format

All API errors follow a consistent format:

```typescript
interface ApiError {
  success: false;
  error: {
    code: string;           // Machine-readable error code
    message: string;        // Human-readable error message
    fields?: Record<string, string>; // Field-level errors (validation)
    details?: any;          // Additional error details (optional)
  };
}
```

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INVALID_ENUM` | 400 | Enum value not recognized |
| `OUT_OF_RANGE` | 400 | Numeric value out of allowed range |
| `UNAUTHORIZED` | 401 | Authentication required |
| `INVALID_CREDENTIALS` | 401 | Email or password incorrect |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource already exists |
| `EMAIL_EXISTS` | 409 | Email already registered |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

## Rate Limiting

### Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/auth/signup` | 5 requests | 15 minutes |
| `/api/auth/signin` | 10 requests | 15 minutes |
| `/api/auth/signout` | 20 requests | 1 minute |
| `/api/v1/personalization/*` | 60 requests | 1 minute |

### Rate Limit Headers

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1708200000
```

### Rate Limit Exceeded Response

```typescript
interface RateLimitError {
  success: false;
  error: {
    code: 'RATE_LIMIT_EXCEEDED';
    message: 'Too many requests. Please try again later.';
    retryAfter: number; // Seconds until rate limit resets
  };
}
```

---

## CORS Configuration

### Allowed Origins

**Development**:
- `http://localhost:3000` (Next.js)
- `http://localhost:3001` (Auth Server)
- `http://localhost:3002` (Docusaurus)

**Production**:
- `https://intellistack.com`
- `https://app.intellistack.com`
- `https://learn.intellistack.com`

### CORS Headers

```
Access-Control-Allow-Origin: <origin>
Access-Control-Allow-Methods: GET, POST, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

---

## Request/Response Examples

### Complete Authentication Flow

```typescript
// 1. Register
const signupResponse = await fetch('http://localhost:3001/api/auth/signup', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    name: 'John Doe',
  }),
  credentials: 'include',
});
const { user, session } = await signupResponse.json();

// 2. Save preferences
const prefsResponse = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${session.token}`,
  },
  body: JSON.stringify({
    learningGoal: 'career_transition',
    experienceLevel: 'beginner',
    weeklyCommitment: 10,
    interests: ['robotics', 'ai'],
    preferredLanguage: 'en',
  }),
});
const { data: preferences } = await prefsResponse.json();

// 3. Redirect to Docusaurus
window.location.href = 'http://localhost:3002/learn';
```

### Error Handling Example

```typescript
async function savePreferences(data: SavePreferencesRequest) {
  try {
    const response = await fetch('http://localhost:8000/api/v1/personalization/preferences', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${sessionToken}`,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error: ApiError = await response.json();

      if (error.error.code === 'VALIDATION_ERROR' && error.error.fields) {
        // Handle field-level errors
        Object.entries(error.error.fields).forEach(([field, message]) => {
          console.error(`${field}: ${message}`);
        });
      } else if (error.error.code === 'UNAUTHORIZED') {
        // Redirect to login
        window.location.href = '/auth/login';
      } else {
        // Generic error handling
        console.error(error.error.message);
      }

      throw new Error(error.error.message);
    }

    const result: SavePreferencesResponse = await response.json();
    return result.data;
  } catch (err) {
    console.error('Network error:', err);
    throw err;
  }
}
```

---

## TypeScript Client SDK

### Recommended Client Structure

```typescript
// lib/api-client.ts
class ApiClient {
  private baseUrl: string;
  private authUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    this.authUrl = process.env.NEXT_PUBLIC_AUTH_URL || 'http://localhost:3001';
  }

  private async request<T>(
    url: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(url, {
      ...options,
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error: ApiError = await response.json();
      throw new ApiClientError(error);
    }

    return response.json();
  }

  // Auth methods
  async signup(data: SignupRequest): Promise<SignupResponse> {
    return this.request(`${this.authUrl}/api/auth/signup`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async signin(data: SigninRequest): Promise<SigninResponse> {
    return this.request(`${this.authUrl}/api/auth/signin`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async signout(): Promise<SignoutResponse> {
    return this.request(`${this.authUrl}/api/auth/signout`, {
      method: 'POST',
    });
  }

  async getSession(): Promise<SessionResponse> {
    return this.request(`${this.authUrl}/api/auth/session`);
  }

  // Preferences methods
  async savePreferences(data: SavePreferencesRequest): Promise<SavePreferencesResponse> {
    return this.request(`${this.baseUrl}/api/v1/personalization/preferences`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getPreferences(): Promise<GetPreferencesResponse> {
    return this.request(`${this.baseUrl}/api/v1/personalization/preferences`);
  }

  async updatePreferences(data: UpdatePreferencesRequest): Promise<SavePreferencesResponse> {
    return this.request(`${this.baseUrl}/api/v1/personalization/preferences`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async deletePreferences(): Promise<DeletePreferencesResponse> {
    return this.request(`${this.baseUrl}/api/v1/personalization/preferences`, {
      method: 'DELETE',
    });
  }
}

class ApiClientError extends Error {
  constructor(public error: ApiError) {
    super(error.error.message);
    this.name = 'ApiClientError';
  }
}

export const apiClient = new ApiClient();
```

---

## Testing Contracts

### Contract Testing Strategy

1. **Schema Validation**: Validate request/response against JSON schemas
2. **Mock Server**: Use MSW (Mock Service Worker) for frontend testing
3. **Integration Tests**: Test actual API endpoints with test database
4. **Contract Tests**: Use Pact or similar for consumer-driven contracts

### Example Mock Handlers (MSW)

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  // Signup
  http.post('http://localhost:3001/api/auth/signup', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      user: {
        id: '123',
        email: body.email,
        name: body.name,
        emailVerified: false,
        image: null,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
      session: {
        token: 'mock-token',
        expiresAt: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      },
    });
  }),

  // Save preferences
  http.post('http://localhost:8000/api/v1/personalization/preferences', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      success: true,
      data: {
        userId: '123',
        ...body,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
    });
  }),
];
```

---

**API Contracts Status**: ✅ Complete
**Next Step**: Create component-api.md and theme-api.md
