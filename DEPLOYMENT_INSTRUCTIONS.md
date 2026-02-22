# IntelliStack Production Deployment Instructions

## Overview

This guide provides step-by-step instructions to deploy the complete fix for IntelliStack's production issues, including:
- Cross-origin cookie authentication fix via Netlify proxy
- Protected route middleware
- OAuth callback URL fixes
- Enhanced error logging

## Architecture

**Before (Broken):**
```
Browser → Netlify (frontend) → Railway (auth-server) ❌ Cookies don't work cross-origin
```

**After (Fixed):**
```
Browser → Netlify (frontend + proxy) → Railway (auth-server) ✅ Same-origin from browser perspective
```

## Prerequisites

- Netlify CLI installed: `npm install -g netlify-cli`
- Railway CLI installed: `npm install -g @railway/cli`
- Access to Railway project
- Access to Netlify site

## Step 1: Verify Local Changes

All code changes have been applied. Verify the following files were updated:

### Frontend Changes
- ✅ `intellistack/frontend/public/_redirects` (NEW) - Netlify proxy rules
- ✅ `intellistack/frontend/src/middleware.ts` (NEW) - Route protection
- ✅ `intellistack/frontend/.env.production` - Empty URL env vars
- ✅ `intellistack/frontend/src/lib/auth.ts` - Empty baseURL, OAuth fixes, error logging
- ✅ `intellistack/frontend/src/lib/api-client.ts` - Empty baseURL
- ✅ `intellistack/frontend/src/app/personalization/page.tsx` - Auth guard
- ✅ `intellistack/frontend/next.config.js` - Keep console errors

### Auth Server Changes
- ✅ `intellistack/auth-server/src/auth.ts` - Cookie domain set to undefined

## Step 2: Update Railway Environment Variables

### Auth Server

```bash
# Login to Railway
railway login

# Link to auth-server service
cd intellistack/auth-server
railway link

# Set CORS origins
railway variables --set "CORS_ORIGINS=https://intellistack-frontend.netlify.app,https://saramali15792.github.io,https://backend-production-bcb8.up.railway.app"

# Verify
railway variables

# Redeploy
railway up
```

### Backend API

```bash
# Link to backend service
cd intellistack/backend
railway link

# Set CORS origins
railway variables --set "CORS_ORIGINS=https://intellistack-frontend.netlify.app,https://saramali15792.github.io,https://auth-server-production-0f46.up.railway.app,https://backend-production-bcb8.up.railway.app"

# Verify
railway variables

# Redeploy
railway up
```

## Step 3: Commit and Push Auth Server Changes

```bash
cd intellistack/auth-server
git add src/auth.ts
git commit -m "fix: Set cookie domain to undefined for Netlify proxy compatibility"
git push origin main
```

Wait for Railway to automatically redeploy the auth-server.

## Step 4: Deploy Frontend to Netlify

```bash
cd intellistack/frontend

# Set environment variables
netlify env:set NEXT_PUBLIC_AUTH_URL "" --context production
netlify env:set NEXT_PUBLIC_API_URL "" --context production
netlify env:set NEXT_PUBLIC_DOCUSAURUS_URL "https://saramali15792.github.io/AINativeBook/" --context production

# Build and deploy
npm run build
netlify deploy --prod
```

Or use the deployment script:

```bash
cd intellistack/frontend
chmod +x deploy-production.sh
./deploy-production.sh
```

## Step 5: Verification Checklist

### Auth Flow Test
1. Navigate to `https://intellistack-frontend.netlify.app/auth/login`
2. Open DevTools → Network tab
3. Submit valid credentials
4. Verify:
   - ✅ Request goes to `/api/auth/sign-in/email` (relative path)
   - ✅ Response includes `Set-Cookie` header
   - ✅ Redirect to `/dashboard`
5. Open DevTools → Application → Cookies
6. Verify:
   - ✅ Cookie `better-auth.session_token` exists
   - ✅ Cookie domain is `.netlify.app`
7. Refresh the page
8. Verify:
   - ✅ Session persists (no redirect to login)
9. Navigate to `/personalization`
10. Verify:
    - ✅ Page loads without redirect
    - ✅ No console errors

### OAuth Flow Test
1. Click "Sign in with Google"
2. Complete OAuth flow
3. Verify:
   - ✅ Redirects back to Netlify domain (not Railway)
   - ✅ Session is established
   - ✅ Cookie is set

### Protected Routes Test
1. Log out
2. Try accessing `/dashboard` directly
3. Verify:
   - ✅ Redirects to `/auth/login?redirect=/dashboard`
4. Log in
5. Verify:
   - ✅ Redirects back to `/dashboard`

### API Calls Test
1. Log in and navigate to `/dashboard`
2. Open DevTools → Network tab
3. Verify:
   - ✅ API calls go to `/api/v1/*` (relative paths)
   - ✅ No CORS errors in console
   - ✅ Requests include cookies automatically

### Documentation Links Test
1. Navigate to curriculum page
2. Click any documentation link
3. Verify:
   - ✅ Opens `https://saramali15792.github.io/AINativeBook/docs/...`
   - ✅ Page loads successfully (no 404)

## Step 6: Monitor for Issues

### Check Netlify Logs
```bash
netlify logs
```

### Check Railway Logs
```bash
# Auth server
cd intellistack/auth-server
railway logs

# Backend
cd intellistack/backend
railway logs
```

### Common Issues and Solutions

#### Issue: "No internet connection" error
**Solution:** Check Netlify `_redirects` file is deployed correctly
```bash
netlify deploy --prod --dir=.next
```

#### Issue: CORS errors still appearing
**Solution:** Verify Railway environment variables are set correctly
```bash
railway variables
```

#### Issue: Cookies not being set
**Solution:**
1. Check auth-server cookie domain is `undefined`
2. Verify Netlify proxy is working (check Network tab)
3. Ensure `credentials: 'include'` in all fetch calls

#### Issue: OAuth redirects to Railway domain
**Solution:** Check `socialSignIn` function uses `window.location.origin`

## Rollback Plan

If critical issues occur:

### Rollback Netlify
```bash
netlify rollback
```

### Rollback Railway
```bash
# Auth server
cd intellistack/auth-server
railway rollback

# Backend
cd intellistack/backend
railway rollback
```

### Revert Environment Variables
```bash
# Auth server
railway variables --set "CORS_ORIGINS=<previous-value>"

# Backend
railway variables --set "CORS_ORIGINS=<previous-value>"
```

## Success Criteria

✅ Users can log in with email/password
✅ Users can log in with Google/GitHub OAuth
✅ Sessions persist across page refreshes
✅ Protected routes redirect unauthenticated users
✅ Personalization page loads for authenticated users
✅ Documentation links work correctly
✅ No CORS errors in browser console
✅ No cookie warnings in browser console
✅ API calls succeed with proper authentication

## Support

If issues persist after following this guide:
1. Check browser console for errors
2. Check Netlify function logs
3. Check Railway service logs
4. Verify all environment variables are set correctly
5. Ensure DNS propagation is complete (can take up to 48 hours)

## URLs Reference

- **Frontend:** https://intellistack-frontend.netlify.app
- **Auth Server:** https://auth-server-production-0f46.up.railway.app
- **Backend API:** https://backend-production-bcb8.up.railway.app
- **Documentation:** https://saramali15792.github.io/AINativeBook/

---

**Last Updated:** 2026-02-22
**Status:** Ready for deployment
