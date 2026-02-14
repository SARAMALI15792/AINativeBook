@echo off
REM IntelliStack Backend Startup Script for Windows
REM This script will set up and run the backend server

echo ========================================
echo IntelliStack Backend Startup
echo ========================================
echo.

REM Change to backend directory
cd /d "%~dp0"

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    exit /b 1
)
echo.

echo [2/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

echo [3/5] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)
echo.

echo [4/5] Running database migrations...
alembic upgrade head
if errorlevel 1 (
    echo ERROR: Database migrations failed
    exit /b 1
)
echo.

echo [5/5] Starting FastAPI server...
echo.
echo ========================================
echo Backend running at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn src.main:app --reload --port 8000

pause
