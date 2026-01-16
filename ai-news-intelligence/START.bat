@echo off
REM AI News Intelligence - Complete Startup Script (Batch Version)
REM Starts both backend and frontend development servers

setlocal enabledelayedexpansion

echo ================================
echo AI News Intelligence
echo Project Startup Script
echo ================================
echo.

REM Paths
set "projectRoot=c:\Users\ASUS\Desktop\My Start Up\news\ai-news-intelligence"
set "backendPath=%projectRoot%\backend"
set "frontendPath=%projectRoot%\frontend"

echo [INFO] Project Root: %projectRoot%
echo.

REM Check if paths exist
if not exist "%backendPath%" (
    echo [ERROR] Backend path not found: %backendPath%
    exit /b 1
)

if not exist "%frontendPath%" (
    echo [ERROR] Frontend path not found: %frontendPath%
    exit /b 1
)

echo [SUCCESS] Project structure verified
echo.

REM ==================== BACKEND SETUP ====================
echo [INFO] Setting up Backend...
echo ===============================================

cd /d "%backendPath%"

REM Check if venv exists
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] No .env file found. Creating with defaults...
    echo [INFO] Please update .env with your API keys
)

echo [SUCCESS] Backend environment ready
echo.

REM ==================== FRONTEND SETUP ====================
echo [INFO] Setting up Frontend...
echo ===============================================

cd /d "%frontendPath%"

REM Check if node_modules exists
if not exist "node_modules" (
    echo [INFO] Installing npm packages...
    call npm install --legacy-peer-deps --silent
    echo [SUCCESS] Frontend dependencies installed
) else (
    echo [SUCCESS] Frontend dependencies already installed
)

echo.
echo ================================
echo [SUCCESS] PROJECT READY TO RUN!
echo ================================
echo.

echo [INFO] To start the development servers:
echo.

echo 1 - Open Terminal 1 and run:
echo   cd "%backendPath%"
echo   venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.

echo 2 - Open Terminal 2 and run:
echo   cd "%frontendPath%"
echo   npx expo start --web
echo.

echo [INFO] For React Native on Emulator:
echo   cd "%frontendPath%"
echo   npx react-native run-android
echo.

echo [INFO] API Documentation:
echo   SwaggerUI: http://localhost:8000/docs
echo   ReDoc: http://localhost:8000/redoc
echo.

echo [INFO] Configuration:
echo   Backend .env: %backendPath%\.env
echo   - Update OPENAI_API_KEY with your key
echo   - Update NEWS_API_KEY with your key
echo.

echo ===============================================
echo Ready to develop!
echo ===============================================
echo.

pause
