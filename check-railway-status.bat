@echo off
echo.
echo ============================================================
echo Railway Deployment Status Check
echo ============================================================
echo.
echo Checking all services...
echo.

echo Backend Service:
railway service backend status
echo.

echo Auth-Server Service:
railway service auth-server status
echo.

echo Content Service:
railway service content status
echo.

echo Redis Service:
railway service redis status
echo.

echo.
echo ============================================================
echo.
echo If services show FAILED, check the Root Directory fields
echo in Railway dashboard and make sure there are NO spaces.
echo.
pause
