@echo off
echo Starting Carbon Footprint Management System...
echo.

cd /d "%~dp0backend"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    pause
    exit /b 1
)

REM Check if MySQL is running
mysql --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: MySQL might not be in PATH. Make sure MySQL is running!
    echo.
)

echo Starting Flask application...
echo The application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python main.py

