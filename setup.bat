@echo off
REM ================================================
REM NutriAI - Quick Setup Script for Windows
REM ================================================

echo.
echo   ╔═══════════════════════════════════╗
echo   ║   NutriAI - Quick Setup Script    ║
echo   ║   AI Gym Nutrition Calculator     ║
echo   ╚═══════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️  Warning: Could not upgrade pip
)

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Train models
echo.
echo ================================================
echo Training Machine Learning Models...
echo ================================================
python train_models.py
if errorlevel 1 (
    echo ❌ Failed to train models
    pause
    exit /b 1
)
echo ✓ Models trained successfully

REM Check for .env file
echo.
if not exist .env (
    echo ⚠️  .env file not found!
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo.
    echo ⚠️  IMPORTANT: Edit .env and add your Google Gemini API key
    echo    1. Open .env in a text editor
    echo    2. Replace 'your_google_gemini_api_key_here' with your actual API key
    echo    3. Get API key from: https://ai.google.dev/
)

REM Setup complete
echo.
echo ================================================
echo ✓ Setup Complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env and add your Google Gemini API key
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
echo To deactivate virtual environment later, type: deactivate
echo.

pause
