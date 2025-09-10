# Cinemajoo Django Backend Startup Script
# Run this script to start the Django development server

Write-Host "Starting Cinemajoo Django Backend..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "❌ Error: manage.py not found" -ForegroundColor Red
    Write-Host "Please run this script from the backend directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Ensure virtual environment exists
$venvDirCandidates = @('.venv', 'venv', 'env')
$venvDir = $null
foreach ($cand in $venvDirCandidates) {
    if (Test-Path $cand) { $venvDir = $cand; break }
}
if (-not $venvDir) {
    Write-Host "Creating virtual environment in .venv..." -ForegroundColor Yellow
    python -m venv .venv
    if (-not (Test-Path ".venv")) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    $venvDir = '.venv'
}

# Activate virtual environment
$activateScript = Join-Path $venvDir 'Scripts\Activate.ps1'
. $activateScript
if (-not $env:VIRTUAL_ENV) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install requirements if present
if (Test-Path "requirements.txt") {
    Write-Host "Installing/updating dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host "The server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Apply migrations then start the Django server
python manage.py migrate
python manage.py runserver

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"





