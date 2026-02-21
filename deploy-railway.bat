@echo off
REM IntelliStack Railway Deployment Script (Windows)
REM Run this AFTER rotating credentials and configuring Railway environment variables

echo.
echo 🚀 IntelliStack Railway Deployment
echo ==================================
echo.

REM Check Railway authentication
echo ✓ Checking Railway authentication...
railway whoami >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged in to Railway. Run: railway login
    exit /b 1
)

echo.
echo ⚠️  CRITICAL: Have you completed credential rotation?
echo    1. Rotated Neon database password?
echo    2. Rotated Google OAuth credentials?
echo    3. Generated new secrets?
echo    4. Updated Railway environment variables?
echo.
set /p confirm="Continue with deployment? (yes/no): "

if not "%confirm%"=="yes" (
    echo ❌ Deployment cancelled
    exit /b 1
)

echo.
echo 📦 Deploying Backend Service...
echo ================================
cd intellistack\backend
railway link --service backend --environment production
railway up --detach
echo ✓ Backend deployment initiated
echo.

echo 📦 Deploying Auth Server...
echo ================================
cd ..\auth-server
railway link --service auth-server --environment production
railway up --detach
echo ✓ Auth Server deployment initiated
echo.

echo 📦 Deploying Content Service...
echo ================================
cd ..\content
railway link --service content --environment production
railway up --detach
echo ✓ Content deployment initiated
echo.

echo ⏳ Waiting 30 seconds for builds to start...
timeout /t 30 /nobreak >nul

echo.
echo 📊 Checking Deployment Status...
echo ================================
cd ..\..

echo.
echo Backend logs:
railway logs --service backend --tail 20

echo.
echo Auth Server logs:
railway logs --service auth-server --tail 20

echo.
echo Content logs:
railway logs --service content --tail 20

echo.
echo ✅ Deployment commands completed!
echo.
echo Next steps:
echo 1. Monitor logs: railway logs --service ^<service-name^>
echo 2. Check health endpoints (see DEPLOYMENT_CHECKLIST.md)
echo 3. Verify all services are running
