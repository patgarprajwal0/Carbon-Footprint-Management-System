@echo off
REM Batch script to commit and push CI/CD changes
echo === Carbon Footprint Management System - CI/CD Commit Script ===
echo.

REM Check if git is initialized
if not exist ".git" (
    echo ERROR: Not a git repository. Please run 'git init' first.
    exit /b 1
)

REM Check if we're in the right directory
if not exist "azure-pipelines.yml" (
    echo ERROR: Please run this script from the Carbon-Footprint-Management-System directory
    exit /b 1
)

echo Checking git status...
git status --short

echo.
echo Files will be committed:
git status --short

echo.
set /p confirmation="Do you want to commit these changes? (y/n): "
if /i not "%confirmation%"=="y" (
    echo Commit cancelled.
    exit /b 0
)

echo.
echo Staging files...
git add .

echo.
set /p commitMessage="Enter commit message (or press Enter for default): "
if "%commitMessage%"=="" (
    set commitMessage=Add CI/CD pipeline with test cases and Azure DevOps configuration
)

echo.
echo Committing changes...
git commit -m "%commitMessage%"

if errorlevel 1 (
    echo ERROR: Commit failed!
    exit /b 1
)

echo.
echo Commit successful!

echo.
set /p pushConfirmation="Do you want to push to remote repository? (y/n): "
if /i not "%pushConfirmation%"=="y" (
    echo Push cancelled. Run 'git push' manually when ready.
    exit /b 0
)

echo.
echo Pushing to remote repository...
git push

if errorlevel 1 (
    echo.
    echo ERROR: Push failed. Check your remote repository settings.
    echo You can push manually later with: git push
) else (
    echo.
    echo === Success! Changes pushed to remote repository ===
    echo.
    echo Next steps:
    echo 1. Go to Azure DevOps portal
    echo 2. Create a new pipeline using azure-pipelines.yml
    echo 3. Run the pipeline to see CI/CD in action!
)

pause

