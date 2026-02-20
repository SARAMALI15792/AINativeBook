# 🚀 Quick Deployment Checklist

## ✅ Completed
- [x] Configured Vercel deployment files
- [x] Removed static export from Next.js
- [x] Created serverless handlers for backend
- [x] Added Mangum adapter for FastAPI
- [x] Pushed changes to GitHub

## 📋 Next Steps (Do These Now)

### Step 1: Deploy to Vercel (5 minutes)
1. Go to: https://vercel.com/new
2. Click "Import Git Repository"
3. Select: `SARAMALI15792/AINativeBook`
4. Click "Deploy" (it will fail - that's expected!)

### Step 2: Set Up Database (10 minutes)

**Choose ONE option:**

**Option A: Vercel Postgres** (Easiest)
- In Vercel dashboard → Storage → Create Database → Postgres
- Copy the `DATABASE_URL` connection string

**Option B: Neon** (Free tier, recommended)
- Go to: https://neon.tech
- Sign up and create a new project
- Copy the connection string from dashboard

### Step 3: Generate Secrets (2 minutes)

Run these commands in your terminal:

```bash
# Generate BETTER_AUTH_SECRET
openssl rand -base64 32

# Generate SECRET_KEY
openssl rand -base64 32
```

Copy both outputs - you'll need them in the next step.

### Step 4: Add Environment Variables (10 minutes)

In Vercel dashboard → Your Project → Settings → Environment Variables

**Add these REQUIRED variables:**

```
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
BETTER_AUTH_SECRET=<paste from step 3>
SECRET_KEY=<paste from step 3>
BETTER_AUTH_URL=https://your-app-name.vercel.app
BETTER_AUTH_TRUST_HOST=true
NEXT_PUBLIC_AUTH_URL=https://your-app-name.vercel.app
NEXT_PUBLIC_API_URL=https://your-app-name.vercel.app/api/v1
CORS_ORIGINS=https://your-app-name.vercel.app
COOKIE_DOMAIN=.vercel.app
```

**Replace `your-app-name` with your actual Vercel domain!**

**Optional but recommended (for AI features):**

```
OPENAI_API_KEY=sk-your-key-here
QDRANT_HOST=your-cluster.qdrant.io
QDRANT_API_KEY=your-key-here
COHERE_API_KEY=your-key-here
```

### Step 5: Redeploy (2 minutes)

1. Go to Vercel dashboard → Deployments
2. Click "Redeploy" on the latest deployment
3. Wait 5-10 minutes for build to complete

### Step 6: Run Database Migrations (5 minutes)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link to your project
vercel link

# Pull environment variables
vercel env pull .env.production

# Run migrations
cd intellistack/backend
alembic upgrade head
```

### Step 7: Test Your Deployment

Visit your Vercel URL and test:

1. Homepage: `https://your-app.vercel.app`
2. Login page: `https://your-app.vercel.app/login`
3. API health: `https://your-app.vercel.app/api/v1/health`

---

## 🐛 Common Issues

### "Login not working"
- Check `BETTER_AUTH_URL` matches your Vercel domain exactly
- Verify `BETTER_AUTH_SECRET` is set
- Check browser console for errors

### "API returns 500 errors"
- Verify `DATABASE_URL` is correct
- Check Vercel function logs (Dashboard → Functions → Logs)
- Make sure migrations ran successfully

### "Build failed"
- Check Vercel build logs for specific error
- Verify all dependencies are in package.json/requirements.txt
- Make sure Python version is 3.11

---

## 📚 Full Documentation

- **Complete Guide**: See `VERCEL_DEPLOYMENT.md` in your project
- **Vercel Docs**: https://vercel.com/docs
- **Better-Auth**: https://better-auth.com

---

## ⏱️ Estimated Total Time: 30-40 minutes

**Current Status**: Ready to deploy! Start with Step 1 above.

**Last Updated**: 2026-02-20
