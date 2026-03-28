#!/usr/bin/env pwsh
# Quick Start Script for STUAI Demo
# Run: .\START_DEMO.ps1

Write-Host @"
================================================
  STUAI - Autonomous Operations Demo Launcher
================================================
"@ -ForegroundColor Cyan

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Install from: https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python." -ForegroundColor Red
    exit 1
}

# Check if Ollama is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
    Write-Host "✓ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "⚠ Warning: Ollama not detected. Start it from: https://ollama.com" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[1/2] Starting FastAPI Backend..." -ForegroundColor Cyan
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d `"$PSScriptRoot`" && .venv\Scripts\activate.bat && python main.py"

Start-Sleep -Seconds 3

Write-Host "[2/2] Starting React Frontend..." -ForegroundColor Cyan

# Install dependencies if needed
if (-not (Test-Path "frontend/node_modules")) {
    Write-Host "Installing npm dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d `"$PSScriptRoot\frontend`" && npm run dev"

Write-Host @"

================================================
  ✅ Demo Servers Starting!
================================================

Backend:  http://localhost:8000
Frontend: http://localhost:3000
Docs:     http://localhost:8000/docs

Close the terminal windows when done.
Press Enter to continue...
"@ -ForegroundColor Green

Read-Host
