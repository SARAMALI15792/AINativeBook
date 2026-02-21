@echo off
REM Railway Service Configuration Script
REM This script guides you through configuring Railway services

echo.
echo 🚂 Railway Service Configuration
echo.
echo Unfortunately, the Railway CLI doesn't support setting root directories for monorepo services.
echo You need to configure this through the Railway dashboard.
echo.
echo 📋 Quick Configuration Steps:
echo.
echo 1. Open Railway Dashboard:
echo    https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c
echo.
echo 2. For BACKEND service:
echo    - Click on 'backend' service
echo    - Click 'Settings' tab
echo    - Under 'Source' section, find 'Root Directory'
echo    - Enter: intellistack/backend
echo    - Click 'Save'
echo    - Click 'Deploy' button
echo.
echo 3. For AUTH-SERVER service:
echo    - Click on 'auth-server' service
echo    - Click 'Settings' tab
echo    - Under 'Source' section, find 'Root Directory'
echo    - Enter: intellistack/auth-server
echo    - Click 'Save'
echo    - Click 'Deploy' button
echo.
echo 4. For CONTENT service:
echo    - Click on 'content' service
echo    - Click 'Settings' tab
echo    - Under 'Source' section, find 'Root Directory'
echo    - Enter: intellistack/content
echo    - Click 'Save'
echo    - Click 'Deploy' button
echo.
echo ⏱️  This will take about 2 minutes to configure all services.
echo.
echo ✅ After configuration, your services will deploy successfully!
echo.
echo Press any key to open the Railway dashboard...
pause >nul

start https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c
