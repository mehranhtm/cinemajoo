@echo off
echo Starting Cinemajoo Django Backend...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "manage.py" (
    echo Error: manage.py not found
    echo Please run this script from the backend directory
    pause
    exit /b 1
)

REM Check if requirements are installed
if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting Django development server...
echo The server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

pause



