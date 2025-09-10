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

REM Determine virtual environment directory
set "VENV_DIR=.venv"
if not exist "%VENV_DIR%" set "VENV_DIR=venv"
if not exist "%VENV_DIR%" set "VENV_DIR=env"

REM Create venv if it does not exist
if not exist "%VENV_DIR%" (
    echo Creating virtual environment in .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
    set "VENV_DIR=.venv"
)

REM Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install requirements if file exists
if exist "requirements.txt" (
    echo Installing/updating dependencies from requirements.txt...
    pip install -r requirements.txt
)

echo.
echo Starting Django development server...
echo The server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Apply migrations automatically
python manage.py migrate

python manage.py runserver

pause





