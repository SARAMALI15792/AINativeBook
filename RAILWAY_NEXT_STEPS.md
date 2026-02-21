# Railway Deployment - Next Steps

## ✅ Completed

1. ✅ Removed Render configuration files (`render.yaml`, `.github/workflows/deploy.yml`)
2. ✅ Created Railway configuration files for all services
3. ✅ Created GitHub Actions workflow for Railway deployment
4. ✅ Created comprehensive deployment documentation (`RAILWAY_DEPLOYMENT.md`)
5. ✅ Created automated setup scripts (`setup-railway.sh`, `setup-railway.bat`)
6. ✅ Generated secure secrets (SECRET_KEY, BETTER_AUTH_SECRET)
7. ✅ Committed and pushed all changes to GitHub

## 🚀 Next Steps (Manual Actions Required)

### Step 1: Login to Railway
```bash
railway login
```
This will open a browser window for authentication.

### Step 2: Run the Setup Script

**On Windows:**
```bash
.\setup-railway.bat
```

**On Linux/Mac:**
```bash
chmod +x setup-railway.sh
./setup-railway.sh
```

The script will:
- Create the Railway project "intellistack-platform"
- Create services: backend, auth-server, content, redis
- Prompt you to set environment variables manually

### Step 3: Set Environment Variables

When prompted by the script, run these commands:

**Backend Service:**
```bash
source railway-credentials.sh  # Load credentials from local file

railway variables set --service backend \
  ENVIRONMENT=production \
  DEBUG=false \
  DATABASE_URL="$BACKEND_DATABASE_URL" \
  SECRET_KEY="$BACKEND_SECRET_KEY" \
  QDRANT_HOST="$BACKEND_QDRANT_HOST" \
  QDRANT_PORT=6333 \
  QDRANT_API_KEY="$BACKEND_QDRANT_API_KEY" \
  OPENAI_API_KEY="$BACKEND_OPENAI_API_KEY"
```

**Auth Server:**
```bash
railway variables set --service auth-server \
  NODE_ENV=production \
  DATABASE_URL="$AUTH_DATABASE_URL" \
  BETTER_AUTH_SECRET="$AUTH_BETTER_AUTH_SECRET" \
  BETTER_AUTH_TRUST_HOST=true
```

**Content Site:**
```bash
railway variables set --service content \
  NODE_ENV=production
```

### Step 4: Link Service References

After initial deployment, set cross-service references:

```bash
# Link Redis to backend
railway variables set --service backend REDIS_URL='${{Redis.REDIS_URL}}'

# Link auth-server to backend
railway variables set --service backend \
  BETTER_AUTH_URL='https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}' \
  BETTER_AUTH_JWKS_URL='https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}/.well-known/jwks.json' \
  CORS_ORIGINS='https://${{content.RAILWAY_PUBLIC_DOMAIN}},https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}'

# Set auth-server URL and CORS
railway variables set --service auth-server \
  BETTER_AUTH_URL='https://${{RAILWAY_PUBLIC_DOMAIN}}' \
  CORS_ORIGINS='https://${{backend.RAILWAY_PUBLIC_DOMAIN}},https://${{content.RAILWAY_PUBLIC_DOMAIN}}'

# Set content site URLs
railway variables set --service content \
  SITE_URL='https://${{RAILWAY_PUBLIC_DOMAIN}}' \
  BETTER_AUTH_URL='https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}' \
  BACKEND_URL='https://${{backend.RAILWAY_PUBLIC_DOMAIN}}'
```

### Step 5: Deploy Services

The setup script will automatically deploy all services. Monitor deployment:

```bash
# Check deployment status
railway status

# View logs
railway logs --service backend --follow
railway logs --service auth-server --follow
railway logs --service content --follow
```

### Step 6: Verify Deployments

Once deployed, test each service:

```bash
# Get service URLs
railway status

# Test backend health
curl https://<backend-url>/health

# Test auth server health
curl https://<auth-url>/health

# Test content site
curl https://<content-url>
```

### Step 7: Set Up GitHub Actions CI/CD

Generate a Railway token for automated deployments:

```bash
railway tokens create
```

Add the token to GitHub:
1. Go to: https://github.com/SARAMALI15792/AINativeBook/settings/secrets/actions
2. Click "New repository secret"
3. Name: `RAILWAY_TOKEN`
4. Value: Paste the token from above
5. Click "Add secret"

Now, every push to `main` will automatically deploy changed services!

## 📊 Monitoring

### View Service Status
```bash
railway status
```

### View Logs
```bash
railway logs --service backend
railway logs --service auth-server
railway logs --service content
```

### View Environment Variables
```bash
railway variables --service backend
```

### Restart Services
```bash
railway restart --service backend
```

## 🔐 Security Notes

- ✅ Credentials are stored in `railway-credentials.sh` (gitignored)
- ✅ Setup scripts do NOT contain hardcoded secrets
- ✅ GitHub push protection is active
- ✅ All secrets are managed via Railway environment variables

## 📚 Documentation

Full deployment guide: `RAILWAY_DEPLOYMENT.md`

## 🎯 Expected Outcome

After completing these steps, you will have:
- ✅ Backend API running on Railway
- ✅ Auth server running on Railway
- ✅ Content site running on Railway
- ✅ Redis managed service connected
- ✅ All services communicating via service references
- ✅ Automated CI/CD via GitHub Actions
- ✅ Database migrations applied automatically on deployment

## ⏱️ Estimated Time

- Setup script execution: 5-10 minutes
- Service deployment: 10-15 minutes
- Verification: 5 minutes
- **Total: ~30 minutes**

## 🆘 Troubleshooting

If you encounter issues, refer to the "Troubleshooting" section in `RAILWAY_DEPLOYMENT.md`.

Common issues:
- Database connection errors → Check DATABASE_URL
- Redis connection errors → Verify Redis service is running
- Auth server not accessible → Check BETTER_AUTH_URL
- Build failures → Review build logs with `railway logs --service <name> --deployment`

---

**Ready to deploy? Run `railway login` and then execute the setup script!**
