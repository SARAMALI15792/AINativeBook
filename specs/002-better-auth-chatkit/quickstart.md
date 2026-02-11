# Quickstart: Better-Auth OIDC Server + ChatKit AI Tutor

## Prerequisites

- Node.js 20+ (for Better-Auth server)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL (Neon connection string)
- Docker & Docker Compose
- Google Cloud OAuth credentials
- GitHub OAuth App credentials
- OpenAI API key
- Resend API key (or SMTP credentials)

## Environment Variables

### Auth Server (.env)
```env
# Database
DATABASE_URL=postgresql://...@neon.tech/intellistack

# Server
PORT=3001
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_SECRET=<random-32-char-secret>

# OAuth Providers
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...

# Email (Resend)
RESEND_API_KEY=re_...

# Frontend URL (for CORS and redirects)
FRONTEND_URL=http://localhost:3000
```

### FastAPI Backend (.env)
```env
# Existing vars plus:
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_JWKS_URL=http://localhost:3001/.well-known/jwks.json
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3001
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Development Setup

### 1. Start Auth Server
```bash
cd intellistack/auth-server
npm install
npm run dev  # starts on port 3001
```

### 2. Run Database Migration
```bash
cd intellistack/auth-server
npx better-auth migrate  # creates Better-Auth tables
npm run migrate:data      # migrates existing user data
```

### 3. Start FastAPI Backend
```bash
cd intellistack/backend
pip install -r requirements.txt
python start_server.py  # starts on port 8000
```

### 4. Start Frontend
```bash
cd intellistack/frontend
npm install
npm run dev  # starts on port 3000
```

### Docker Compose (all services)
```bash
docker compose up -d
```

## Verification Checklist

- [ ] Auth server responds at `http://localhost:3001/.well-known/openid-configuration`
- [ ] JWKS endpoint returns keys at `http://localhost:3001/.well-known/jwks.json`
- [ ] Registration creates user and sends verification email
- [ ] Login returns session with JWT containing role claim
- [ ] Google OAuth redirects correctly and creates/links account
- [ ] FastAPI validates JWT tokens via JWKS
- [ ] ChatKit endpoint responds at `http://localhost:8000/api/v1/chatkit`
- [ ] Chat widget renders on lesson pages
- [ ] AI tutor responds with streaming text
- [ ] Conversation persists across page reloads
