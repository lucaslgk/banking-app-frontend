@echo off
echo ==========================================
echo    Banking App Frontend - Startup Script
echo ==========================================

echo.
echo [1/2] Checking for backend API...
python -c "import socket, sys; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); result = s.connect_ex(('localhost', 8000)); s.close(); sys.exit(0 if result == 0 else 1)" > nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Port 8000 is not accessible!
    echo.
    echo Please start the backend API first in a separate terminal.
    echo The frontend needs the backend to fetch data.
    echo.
    set /p continue="Do you want to continue anyway? (y/n) "
    if /i "%continue%" neq "y" exit /b
) else (
    echo [OK] Backend API detected on port 8000.
)

echo.
echo [2/2] Starting Frontend (Reflex)...
echo Attempting to launch application...

REM Attempt 1: Direct reflex command
call reflex run
if %errorlevel% equ 0 goto :eof

echo.
echo 'reflex' command not found or failed.
echo Attempting fallback with 'python -m reflex run'...

REM Attempt 2: Python module execution
python -m reflex run
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Could not start Reflex.
    echo Please ensure Python is installed and added to your PATH.
    echo You may need to activate your virtual environment (conda/venv) before running this script if Python is not in your global PATH.
)

pause
