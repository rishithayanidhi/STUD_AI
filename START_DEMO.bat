@echo off
REM Quick Start Script for STUAI Demo
REM Run this batch file to start both backend and frontend simultaneously

echo.
echo ================================================
echo   STUAI - Autonomous Operations Demo Launcher
echo ================================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python.
    pause
    exit /b 1
)

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama not running. Please start Ollama first.
    echo Download from: https://ollama.com
    echo.
)

REM Start Backend
echo [1/2] Starting FastAPI Backend...
start cmd /k "cd /d %~dp0 && .venv\Scripts\activate.bat && python main.py"

timeout /t 3 /nobreak

REM Install frontend dependencies
echo [2/2] Starting React Frontend...
if not exist "frontend\node_modules" (
    echo Installing npm dependencies...
    cd frontend
    call npm install
    cd ..
)

REM Start Frontend
start cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ================================================
echo   ✅ Demo Servers Starting!
echo ================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo Docs:     http://localhost:8000/docs
echo.
echo Close these windows when done.
echo.
pause
