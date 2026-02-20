# Vercel Deployment Guide for IntelliStack Platform

## 🚀 Quick Start

This guide will help you deploy the IntelliStack platform (frontend + backend + auth server) to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code is already on GitHub
3. **PostgreSQL Database**: You'll need a hosted PostgreSQL instance
4. **Qdrant Vector Store**: For RAG chatbot functionality

---

## Step 1: Set Up PostgreSQL Database

### Option A: Vercel Postgres (Recommended)
1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Storage" → "Create Database" → "Postgres"
3. Copy the connection string (starts with `postgresql://`)

### Option B: Neon (Free Tier Available)
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string from the dashboard

### Option C: Supabase (Free Tier Available)
1. Sign up at [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings → Database → Connection String
4. Copy the connection string

---

## Step 2: Set Up Qdrant Vector Store

### Option A: Qdrant Cloud (Recommended)
1. Sign up at [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a cluster (free tier available)
3. Copy the cluster URL and API key

### Option B: Self-Hosted (Advanced)
- Deploy Qdrant to Railway, Render, or Fly.io
- Use Docker: `docker run -p 6333:6333 qdrant/qdrant`

---

## Step 3: Configure Environment Variables in Vercel

### 3.1 Import Your Project to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository: `SARAMALI15792/AINativeBook`
3. Select the root directory
4. Click "Deploy" (it will fail initially - that's expected)

### 3.2 Add Environment Variables

Go to your project → Settings → Environment Variables and add:

#### **Application Settings**
```
NODE_ENV=production
PYTHON_VERSION=3.11
```

#### **Database (PostgreSQL)**
```
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```
*Replace with your actual PostgreSQL connection string*

#### **Redis (Optional - for caching)**
```
REDIS_URL=redis://default:password@host:6379
```
*You can use Upstash Redis (free tier) or skip for now*

#### **Qdrant Vector Store**
```
QDRANT_HOST=your-cluster-url.qdrant.io
QDRANT_PORT=6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=intellistack_content
```

#### **OpenAI API**
```
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

#### **Cohere (for reranking)**
```
COHERE_API_KEY=your-cohere-api-key
```
*Get free API key at [cohere.com](https://cohere.com)*

#### **Better-Auth Configuration**
```
BETTER_AUTH_SECRET=your-random-secret-min-32-characters
BETTER_AUTH_URL=https://your-app.vercel.app
BETTER_AUTH_TRUST_HOST=true
BETTER_AUTH_ISSUER=https://your-app.vercel.app
BETTER_AUTH_AUDIENCE=intellistack-api
BETTER_AUTH_JWKS_URL=https://your-app.vercel.app/.well-known/jwks.json
```

#### **OAuth Providers (Optional)**

**Google OAuth:**
```
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-app.vercel.app/api/auth/callback/google
```

**GitHub OAuth:**
```
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=https://your-app.vercel.app/api/auth/callback/github
```

#### **Frontend Environment Variables**
```
NEXT_PUBLIC_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_API_URL=https://your-app.vercel.app/api/v1
NEXT_PUBLIC_DOCUSAURUS_URL=https://your-app.vercel.app/docs
```

#### **CORS Origins**
```
CORS_ORIGINS=https://your-app.vercel.app,https://your-app-git-main.vercel.app
```

#### **Security**
```
SECRET_KEY=your-random-secret-key-min-32-characters
ALGORITHM=EdDSA
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### **Cookie Configuration**
```
COOKIE_DOMAIN=.vercel.app
```

---

## Step 4: Generate Secrets

Run these commands locally to generate secure secrets:

```bash
# Generate BETTER_AUTH_SECRET (32+ characters)
openssl rand -base64 32

# Generate SECRET_KEY (32+ characters)
openssl rand -base64 32
```

---

## Step 5: Set Up OAuth Providers (Optional)

### Google OAuth
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable "Google+ API"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Add authorized redirect URI: `https://your-app.vercel.app/api/auth/callback/google`
6. Copy Client ID and Client Secret

### GitHub OAuth
1. Go to [github.com/settings/developers](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Set Authorization callback URL: `https://your-app.vercel.app/api/auth/callback/github`
4. Copy Client ID and Client Secret

---

## Step 6: Deploy

1. After adding all environment variables, go to "Deployments"
2. Click "Redeploy" on the latest deployment
3. Wait for build to complete (~5-10 minutes)

---

## Step 7: Run Database Migrations

After successful deployment, you need to initialize the database:

### Option A: Using Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link to your project
vercel link

# Run migrations
vercel env pull .env.production
cd intellistack/backend
alembic upgrade head
```

### Option B: Manual SQL Execution
1. Connect to your PostgreSQL database
2. Run the migration SQL files from `intellistack/backend/alembic/versions/`

---

## Step 8: Verify Deployment

Visit your Vercel URL and test:

1. **Homepage**: `https://your-app.vercel.app`
2. **Auth endpoints**: `https://your-app.vercel.app/api/auth/session`
3. **API health**: `https://your-app.vercel.app/api/v1/health`
4. **JWKS endpoint**: `https://your-app.vercel.app/.well-known/jwks.json`

---

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Make sure all dependencies are in `package.json` and `requirements.txt`

### Issue: Database connection fails
**Solution**:
- Check `DATABASE_URL` format includes `?sslmode=require`
- Verify database is accessible from Vercel's IP ranges
- Check database credentials

### Issue: Authentication not working
**Solution**:
- Verify `BETTER_AUTH_URL` matches your Vercel domain
- Check `BETTER_AUTH_SECRET` is set
- Ensure `COOKIE_DOMAIN` is correct (`.vercel.app` for Vercel)

### Issue: CORS errors
**Solution**:
- Add your Vercel domain to `CORS_ORIGINS`
- Include preview deployment URLs: `https://your-app-git-*.vercel.app`

### Issue: Serverless function timeout
**Solution**:
- Upgrade to Vercel Pro for longer timeouts (60s vs 10s)
- Optimize slow database queries
- Consider using Edge Functions for faster response

---

## Important Notes

⚠️ **Vercel Limitations:**
- Free tier has 10-second serverless function timeout
- PostgreSQL and Qdrant must be hosted separately
- Redis is optional but recommended for production

⚠️ **After First Deployment:**
- Update OAuth redirect URIs with actual Vercel domain
- Update `BETTER_AUTH_URL` and `NEXT_PUBLIC_*` variables
- Redeploy after updating environment variables

⚠️ **Security:**
- Never commit `.env` files to Git
- Rotate secrets regularly
- Use Vercel's environment variable encryption

---

## Next Steps

1. ✅ Deploy to Vercel
2. ✅ Set up database and run migrations
3. ✅ Configure OAuth providers
4. ✅ Test authentication flow
5. ✅ Test API endpoints
6. ✅ Monitor logs in Vercel dashboard

---

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Better-Auth Docs**: [better-auth.com](https://better-auth.com)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**Generated**: 2026-02-20
**Project**: IntelliStack Platform
**Deployment Target**: Vercel (Full-Stack)
