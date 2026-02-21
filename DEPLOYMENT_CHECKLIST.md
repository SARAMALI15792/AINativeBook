# IntelliStack Deployment Checklist

**Last Updated:** 2026-02-21 23:33 UTC
**Status:** Phase 1 Complete - Ready for Credential Rotation

## ✅ Phase 0: Emergency Fixes (COMPLETED)

- [x] Backend railway.toml created with DOCKERFILE builder
- [x] Content railway.toml fixed to use DOCKERFILE builder
- [x] CI/CD path filters corrected in .github/workflows/railway-deploy.yml
- [x] All services configured for Railway deployment

## ✅ Phase 1: Security Remediation (COMPLETED)

- [x] Debug print statements removed from middleware.py
- [x] .gitignore enhanced to block all .env variants
- [x] .dockerignore files verified (all services)
- [x] Security incident report created (SECURITY_INCIDENT_2026-02-21.md)
- [x] Changes committed to git

## ⚠️ CRITICAL: User Action Required (BLOCKING DEPLOYMENT)

**You must complete these steps before deploying to production:**

### 1. Rotate Database Password (5 minutes)
```bash
# Go to: https://console.neon.tech
# Select: IntelliStack project
# Navigate: Settings → Reset Password
# Copy new DATABASE_URL
```

### 2. Rotate Google OAuth Credentials (10 minutes)
```bash
# Go to: https://console.cloud.google.com/apis/credentials
# Delete old OAuth client
# Create new OAuth 2.0 Client ID
# Add authorized redirect URIs:
#   - https://<auth-railway-domain>/api/auth/callback/google
#   - http://localhost:3001/api/auth/callback/google
```

### 3. Generate New Secrets (2 minutes)
```bash
# Better-Auth secret
openssl rand -base64 32

# Backend secret key
openssl rand -base64 32
```

### 4. Configure Railway Environment Variables (15 minutes)

#### Backend Service Variables
```
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<new-secret-from-step-3>
DATABASE_URL=<new-database-url-from-step-1>
REDIS_URL=<railway-redis-url>
QDRANT_HOST=<railway-qdrant-host>
QDRANT_PORT=6333
OPENAI_API_KEY=<real-openai-key>
BETTER_AUTH_URL=<railway-auth-server-url>
BETTER_AUTH_JWKS_URL=<railway-auth-server-url>/.well-known/jwks.json
BETTER_AUTH_SECRET=<new-secret-from-step-3>
CORS_ORIGINS=<production-domains-comma-separated>
```

#### Auth Server Variables
```
NODE_ENV=production
PORT=3001
BETTER_AUTH_URL=<railway-auth-server-url>
BETTER_AUTH_SECRET=<new-secret-from-step-3>
DATABASE_URL=<new-database-url-from-step-1>
GOOGLE_CLIENT_ID=<new-client-id-from-step-2>
GOOGLE_CLIENT_SECRET=<new-client-secret-from-step-2>
CORS_ORIGINS=<production-domains-comma-separated>
```

#### Content Service Variables
```
BETTER_AUTH_URL=<railway-auth-server-url>
BACKEND_URL=<railway-backend-url>
FRONTEND_URL=<railway-content-url>
SITE_URL=<railway-content-url>
```

### 5. Verify Railway Dashboard Configuration (CRITICAL)

**Check for trailing spaces in Root Directory fields:**

- Backend Root Directory: `intellistack/backend` (NO trailing spaces)
- Auth Server Root Directory: `intellistack/auth-server` (NO trailing spaces)
- Content Root Directory: `intellistack/content` (NO trailing spaces)

**How to fix trailing spaces:**
1. Click in Root Directory field
2. Press Ctrl+A (select all)
3. Press Delete (clear completely)
4. Type path character-by-character (no copy-paste)
5. Click OUTSIDE field immediately (don't press Tab/Space)
6. Verify no spaces at end
7. Click "Redeploy"

## 🚀 Phase 2: Manual Deployment (After Credential Rotation)

### Deploy Backend
```bash
cd intellistack/backend
railway link --service backend
railway up --detach
railway logs
```

**Expected output:**
- "Building from intellistack/backend"
- "Running: alembic upgrade head"
- "INFO: Uvicorn running on http://0.0.0.0:8000"
- Health check passes

### Deploy Auth Server
```bash
cd ../auth-server
railway link --service auth-server
railway up --detach
railway logs
```

**Expected output:**
- "Server listening on port 3001"
- Health check passes

### Deploy Content Service
```bash
cd ../content
railway link --service content
railway up --detach
railway logs
```

**Expected output:**
- "npm run build" completes
- "Serving build directory"
- Health check passes

## ✅ Phase 3: Verification

### Test Health Endpoints
```bash
# Backend
curl https://<backend-domain>/health
# Expected: {"status": "healthy", "version": "0.1.0", ...}

# Auth Server
curl https://<auth-domain>/health
# Expected: {"status": "ok"}

# Content
curl https://<content-domain>/
# Expected: HTML content (Docusaurus homepage)
```

### Check Railway Logs for Errors
```bash
railway logs --service backend | grep -i error
railway logs --service auth-server | grep -i error
railway logs --service content | grep -i error
```

**Expected:** No errors

### Test Service Integration
- [ ] Backend can connect to database
- [ ] Backend can connect to Redis
- [ ] Backend can connect to Qdrant
- [ ] Auth server can validate JWT tokens
- [ ] Content can load from backend API

## 📋 Optional: Git History Cleanup (After Deployment Success)

**WARNING: This rewrites git history - coordinate with team first**

```bash
# Backup repository
cd ..
git clone physicalhumoniodbook physicalhumoniodbook-backup

# Install git-filter-repo
pip install git-filter-repo

# Remove .env files from history
cd physicalhumoniodbook
git filter-repo --path intellistack/backend/.env --invert-paths --force
git filter-repo --path intellistack/backend/.env.production --invert-paths --force
git filter-repo --path intellistack/auth-server/.env --invert-paths --force
git filter-repo --path intellistack/content/.env --invert-paths --force

# Force push (WARNING: Destructive)
git push origin --force --all
git push origin --force --tags
```

## 🔒 Post-Deployment Security Hardening

### Recommended Actions
- [ ] Enable GitHub secret scanning alerts
- [ ] Add pre-commit hook for secret detection (gitleaks or detect-secrets)
- [ ] Implement secret rotation policy (every 90 days)
- [ ] Add security scanning to CI/CD pipeline
- [ ] Enable Railway deployment notifications
- [ ] Set up monitoring and alerting

### Future Improvements (Phase 7+)
- [ ] Implement Redis-based rate limiting (currently in-memory)
- [ ] Add request correlation IDs to all logs
- [ ] Configure production CORS (remove localhost origins)
- [ ] Add Prometheus metrics endpoints
- [ ] Implement structured JSON logging
- [ ] Add database connection pool monitoring

## 📊 Success Criteria

### Must Pass Before Production
- [ ] All credentials rotated
- [ ] Railway environment variables configured
- [ ] All three services deploy successfully
- [ ] Health checks pass for all services
- [ ] No errors in Railway logs
- [ ] Database migrations completed
- [ ] Services can communicate with each other

### Should Pass (Post-Deployment)
- [ ] Backend startup time < 30 seconds
- [ ] Auth startup time < 15 seconds
- [ ] Content startup time < 20 seconds
- [ ] Health check response time < 500ms
- [ ] No secrets in container images
- [ ] All containers run as non-root users

## 🆘 Rollback Plan

### If Deployment Fails
1. Railway automatically keeps previous deployment
2. Click "Rollback" in Railway dashboard
3. Check logs for error details
4. Fix issue and redeploy

### If Credentials Don't Work
1. Verify environment variables in Railway dashboard
2. Check for typos or missing values
3. Ensure URLs don't have trailing slashes
4. Redeploy after fixing

## 📞 Support

- Railway Documentation: https://docs.railway.app
- Neon Documentation: https://neon.tech/docs
- Google OAuth Setup: https://developers.google.com/identity/protocols/oauth2

---

**Next Step:** Complete credential rotation (Steps 1-4 above), then proceed with deployment (Phase 2)
