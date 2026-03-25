# Scenario: Go Fiber Port

**Source:** IntelliStack FastAPI + SQLAlchemy
**Target:** Go Fiber v2 + GORM + golang-jwt

---

## Prompt to Use

```
Port IntelliStack backend to Go Fiber.
Use GORM for database and golang-jwt for token verification.
```

## What the Agent Produces

### 1. Project Structure
```
intellistack-go/
├── cmd/server/main.go        ← app entry, fiber app setup
├── internal/
│   ├── auth/                 ← handlers, middleware, jwt
│   ├── users/                ← handlers, service, repository
│   ├── learning/             ← stage unlock logic, progress
│   ├── content/              ← authoring, review workflow
│   ├── institution/          ← cohorts, webhooks
│   └── rag/                  ← chatbot SSE, Qdrant client
├── pkg/
│   ├── database/             ← GORM connection, auto-migrate
│   └── config/               ← env loading
└── go.mod
```

### 2. Auth Middleware (JWT from Better-Auth JWKS)

```go
// internal/auth/middleware.go
func JWTMiddleware(jwksURL string) fiber.Handler {
    return func(c *fiber.Ctx) error {
        token := c.Get("Authorization")
        // validate RS256 token against JWKS endpoint
        claims, err := validateJWT(token, jwksURL)
        if err != nil {
            return c.Status(401).JSON(fiber.Map{"error": "unauthorized"})
        }
        c.Locals("user", claims)
        return c.Next()
    }
}
```

### 3. GORM Models (from SQLAlchemy)

```go
// internal/learning/models.go
type Stage struct {
    gorm.Model
    Name     string `gorm:"not null"`
    Order    int    `gorm:"not null"`
    IsLocked bool   `gorm:"default:true"`
}

type LearningProgress struct {
    gorm.Model
    UserID      uint
    StageID     uint
    Completed   bool
    CompletedAt *time.Time
}
```

### 4. SSE Streaming (RAG Chatbot)

Go Fiber supports SSE natively:
```go
app.Get("/api/v1/rag/chat", middleware.JWTMiddleware(cfg.JWKSURI), func(c *fiber.Ctx) error {
    c.Set("Content-Type", "text/event-stream")
    c.Set("Cache-Control", "no-cache")
    // stream OpenAI chunks via channel
})
```

## Key Differences to Note

| IntelliStack (FastAPI)       | Go Fiber Equivalent                   |
|-----------------------------|---------------------------------------|
| `async def` + `await`       | goroutines + channels                 |
| SQLAlchemy async session     | GORM (sync, connection-pooled)        |
| Pydantic validation          | `go-playground/validator`             |
| `Depends(get_current_user)` | `c.Locals("user")` after middleware   |
| Alembic migrations           | `db.AutoMigrate(&Model{})` on startup |
| Python `httpx` async client  | `net/http` or `resty`                 |

## Required Dependencies

```go
// go.mod
require (
    github.com/gofiber/fiber/v2 v2.52.x
    gorm.io/gorm v1.25.x
    gorm.io/driver/postgres v1.5.x
    github.com/golang-jwt/jwt/v5 v5.2.x
    github.com/redis/go-redis/v9 v9.x
    github.com/go-playground/validator/v10 v10.x
)
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@host:5432/intellistack
JWKS_URI=https://your-auth-server/.well-known/jwks.json
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
REDIS_URL=redis://localhost:6379
PORT=8000
```
