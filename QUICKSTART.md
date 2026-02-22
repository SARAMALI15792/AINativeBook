# Quick Start: Deploy Production Fix

## Prerequisites
- Netlify CLI: `npm install -g netlify-cli`
- Railway CLI: `npm install -g @railway/cli`

## Step 1: Update Railway CORS (5 minutes)

### Auth Server
```bash
cd intellistack/auth-server
railway link
railway variables --set "CORS_ORIGINS=https://intellistack-frontend.netlify.app,https://saramali15792.github.io,https://backend-production-bcb8.up.railway.app"
railway up
```

### Backend
```bash
cd intellistack/backend
railway link
railway variables --set "CORS_ORIGINS=https://intellistack-frontend.netlify.app,https://saramali15792.github.io,https://auth-server-production-0f46.up.railway.app,https://backend-production-bcb8.up.railway.app"
railway up
```

## Step 2: Deploy Frontend to Netlify (5 minutes)

```bash
cd intellistack/frontend

# Set environment variables
netlify env:set NEXT_PUBLIC_AUTH_URL "" --context production
netlify env:set NEXT_PUBLIC_API_URL "" --context production
netlify env:set NEXT_PUBLIC_DOCUSAURUS_URL "https://saramali15792.github.io/AINativeBook/" --context production

# Deploy
npm run build
netlify deploy --prod
```

Or use the automated script:
```bash
cd intellistack/frontend
chmod +x deploy-production.sh
./deploy-production.sh
```

## Step 3: Verify (5 minutes)

1. Go to https://intellistack-frontend.netlify.app/auth/login
2. Log in with test credentials
3. Verify redirect to /dashboard
4. Refresh page - session should persist
5. Navigate to /personalization - should load
6. Check DevTools → Console - no CORS errors
7. Check DevTools → Application → Cookies - should see `better-auth.session_token`

## Troubleshooting

### "No internet connection" error
Check Netlify `_redirects` file deployed:
```bash
netlify deploy --prod
```

### CORS errors
Verify Railway environment variables:
```bash
railway variables
```

### Cookies not set
1. Check auth-server cookie domain is `undefined`
2. Verify Netlify proxy working (Network tab)
3. Ensure `credentials: 'include'` in fetch calls

## Rollback

```bash
# Netlify
netlify rollback

# Railway
railway rollback
```

## Full Documentation

See `DEPLOYMENT_INSTRUCTIONS.md` for complete guide.
See `PRODUCTION_FIX_SUMMARY.md` for technical details.

---

**Total Time:** ~15 minutes
**Risk:** Low (backwards compatible)
