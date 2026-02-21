@echo off
echo.
echo ============================================================
echo Railway Root Directory Fix
echo ============================================================
echo.
echo What we're fixing:
echo   The Root Directory fields have trailing spaces
echo   This prevents Railway from finding your code
echo.
echo Time required: 2-3 minutes
echo.
echo Press any key to open Railway dashboard...
pause >nul

start https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c

echo.
echo ============================================================
echo Fixing BACKEND Service
echo ============================================================
echo.
echo 1. Click on 'backend' service card
echo 2. Click 'Settings' tab
echo 3. Find 'Root Directory' field
echo 4. Select ALL text (Ctrl+A)
echo 5. Delete it
echo 6. Type: intellistack/backend
echo 7. Press Tab
echo 8. Click 'Redeploy'
echo.
pause

echo.
echo ============================================================
echo Fixing AUTH-SERVER Service
echo ============================================================
echo.
echo 1. Click on 'auth-server' service card
echo 2. Click 'Settings' tab
echo 3. Find 'Root Directory' field
echo 4. Select ALL text (Ctrl+A)
echo 5. Delete it
echo 6. Type: intellistack/auth-server
echo 7. Press Tab
echo 8. Click 'Redeploy'
echo.
pause

echo.
echo ============================================================
echo Fixing CONTENT Service
echo ============================================================
echo.
echo 1. Click on 'content' service card
echo 2. Click 'Settings' tab
echo 3. Find 'Root Directory' field
echo 4. Select ALL text (Ctrl+A)
echo 5. Delete it
echo 6. Type: intellistack/content
echo 7. Press Tab
echo 8. Click 'Redeploy'
echo.
pause

echo.
echo ============================================================
echo All Done!
echo ============================================================
echo.
echo Your services are now redeploying with correct paths.
echo.
echo Monitor progress in Railway dashboard:
echo https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c
echo.
pause
