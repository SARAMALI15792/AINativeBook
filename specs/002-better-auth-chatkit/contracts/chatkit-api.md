# ChatKit API Contract (FastAPI Backend)

**Base URL**: `http://localhost:8000` (dev) / `https://api.intellistack.app` (prod)

## ChatKit Endpoint

### POST `/api/v1/chatkit`
Single endpoint handling all ChatKit protocol operations (thread management, message sending, history loading). The ChatKit SDK sends different operation types via the request body.

**Authentication**: JWT Bearer token (RS256, validated via JWKS)
```
Authorization: Bearer <access_token>
```

**Request Body**: ChatKit protocol (managed by SDK). The body varies by operation:

#### Create Thread
```json
{
  "type": "threads.create",
  "metadata": {
    "courseId": "course-uuid",
    "lessonStage": 3,
    "pageUrl": "/learn/stage-3/ros2-topics",
    "pageTitle": "ROS 2 Topics & Services"
  }
}
```

#### Send Message
```json
{
  "type": "threads.runs.create",
  "thread_id": "thread-uuid",
  "input": [
    {
      "type": "message",
      "role": "user",
      "content": "What is the difference between a topic and a service in ROS 2?"
    }
  ],
  "metadata": {
    "pageContext": {
      "url": "/learn/stage-3/ros2-topics",
      "title": "ROS 2 Topics & Services",
      "headings": ["Publisher-Subscriber Pattern", "Service-Client Pattern"],
      "selectedText": "Topics use publish-subscribe pattern for continuous data streams"
    }
  }
}
```

#### List Threads
```json
{
  "type": "threads.list",
  "limit": 20,
  "order": "desc"
}
```

#### Load Thread Items
```json
{
  "type": "threads.items.list",
  "thread_id": "thread-uuid",
  "limit": 50,
  "order": "asc"
}
```

#### Delete Thread
```json
{
  "type": "threads.delete",
  "thread_id": "thread-uuid"
}
```

**Response**: Varies by operation type.

For message sending, returns SSE stream:
```
Content-Type: text/event-stream

event: thread.item.created
data: {"type":"message","role":"assistant","content":""}

event: thread.item.delta
data: {"type":"text","text":"That's a great question! Let me "}

event: thread.item.delta
data: {"type":"text","text":"ask you something first..."}

event: thread.item.completed
data: {"type":"message","id":"msg-id","role":"assistant","content":"That's a great question! Let me ask you something first..."}

event: done
data: {}
```

For thread listing, returns JSON:
```json
{
  "data": [
    {
      "id": "thread-uuid",
      "title": "ROS 2 Topics Discussion",
      "metadata": { "courseId": "...", "lessonStage": 3 },
      "created_at": "2026-02-11T10:00:00Z",
      "updated_at": "2026-02-11T14:30:00Z"
    }
  ],
  "has_more": false
}
```

**Errors**:
- `401` Unauthorized (invalid/missing JWT)
- `403` Forbidden (email not verified, or student accessing locked stage content)
- `429` Rate Limited (20 messages/day exceeded for students)
  ```json
  {
    "error": "daily_limit_reached",
    "message": "You've reached your daily message limit (20/20). Resets in 4h 23m.",
    "resets_at": "2026-02-12T10:00:00Z"
  }
  ```

## Context Injection Contract

The frontend injects context via the ChatKit `fetch` override and request metadata:

### Request Headers (injected by custom fetch)
```
Authorization: Bearer <jwt_access_token>
X-User-Id: <user-id>
X-User-Role: <student|instructor|admin>
X-User-Stage: <current-unlocked-stage>
```

### Message Metadata (injected per message)
```json
{
  "pageContext": {
    "url": "/learn/stage-3/ros2-topics",
    "title": "ROS 2 Topics & Services",
    "headings": ["Section 1", "Section 2"],
    "selectedText": "user-highlighted text (optional)"
  }
}
```

## Rate Limit Response Headers

Every ChatKit response includes rate limit info:
```
X-RateLimit-Limit: 20
X-RateLimit-Remaining: 15
X-RateLimit-Reset: 2026-02-12T10:00:00Z
```

Instructors and admins receive:
```
X-RateLimit-Limit: unlimited
X-RateLimit-Remaining: unlimited
```
