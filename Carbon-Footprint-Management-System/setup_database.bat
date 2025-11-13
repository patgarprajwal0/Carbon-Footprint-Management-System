@echo off
echo Setting up MySQL database for Carbon Footprint Management System...
echo.

REM Add XAMPP MySQL to PATH
set PATH=%PATH%;C:\xampp\mysql\bin

REM Check if MySQL is accessible
mysql -u root -e "SELECT 'MySQL is working' AS status;" 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Cannot connect to MySQL server!
    echo.
    echo Please ensure MySQL is running. You can start it from:
    echo 1. XAMPP Control Panel (start the MySQL service)
    echo 2. Or run: net start mysql
    echo.
    pause
    exit /b 1
)

echo.
echo MySQL is running. Setting up database...
echo.

REM Create database
echo Creating database 'icfms_new'...
mysql -u root -e "CREATE DATABASE IF NOT EXISTS icfms_new;" 2>nul
if errorlevel 1 (
    echo ERROR: Failed to create database!
    pause
    exit /b 1
)

echo Database created successfully!
echo.

REM Import SQL schema
echo Importing database schema...
mysql -u root icfms_new < "%~dp0icfms_updated.sql" 2>nul
if errorlevel 1 (
    echo ERROR: Failed to import schema!
    pause
    exit /b 1
)

echo.
echo Database setup completed successfully!
echo.
echo Database Name: icfms_new
echo User: root
echo Password: (empty)
echo.
echo You can now run the Flask application!
echo.
pause

