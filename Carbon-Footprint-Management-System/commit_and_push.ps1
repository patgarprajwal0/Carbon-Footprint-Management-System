# PowerShell script to commit and push CI/CD changes
Write-Host "=== Carbon Footprint Management System - CI/CD Commit Script ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "ERROR: Not a git repository. Please run 'git init' first." -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "azure-pipelines.yml")) {
    Write-Host "ERROR: Please run this script from the Carbon-Footprint-Management-System directory" -ForegroundColor Red
    exit 1
}

Write-Host "Checking git status..." -ForegroundColor Yellow
$status = git status --porcelain

if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes to commit." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Cyan
git status --short

Write-Host ""
$confirmation = Read-Host "Do you want to commit these changes? (y/n)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "Commit cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Staging files..." -ForegroundColor Yellow
git add .

Write-Host ""
$commitMessage = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "Add CI/CD pipeline with test cases and Azure DevOps configuration"
}

Write-Host ""
Write-Host "Committing changes..." -ForegroundColor Yellow
git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Commit failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Commit successful!" -ForegroundColor Green

Write-Host ""
$pushConfirmation = Read-Host "Do you want to push to remote repository? (y/n)"
if ($pushConfirmation -ne 'y' -and $pushConfirmation -ne 'Y') {
    Write-Host "Push cancelled. Run 'git push' manually when ready." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Pushing to remote repository..." -ForegroundColor Yellow
git push

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=== Success! Changes pushed to remote repository ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to Azure DevOps portal" -ForegroundColor White
    Write-Host "2. Create a new pipeline using azure-pipelines.yml" -ForegroundColor White
    Write-Host "3. Run the pipeline to see CI/CD in action!" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "ERROR: Push failed. Check your remote repository settings." -ForegroundColor Red
    Write-Host "You can push manually later with: git push" -ForegroundColor Yellow
}

