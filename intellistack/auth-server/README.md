# IntelliStack Auth Server

Better-Auth OIDC (OpenID Connect) server for IntelliStack Platform. Provides:

- **Email/Password Authentication**: Registration, login, password reset
- **OAuth 2.0 Social Login**: Google and GitHub authentication
- **JWT Tokens**: RS256-signed access and refresh tokens
- **JWKS Endpoint**: Token verification for downstream services
- **OIDC Discovery**: Standard OpenID Connect discovery endpoint
- **Email Verification**: Via Resend API
- **Role-Based Access Control**: student, instructor, admin roles

## Quick Start

### Prerequisites

- Node.js 20+
- PostgreSQL 16+
- Environment variables (see `.env.example`)

### Development

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run migrations
npm run migrate

# Start development server
npm run dev
```

Server runs on `http://localhost:3001`

### OIDC Discovery Endpoint

```bash
GET http://localhost:3001/.well-known/openid-configuration
```

### JWKS Endpoint

```bash
GET http://localhost:3001/.well-known/jwks.json
```

## Project Structure

```
src/
├── index.ts           # Express server entry point
├── auth.ts            # Better-Auth configuration
├── db.ts              # Drizzle ORM adapter setup
├── email.ts           # Email service (Resend)
└── hooks.ts           # Auth event logging hooks
```

## Environment Variables

Required:
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (min 32 chars)
- `RESEND_API_KEY`: Resend email service API key

Optional (for OAuth):
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
- `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`

See `.env.example` for all available options.

## API Endpoints

### Authentication

- `POST /api/auth/sign-up/email` - Email registration
- `POST /api/auth/sign-in/email` - Email login
- `POST /api/auth/sign-out` - Logout
- `GET /api/auth/get-session` - Get current session
- `POST /api/auth/forget-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

### OAuth

- `POST /api/auth/sign-in/social` - Initiate OAuth flow
- `GET /api/auth/callback/{provider}` - OAuth callback

### OIDC

- `GET /.well-known/openid-configuration` - Discovery document
- `GET /.well-known/jwks.json` - Public keys for token verification

## Docker

```bash
# Build image
docker build -t intellistack-auth-server .

# Run container
docker run -p 3001:3001 \
  -e DATABASE_URL=postgresql://... \
  -e BETTER_AUTH_SECRET=your-secret \
  intellistack-auth-server
```

## Production Deployment

1. Set `BETTER_AUTH_URL` to your production domain
2. Set `NODE_ENV=production`
3. Use strong `BETTER_AUTH_SECRET` (64+ random chars)
4. Enable `SESSION_COOKIE_SECURE=true`
5. Set proper `CORS_ORIGINS`
6. Use environment-specific OAuth credentials
7. Set up database backups and monitoring

## Documentation

- [Better-Auth Docs](https://www.better-auth.com/)
- [OIDC Provider Plugin](https://www.better-auth.com/docs/plugins/oidc-provider)
- [JWT Plugin](https://www.better-auth.com/docs/plugins/jwt)

## License

MIT
