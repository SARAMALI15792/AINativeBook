# IntelliStack Platform - Vercel Deployment Summary

## ✅ Configuration Complete

Your project is now configured for Vercel deployment. Here's what was set up:

### Files Created/Modified:

1. **`vercel.json`** (root) - Main Vercel configuration
2. **`intellistack/frontend/next.config.js`** - Removed static export, enabled serverless
3. **`intellistack/backend/vercel.json`** - Backend serverless config
4. **`intellistack/backend/api/index.py`** - Vercel handler for FastAPI
5. **`intellistack/backend/requirements.txt`** - Added Mangum adapter
6. **`intellistack/auth-server/vercel.json`** - Auth server config
7. **`VERCEL_DEPLOYMENT.md`** - Complete deployment guide

---

## 🚀 Next Steps to Deploy

### 1. Push Changes to GitHub

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 2. Import to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import repository: `SARAMALI15792/AINativeBook`
3. Click "Deploy" (will fail initially - expected)

### 3. Set Up Database

**Option A: Vercel Postgres (Easiest)**
- In Vercel dashboard → Storage → Create Database → Postgres
- Copy connection string

**Option B: Neon (Free Tier)**
- Sign up at [neon.tech](https://neon.tech)
- Create project, copy connection string

### 4. Configure Environment Variables

In Vercel dashboard → Settings → Environment Variables, add:

**Critical Variables (Required):**
```
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=<generate with: openssl rand -base64 32>
SECRET_KEY=<generate with: openssl rand -base64 32>
BETTER_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_API_URL=https://your-app.vercel.app/api/v1
```

**AI Services (Required for full functionality):**
```
OPENAI_API_KEY=sk-...
QDRANT_HOST=your-cluster.qdrant.io
QDRANT_API_KEY=...
COHERE_API_KEY=...
```

**See `VERCEL_DEPLOYMENT.md` for complete list**

### 5. Redeploy

After adding environment variables:
- Go to Deployments tab
- Click "Redeploy" on latest deployment

### 6. Run Database Migrations

```bash
# Install Vercel CLI
npm i -g vercel

# Login and link project
vercel login
vercel link

# Pull environment variables
vercel env pull .env.production

# Run migrations
cd intellistack/backend
alembic upgrade head
```

---

## 🔧 What Changed

### Frontend (Next.js)
- ❌ Removed `output: 'export'` (enables server-side features)
- ❌ Removed `basePath: '/AINativeBook'` (deploy to root)
- ✅ Added API rewrites for `/api/auth/*` and `/api/v1/*`
- ✅ Enabled image optimization

### Backend (FastAPI)
- ✅ Created Vercel serverless handler with Mangum adapter
- ✅ Added `mangum>=0.17.0` to requirements.txt
- ✅ Configured Python 3.11 runtime

### Auth Server (Better-Auth)
- ✅ Configured for Vercel Node.js runtime
- ✅ Routes all `/api/auth/*` requests properly

---

## ⚠️ Important Notes

### Limitations on Vercel Free Tier:
- 10-second serverless function timeout
- 100GB bandwidth/month
- 6,000 build minutes/month

### After First Deployment:
1. Update `BETTER_AUTH_URL` with actual Vercel domain
2. Update OAuth redirect URIs (Google/GitHub)
3. Update `NEXT_PUBLIC_*` environment variables
4. Redeploy after updating variables

### Database Requirements:
- PostgreSQL must be hosted separately (Vercel Postgres, Neon, Supabase)
- Qdrant must be hosted separately (Qdrant Cloud or self-hosted)
- Redis is optional but recommended

---

## 📚 Documentation

- **Full Guide**: `VERCEL_DEPLOYMENT.md`
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Better-Auth**: [better-auth.com](https://better-auth.com)

---

## 🐛 Troubleshooting

### Login not working?
- Check `BETTER_AUTH_URL` matches your domain
- Verify `BETTER_AUTH_SECRET` is set
- Check browser console for CORS errors

### API errors?
- Verify `DATABASE_URL` is correct
- Check Vercel function logs
- Ensure migrations ran successfully

### Build failures?
- Check all dependencies in `package.json` and `requirements.txt`
- Verify Python version is 3.11
- Check Vercel build logs for specific errors

---

**Ready to deploy!** Follow the steps above and refer to `VERCEL_DEPLOYMENT.md` for detailed instructions.

Generated: 2026-02-20
