@echo off
REM Railway Setup Script for IntelliStack Platform (Windows)
REM Run this script after logging in with: railway login

echo 🚂 Setting up IntelliStack Platform on Railway...
echo.

REM Check if logged in
railway whoami >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged into Railway. Please run: railway login
    exit /b 1
)

echo ✅ Logged into Railway
echo.

REM Create project
echo 📦 Creating Railway project...
railway init --name intellistack-platform

echo.
echo 🔧 Creating services...

REM Create services
railway service create backend
railway service create auth-server
railway service create content

REM Add Redis
railway add redis

echo.
echo ⚙️  Setting environment variables for BACKEND service...
echo.
echo Please set the following variables manually via Railway dashboard or CLI:
echo   - DATABASE_URL (Neon PostgreSQL connection string)
echo   - SECRET_KEY (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
echo   - QDRANT_HOST (Qdrant Cloud host URL)
echo   - QDRANT_API_KEY (Qdrant API key)
echo   - OPENAI_API_KEY (OpenAI API key)
echo.
echo Example command:
echo railway variables set --service backend ENVIRONMENT=production DEBUG=false DATABASE_URL="your-db-url" SECRET_KEY="your-secret" QDRANT_HOST="your-qdrant-host" QDRANT_PORT=6333 QDRANT_API_KEY="your-qdrant-key" OPENAI_API_KEY="your-openai-key"
echo.
pause

echo.
echo ⚙️  Setting environment variables for AUTH-SERVER service...
echo.
echo Please set the following variables manually via Railway dashboard or CLI:
echo   - DATABASE_URL (same as backend)
echo   - BETTER_AUTH_SECRET (generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
echo.
echo Example command:
echo railway variables set --service auth-server NODE_ENV=production DATABASE_URL="your-db-url" BETTER_AUTH_SECRET="your-secret" BETTER_AUTH_TRUST_HOST=true
echo.
pause

echo.
echo ⚙️  Setting environment variables for CONTENT service...

railway variables set --service content NODE_ENV=production

echo.
echo ⏳ Waiting for services to be created...
timeout /t 5 /nobreak >nul

echo.
echo 🔗 Setting up service references...

REM Link Redis to backend
railway variables set --service backend REDIS_URL="${{Redis.REDIS_URL}}"

REM Set cross-service references
railway variables set --service backend BETTER_AUTH_URL="https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}" BETTER_AUTH_JWKS_URL="https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}/.well-known/jwks.json" CORS_ORIGINS="https://${{content.RAILWAY_PUBLIC_DOMAIN}},https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}"

railway variables set --service auth-server BETTER_AUTH_URL="https://${{RAILWAY_PUBLIC_DOMAIN}}" CORS_ORIGINS="https://${{backend.RAILWAY_PUBLIC_DOMAIN}},https://${{content.RAILWAY_PUBLIC_DOMAIN}}"

railway variables set --service content SITE_URL="https://${{RAILWAY_PUBLIC_DOMAIN}}" BETTER_AUTH_URL="https://${{auth-server.RAILWAY_PUBLIC_DOMAIN}}" BACKEND_URL="https://${{backend.RAILWAY_PUBLIC_DOMAIN}}"

echo.
echo 🚀 Deploying services...

REM Deploy services
railway up --service backend --detach
railway up --service auth-server --detach
railway up --service content --detach

echo.
echo ✅ Railway setup complete!
echo.
echo 📊 View service status:
echo    railway status
echo.
echo 📝 View logs:
echo    railway logs --service backend
echo    railway logs --service auth-server
echo    railway logs --service content
echo.
echo 🔑 Generate Railway token for GitHub Actions:
echo    railway tokens create
echo.
echo    Then add it to GitHub: Settings → Secrets → Actions → RAILWAY_TOKEN
echo.
