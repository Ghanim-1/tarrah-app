@echo off
REM طرّة Business Management System - Startup Script
REM Run this file to start the application

title طرّة - Tarrah Business Manager
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║          طرّة (Tarrah) Business Management System         ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ℹ Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/update dependencies
echo ℹ Checking dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed
echo.

REM Start the application
echo ═════════════════════════════════════════════════════════════
echo.
echo ✓ Starting طرّة application...
echo.
echo 📱 Open your browser and go to: http://localhost:5000
echo.
echo 🔑 Default login:
echo    Username: admin
echo    Password: admin123
echo.
echo 📲 Mobile Access:
echo    Find your IP: Run 'ipconfig' in another CMD
echo    Then on phone: http://YOUR-IP:5000
echo.
echo 🛑 To stop: Press Ctrl+C
echo.
echo ═════════════════════════════════════════════════════════════
echo.

REM Run the application
python app.py

REM If app crashes, keep window open
pause
