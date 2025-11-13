# Setup script for MySQL database
Write-Host "Setting up MySQL database for Carbon Footprint Management System..." -ForegroundColor Cyan
Write-Host ""

# Add XAMPP MySQL to PATH
$env:Path += ";C:\xampp\mysql\bin"

# Check if MySQL is accessible
Write-Host "Checking MySQL connection..." -ForegroundColor Yellow
$mysqlCheck = & mysql -u root -e "SELECT 'MySQL is working' AS status;" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Cannot connect to MySQL server!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please ensure MySQL is running. You can start it from:" -ForegroundColor Yellow
    Write-Host "1. XAMPP Control Panel (start the MySQL service)" -ForegroundColor Yellow
    Write-Host "2. Or run as Administrator: net start mysql" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "MySQL is running!" -ForegroundColor Green
Write-Host ""

# Create database
Write-Host "Creating database 'icfms_new'..." -ForegroundColor Yellow
$createDb = & mysql -u root -e "CREATE DATABASE IF NOT EXISTS icfms_new;" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to create database!" -ForegroundColor Red
    Write-Host $createDb -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Database created successfully!" -ForegroundColor Green
Write-Host ""

# Import SQL schema
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$sqlFile = Join-Path $scriptPath "icfms_updated.sql"

Write-Host "Importing database schema..." -ForegroundColor Yellow
$importSchema = & mysql -u root icfms_new < $sqlFile 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to import schema!" -ForegroundColor Red
    Write-Host $importSchema -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Database setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Database Configuration:" -ForegroundColor Cyan
Write-Host "  Database Name: icfms_new"
Write-Host "  User: root"
Write-Host "  Password: (empty)"
Write-Host ""
Write-Host "You can now run the Flask application!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"

