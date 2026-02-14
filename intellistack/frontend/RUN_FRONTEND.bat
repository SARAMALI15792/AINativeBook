@echo off
REM IntelliStack Frontend Startup Script for Windows
REM This script will set up and run the frontend server

echo ========================================
echo IntelliStack Frontend Startup
echo ========================================
echo.

REM Change to frontend directory
cd /d "%~dp0"

echo [1/3] Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 18+
    exit /b 1
)
echo.

echo [2/3] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

echo [3/3] Starting Next.js development server...
echo.
echo ========================================
echo Frontend running at: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
