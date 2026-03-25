# Scenario: Django REST Framework Port

**Source:** IntelliStack FastAPI + SQLAlchemy (async)
**Target:** Django 5.x + Django REST Framework + SimpleJWT

---

## Prompt to Use

```
Convert IntelliStack backend to Django REST Framework.
Keep PostgreSQL. Use SimpleJWT for auth token verification.
```

## What the Agent Produces

### 1. Project Structure
```
intellistack_django/
├── config/
│   ├── settings.py        ← env vars, INSTALLED_APPS, database
│   └── urls.py            ← root router
├── apps/
│   ├── auth/              ← login, register, OAuth callback
│   ├── users/             ← profile, roles
│   ├── learning/          ← stages, lessons, progress
│   ├── content/           ← MDX authoring, review workflow
│   ├── institution/       ← cohorts, enrollment, webhooks
│   └── rag/               ← chatbot, retrieval, citations
└── manage.py
```

### 2. Auth
- `apps/auth/views.py` — register, login returning JWT pair
- `apps/auth/serializers.py` — UserSerializer, LoginSerializer
- JWKS verification middleware for tokens issued by Better-Auth

### 3. Models (from SQLAlchemy → Django ORM)

```python
# apps/learning/models.py
from django.db import models

class Stage(models.Model):
    name        = models.CharField(max_length=100)
    order       = models.IntegerField()
    is_locked   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

class LearningProgress(models.Model):
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    stage       = models.ForeignKey(Stage, on_delete=models.CASCADE)
    completed   = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True)
```

### 4. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Key Differences to Note

| IntelliStack (FastAPI)       | Django Equivalent                        |
|-----------------------------|------------------------------------------|
| `async def` route handlers  | Sync views (or `async_to_sync` wrapper)  |
| `AsyncSession` SQLAlchemy   | Django ORM QuerySet (sync)               |
| Pydantic schema validation  | DRF Serializer                           |
| `Depends(get_current_user)` | `@permission_classes([IsAuthenticated])` |
| `StreamingResponse` (SSE)   | `StreamingHttpResponse` with generator  |
| Alembic migrations          | `manage.py migrate`                      |

## SSE Warning

Django is synchronous by default. For SSE streaming (RAG chatbot):
- Use Django Channels (ASGI) + `StreamingHttpResponse`
- Or use `django-eventstream` package
- Confirm with: `"Migrate the RAG streaming endpoint to Django Channels"`

## Required Dependencies

```
django>=5.0
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
psycopg[async]>=3.1
django-cors-headers>=4.3
celery>=5.3       # for async tasks (webhook retries)
redis>=5.0
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:5432/intellistack
SECRET_KEY=<django-secret-key>
JWKS_URI=https://your-auth-server/.well-known/jwks.json
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
```
