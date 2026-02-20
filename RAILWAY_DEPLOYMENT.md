# Railway Deployment Guide

## Prerequisites

1. Railway account (https://railway.app)
2. Railway CLI installed: `npm install -g @railway/cli`
3. External services configured:
   - Neon PostgreSQL database
   - Qdrant Cloud vector database

## Initial Setup

### 1. Login to Railway
```bash
railway login
```

### 2. Create New Project
```bash
railway init --name intellistack-platform
```

### 3. Create Services
```bash
# Create backend service
railway service create backend

# Create auth server service
railway service create auth-server

# Create content site service
railway service create content

# Add Redis managed service
railway add --service redis
```

### 4. Link Services to Source Directories
```bash
# Link backend
railway link --service backend --path intellistack/backend

# Link auth server
railway link --service auth-server --path intellistack/auth-server

# Link content site
railway link --service content --path intellistack/content
```

### 5. Configure Environment Variables

#### Backend Service
```bash
railway variables set \
  --service backend \
  ENVIRONMENT=production \
  DEBUG=false \
  DATABASE_URL="<your-neon-connection-string>" \
  SECRET_KEY="<generate-32-char-secret>" \
  QDRANT_HOST="<your-qdrant-host>" \
  QDRANT_PORT=6333 \
  QDRANT_API_KEY="<your-qdrant-key>" \
  OPENAI_API_KEY="<your-openai-key>" \
  COHERE_API_KEY="<your-cohere-key>"
```

After Redis is provisioned, link it:
```bash
railway variables set --service backend REDIS_URL='${{Redis.REDIS_URL}}'
```

After auth-server is deployed, link it:
```bash
railway variables set --service backend \
  BETTER_AUTH_URL='https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}' \
  BETTER_AUTH_JWKS_URL='https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}/.well-known/jwks.json'
```

#### Auth Server
```bash
railway variables set \
  --service auth-server \
  NODE_ENV=production \
  DATABASE_URL="<your-neon-connection-string>" \
  BETTER_AUTH_SECRET="<generate-32-char-secret>" \
  BETTER_AUTH_TRUST_HOST=true \
  RESEND_API_KEY="<your-resend-key>"
```

After deployment, set the auth URL:
```bash
railway variables set --service auth-server \
  BETTER_AUTH_URL='https://${{RAILWAY_PUBLIC_DOMAIN}}'
```

After other services are deployed, set CORS:
```bash
railway variables set --service auth-server \
  CORS_ORIGINS='https://${{backend.RAILWAY_PUBLIC_DOMAIN}},https://${{content.RAILWAY_PUBLIC_DOMAIN}}'
```

#### Content Site
```bash
railway variables set \
  --service content \
  NODE_ENV=production
```

After other services are deployed, set URLs:
```bash
railway variables set --service content \
  SITE_URL='https://${{RAILWAY_PUBLIC_DOMAIN}}' \
  BETTER_AUTH_URL='https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}' \
  BACKEND_URL='https://${{backend.RAILWAY_PUBLIC_DOMAIN}}'
```

### 6. Deploy Services
```bash
# Deploy all services
railway up --service backend --detach
railway up --service auth-server --detach
railway up --service content --detach
```

## CI/CD Setup

### 1. Generate Railway Token
```bash
railway tokens create
```

Copy the generated token.

### 2. Add GitHub Secret
1. Go to your GitHub repository
2. Navigate to: Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `RAILWAY_TOKEN`
5. Value: Paste the token from step 1
6. Click "Add secret"

### 3. Push to Main Branch
The GitHub Actions workflow will automatically deploy on push to main.

## Manual Deployment

Deploy specific service:
```bash
railway up --service backend
railway up --service auth-server
railway up --service content
```

Deploy all services:
```bash
railway up
```

## Monitoring

### View Logs
```bash
# View backend logs
railway logs --service backend

# View auth server logs
railway logs --service auth-server

# View content site logs
railway logs --service content

# Follow logs in real-time
railway logs --service backend --follow
```

### View Service Status
```bash
railway status
```

### View Environment Variables
```bash
railway variables --service backend
railway variables --service auth-server
railway variables --service content
```

## Troubleshooting

### Check Service Health
```bash
# Get service URLs
railway status

# Test backend health
curl https://<your-backend-url>/health

# Test auth server health
curl https://<your-auth-url>/health

# Test content site
curl https://<your-content-url>
```

### Restart Service
```bash
railway restart --service backend
railway restart --service auth-server
railway restart --service content
```

### View Build Logs
```bash
railway logs --service backend --deployment
```

### Common Issues

#### 1. Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check Neon database is accessible
- Ensure connection string includes SSL parameters

#### 2. Redis Connection Errors
- Verify Redis service is running: `railway status`
- Check `REDIS_URL` variable is set: `railway variables --service backend`

#### 3. Auth Server Not Accessible
- Check `BETTER_AUTH_URL` is set correctly
- Verify auth-server service is deployed and running
- Check CORS origins include backend and content domains

#### 4. Build Failures
- Check Dockerfile paths in `railway.toml`
- Verify all dependencies are in `requirements.txt` or `package.json`
- Review build logs: `railway logs --service <service-name> --deployment`

## Environment Variables Reference

### Backend Service
| Variable | Description | Example |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment name | `production` |
| `DEBUG` | Debug mode | `false` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | Application secret key | `<32+ character string>` |
| `REDIS_URL` | Redis connection string | `${{Redis.REDIS_URL}}` |
| `QDRANT_HOST` | Qdrant host | `xyz.qdrant.io` |
| `QDRANT_PORT` | Qdrant port | `6333` |
| `QDRANT_API_KEY` | Qdrant API key | `<your-key>` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `COHERE_API_KEY` | Cohere API key | `<your-key>` |
| `BETTER_AUTH_URL` | Auth server URL | `https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}` |
| `BETTER_AUTH_JWKS_URL` | JWKS endpoint | `https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}/.well-known/jwks.json` |
| `CORS_ORIGINS` | Allowed CORS origins | `https://domain1.com,https://domain2.com` |

### Auth Server
| Variable | Description | Example |
|----------|-------------|---------|
| `NODE_ENV` | Node environment | `production` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `BETTER_AUTH_SECRET` | Auth secret key | `<32+ character string>` |
| `BETTER_AUTH_URL` | Auth server public URL | `https://${{RAILWAY_PUBLIC_DOMAIN}}` |
| `BETTER_AUTH_TRUST_HOST` | Trust host header | `true` |
| `CORS_ORIGINS` | Allowed CORS origins | `https://domain1.com,https://domain2.com` |
| `RESEND_API_KEY` | Resend API key (optional) | `re_...` |

### Content Site
| Variable | Description | Example |
|----------|-------------|---------|
| `NODE_ENV` | Node environment | `production` |
| `SITE_URL` | Content site URL | `https://${{RAILWAY_PUBLIC_DOMAIN}}` |
| `BETTER_AUTH_URL` | Auth server URL | `https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}` |
| `BACKEND_URL` | Backend API URL | `https://${{backend.RAILWAY_PUBLIC_DOMAIN}}` |

## Railway Service References

Railway allows services to reference each other using the `${{service-name.VARIABLE}}` syntax:

- `${{RAILWAY_PUBLIC_DOMAIN}}` - Current service's public domain
- `${{backend.RAILWAY_PUBLIC_DOMAIN}}` - Backend service's public domain
- `${{auth-server.RAILWAY_PUBLIC_DOMAIN}}` - Auth server's public domain
- `${{content.RAILWAY_PUBLIC_DOMAIN}}` - Content site's public domain
- `${{Redis.REDIS_URL}}` - Redis connection string

These references are automatically resolved by Railway at runtime.

## Cost Estimation

Railway pricing (as of 2026):
- **Hobby Plan**: $5/month + usage
  - $5 includes $5 of usage credits
  - Additional usage: ~$0.000463/GB-hour for memory, ~$0.000231/vCPU-hour
- **Redis**: Included in usage costs
- **Bandwidth**: First 100GB free, then $0.10/GB

Estimated monthly cost for IntelliStack:
- 3 services (backend, auth, content) + Redis
- Low to moderate traffic
- **Estimated**: $10-20/month

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [Railway Environment Variables](https://docs.railway.app/develop/variables)
- [Railway Service References](https://docs.railway.app/develop/variables#service-variables)
