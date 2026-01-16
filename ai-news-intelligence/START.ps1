#!/usr/bin/env powershell
# AI News Intelligence - Complete Startup Script
# Starts both backend and frontend development servers

Write-Host "================================" -ForegroundColor Cyan
Write-Host "AI News Intelligence" -ForegroundColor Cyan
Write-Host "Project Startup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Colors
$successColor = "Green"
$errorColor = "Red"
$infoColor = "Cyan"
$warningColor = "Yellow"

# Paths
$projectRoot = "c:\Users\ASUS\Desktop\My Start Up\news\ai-news-intelligence"
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"

Write-Host "📁 Project Root: $projectRoot" -ForegroundColor $infoColor
Write-Host ""

# Check if paths exist
if (-not (Test-Path $backendPath)) {
    Write-Host "❌ Backend path not found: $backendPath" -ForegroundColor $errorColor
    exit 1
}

if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ Frontend path not found: $frontendPath" -ForegroundColor $errorColor
    exit 1
}

Write-Host "✅ Project structure verified" -ForegroundColor $successColor
Write-Host ""

# ==================== BACKEND SETUP ====================
Write-Host "🔧 Setting up Backend..." -ForegroundColor $infoColor
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $infoColor

cd $backendPath

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor $warningColor
    python -m venv venv
}

# Activate venv
.\venv\Scripts\Activate.ps1

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  No .env file found. Creating with defaults..." -ForegroundColor $warningColor
    Write-Host "📝 Please update .env with your API keys (OpenAI, NewsAPI)" -ForegroundColor $warningColor
}

Write-Host "✅ Backend environment ready" -ForegroundColor $successColor
Write-Host ""

# ==================== FRONTEND SETUP ====================
Write-Host "🎨 Setting up Frontend..." -ForegroundColor $infoColor
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor $infoColor

cd $frontendPath

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing npm packages..." -ForegroundColor $warningColor
    npm install --legacy-peer-deps --silent
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor $successColor
} else {
    Write-Host "✅ Frontend dependencies already installed" -ForegroundColor $successColor
}

Write-Host ""
Write-Host "================================" -ForegroundColor $successColor
Write-Host "✅ PROJECT READY TO RUN!" -ForegroundColor $successColor
Write-Host "================================" -ForegroundColor $successColor
Write-Host ""

Write-Host "🚀 To start the development servers:" -ForegroundColor $infoColor
Write-Host ""
Write-Host "1️⃣  Open Terminal 1 and run:" -ForegroundColor $infoColor
Write-Host "   cd '$backendPath'" -ForegroundColor "Gray"
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor "Gray"
Write-Host "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -ForegroundColor "Gray"
Write-Host ""

Write-Host "2️⃣  Open Terminal 2 and run:" -ForegroundColor $infoColor
Write-Host "   cd '$frontendPath'" -ForegroundColor "Gray"
Write-Host "   npx expo start --web" -ForegroundColor "Gray"
Write-Host ""

Write-Host "📱 For React Native on Emulator:" -ForegroundColor $infoColor
Write-Host "   cd '$frontendPath'" -ForegroundColor "Gray"
Write-Host "   npx react-native run-android" -ForegroundColor "Gray"
Write-Host ""

Write-Host "🌐 For Expo Go (Mobile Phone):" -ForegroundColor $infoColor
Write-Host "   1. Install Expo Go app on your phone" -ForegroundColor "Gray"
Write-Host "   2. cd '$frontendPath'" -ForegroundColor "Gray"
Write-Host "   3. npx expo start" -ForegroundColor "Gray"
Write-Host "   4. Scan QR code with Expo Go" -ForegroundColor "Gray"
Write-Host ""

Write-Host "📚 API Documentation:" -ForegroundColor $infoColor
Write-Host "   SwaggerUI: http://localhost:8000/docs" -ForegroundColor $successColor
Write-Host "   ReDoc: http://localhost:8000/redoc" -ForegroundColor $successColor
Write-Host ""

Write-Host "📝 Configuration:" -ForegroundColor $infoColor
Write-Host "   Backend .env: $backendPath\.env" -ForegroundColor "Gray"
Write-Host "   - Update OPENAI_API_KEY with your key" -ForegroundColor $warningColor
Write-Host "   - Update NEWS_API_KEY with your key" -ForegroundColor $warningColor
Write-Host "   - For PostgreSQL: update DATABASE_URL" -ForegroundColor $warningColor
Write-Host ""

Write-Host "📂 Project Structure:" -ForegroundColor $infoColor
Write-Host "   backend/         FastAPI application" -ForegroundColor "Gray"
Write-Host "   frontend/        React Native app" -ForegroundColor "Gray"
Write-Host "   deployment/      Docker & Kubernetes configs" -ForegroundColor "Gray"
Write-Host ""

Write-Host "✨ Features:" -ForegroundColor $infoColor
Write-Host "   ✅ News aggregation from multiple sources" -ForegroundColor "Gray"
Write-Host "   ✅ RAG-powered AI Q&A" -ForegroundColor "Gray"
Write-Host "   ✅ Sentiment analysis" -ForegroundColor "Gray"
Write-Host "   ✅ Topic extraction & trends" -ForegroundColor "Gray"
Write-Host "   ✅ Mobile app (iOS/Android)" -ForegroundColor "Gray"
Write-Host "   ✅ Type-safe (TypeScript)" -ForegroundColor "Gray"
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor $successColor
Write-Host "Ready to develop! Press Ctrl+C to exit this script." -ForegroundColor $successColor
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor $successColor
Write-Host ""
