# Railway Service Configuration Fix

## Issue
Railway is building from the project root instead of the service-specific directories. The `RAILWAY_ROOT_DIRECTORY` environment variable is not being recognized.

## Solution
Configure each service's root directory through the Railway dashboard.

## Steps to Fix

### 1. Open Railway Dashboard
```
https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c
```

### 2. Configure Backend Service

1. Click on the **backend** service
2. Go to **Settings** tab
3. Scroll to **Source** section
4. Set **Root Directory**: `intellistack/backend`
5. Set **Build Command**: (leave empty, Dockerfile will handle it)
6. Set **Start Command**: (leave empty, Dockerfile will handle it)
7. Click **Save**
8. Click **Deploy** to redeploy

### 3. Configure Auth-Server Service

1. Click on the **auth-server** service
2. Go to **Settings** tab
3. Scroll to **Source** section
4. Set **Root Directory**: `intellistack/auth-server`
5. Set **Build Command**: (leave empty, Dockerfile will handle it)
6. Set **Start Command**: (leave empty, Dockerfile will handle it)
7. Click **Save**
8. Click **Deploy** to redeploy

### 4. Configure Content Service

1. Click on the **content** service
2. Go to **Settings** tab
3. Scroll to **Source** section
4. Set **Root Directory**: `intellistack/content`
5. Set **Build Command**: `npm ci && npm run build`
6. Set **Start Command**: `npx serve build -s -p $PORT`
7. Click **Save**
8. Click **Deploy** to redeploy

## Alternative: Use Railway CLI with Correct Context

If the dashboard method doesn't work, we can link each service to its directory:

```bash
# Backend
cd intellistack/backend
railway link --service backend
railway up

# Auth-Server
cd ../auth-server
railway link --service auth-server
railway up

# Content
cd ../content
railway link --service content
railway up
```

## Expected Result

After configuration:
- Backend will build using `intellistack/docker/backend.Dockerfile`
- Auth-Server will build using `intellistack/auth-server/Dockerfile`
- Content will build as a Node.js app with Docusaurus

## Verification

Once redeployed, check logs:
```bash
railway service backend logs
railway service auth-server logs
railway service content logs
```

You should see proper build processes instead of "Railpack could not determine how to build the app."
