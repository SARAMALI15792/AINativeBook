# 🚀 Quick Deployment Guide

**After rotating credentials, run ONE command to deploy everything:**

## Windows
```cmd
deploy-railway.bat
```

## Linux/Mac
```bash
chmod +x deploy-railway.sh health-check.sh
./deploy-railway.sh
```

## What These Scripts Do

### `deploy-railway.bat` / `deploy-railway.sh`
- Checks Railway authentication
- Confirms credential rotation completed
- Deploys all three services sequentially
- Shows initial logs from each service
- **Safety:** Requires explicit "yes" confirmation

### `health-check.sh`
- Tests all health endpoints
- Checks Railway logs for errors
- Provides deployment success summary
- **Run after deployment completes** (5-10 minutes)

## Manual Deployment (Alternative)

If you prefer manual control:

```bash
# Backend
cd intellistack/backend
railway link --service backend
railway up --detach

# Auth Server
cd ../auth-server
railway link --service auth-server
railway up --detach

# Content
cd ../content
railway link --service content
railway up --detach
```

## Verification

```bash
# Check health endpoints
curl https://<backend-domain>/health
curl https://<auth-domain>/health
curl https://<content-domain>/

# Or use automated health check
./health-check.sh
```

## Troubleshooting

If deployment fails:
1. Check Railway logs: `railway logs --service <service-name>`
2. Verify environment variables in Railway dashboard
3. Check Root Directory settings (no trailing spaces)
4. See `DEPLOYMENT_CHECKLIST.md` for detailed steps

---

**⚠️ REMINDER:** You must complete credential rotation BEFORE running these scripts!

See `SECURITY_INCIDENT_2026-02-21.md` for rotation procedures.
