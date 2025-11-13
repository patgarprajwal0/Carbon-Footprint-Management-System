# CI/CD Pipeline Setup Guide

## Quick Start

### 1. Commit and Push Changes
Use the provided scripts to commit and push your CI/CD changes:

**Windows (PowerShell):**
```powershell
.\commit_and_push.ps1
```

**Windows (Command Prompt):**
```cmd
commit_and_push.bat
```

**Manual:**
```bash
git add .
git commit -m "Add CI/CD pipeline with test cases and Azure DevOps configuration"
git push
```

### 2. Set Up Azure DevOps Pipeline

1. **Log in to Azure DevOps**
   - Go to [dev.azure.com](https://dev.azure.com)
   - Select your organization or create a new one

2. **Create a New Project** (if needed)
   - Click "New Project"
   - Enter project name: "Carbon-Footprint-Management-System"
   - Choose visibility (Private/Public)
   - Click "Create"

3. **Connect Your Repository**
   - Go to Repos > Files
   - If using GitHub, connect via "Import repository"
   - If using Azure Repos, push your code there

4. **Create Pipeline**
   - Go to Pipelines > Pipelines
   - Click "New pipeline" or "Create Pipeline"
   - Select your repository source (Azure Repos Git, GitHub, etc.)
   - Select your repository
   - Choose "Existing Azure Pipelines YAML file"
   - Select branch: `main` (or your default branch)
   - Select path: `/azure-pipelines.yml`
   - Click "Continue"

5. **Review and Run**
   - Review the pipeline YAML configuration
   - Click "Run" to execute the pipeline
   - Monitor the pipeline execution in real-time

### 3. Pipeline Triggers

The pipeline automatically triggers on:
- **Pushes to `main` branch**
- **Pushes to `develop` branch**
- **Pull requests** (if configured)

### 4. View Results

After the pipeline runs:
- **Test Results**: View in the "Tests" tab
- **Code Coverage**: View in the "Coverage" tab or download HTML report
- **Build Artifacts**: Download from the "Artifacts" section
- **Security Reports**: Download from the "Artifacts" section

## Pipeline Stages Explained

### Stage 1: Test
- Installs Python dependencies
- Runs Flake8 linting
- Executes pytest with coverage
- Publishes test results and coverage reports

### Stage 2: Build
- Installs application dependencies
- Verifies build success
- Creates application archive
- Publishes build artifacts

### Stage 3: Security
- Scans code with Bandit
- Checks dependencies with Safety
- Publishes security reports

## Running Tests Locally

Before pushing, test locally:

```bash
# Install test dependencies
pip install -r backend/requirements-test.txt

# Run tests
cd backend
pytest tests/ -v --cov=. --cov-report=html

# Run linting
flake8 .
```

## Troubleshooting

### Pipeline Fails at Test Stage
- Check that all dependencies are listed in `requirements-test.txt`
- Verify Python version matches your local environment
- Check test files for syntax errors

### Pipeline Fails at Linting
- Run `flake8 .` locally to see errors
- Fix formatting issues
- Update `.flake8` config if needed

### Tests Fail in Pipeline
- Ensure all mocks are properly configured
- Check that test data is consistent
- Verify no hard-coded paths or local dependencies

### Build Stage Fails
- Check that `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check for syntax errors in `main.py`

## Customizing the Pipeline

### Change Python Version
Edit `azure-pipelines.yml`:
```yaml
variables:
  pythonVersion: '3.11'  # Change to your desired version
```

### Add More Test Stages
Add stages in `azure-pipelines.yml`:
```yaml
- stage: YourStage
  displayName: 'Your Stage Description'
  jobs:
  - job: YourJob
    steps:
    # Your steps here
```

### Modify Linting Rules
Edit `backend/.flake8`:
```ini
max-line-length = 127  # Change line length
max-complexity = 10     # Change complexity threshold
```

## Best Practices

1. **Run tests locally** before pushing
2. **Fix linting errors** before committing
3. **Write tests** for new features
4. **Keep test coverage** above 70%
5. **Review pipeline logs** when it fails
6. **Update dependencies** regularly

## Additional Resources

- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Project Test Documentation](backend/tests/README.md)
- [Full CI/CD Documentation](CICD_README.md)

