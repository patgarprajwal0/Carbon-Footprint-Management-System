# CI/CD Pipeline Documentation

## Overview
This project includes a complete CI/CD pipeline configured for Azure DevOps that demonstrates automated testing, linting, code quality checks, and build processes.

## Pipeline Stages

### 1. Test Stage
- **Linting**: Runs Flake8 to check code quality and style
- **Unit Tests**: Runs pytest with coverage reporting
- **Coverage Report**: Generates HTML and XML coverage reports
- **Test Results**: Publishes test results in JUnit XML format

### 2. Build Stage
- **Dependency Installation**: Installs all required Python packages
- **Build Verification**: Verifies the application can be built successfully
- **Artifact Creation**: Creates a zip archive of the application
- **Artifact Publishing**: Publishes build artifacts for deployment

### 3. Security Stage
- **Bandit**: Scans code for security vulnerabilities
- **Safety**: Checks dependencies for known security issues
- **Security Reports**: Publishes security scan reports

## Running Tests Locally

### Prerequisites
```bash
pip install -r backend/requirements.txt
pip install -r backend/requirements-test.txt
```

### Run Tests
```bash
cd backend
pytest tests/ -v --cov=. --cov-report=html
```

### Run Linting
```bash
cd backend
flake8 .
```

### View Coverage Report
```bash
# After running pytest with coverage
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

## Azure DevOps Setup

### 1. Create Pipeline
1. Go to your Azure DevOps project
2. Navigate to Pipelines > Pipelines
3. Click "New pipeline"
4. Select your repository (Azure Repos, GitHub, etc.)
5. Choose "Existing Azure Pipelines YAML file"
6. Select the `azure-pipelines.yml` file from the root directory

### 2. Configure Pipeline Variables (Optional)
- `pythonVersion`: Python version to use (default: 3.11)

### 3. Run Pipeline
- The pipeline will automatically trigger on pushes to `main` or `develop` branches
- You can also manually trigger it from the Pipelines page

## Test Cases

### Route Tests (`tests/test_routes.py`)
- Home routes (home, index, signup, login, logout)
- Authentication routes (login, register)
- Industry routes (add, view)
- Process routes (add, view)
- Transportation routes (add, view)
- Emission source routes (add, view)
- Carbon offset routes (add, view)
- API endpoints (industry summary)

### Database Tests (`tests/test_database.py`)
- Database connection tests
- Query execution tests

## Coverage Goals
- Target coverage: > 70%
- Critical paths: > 90%

## Best Practices
1. **Run tests before pushing**: Always run tests locally before pushing code
2. **Keep tests updated**: Update tests when adding new features
3. **Mock external dependencies**: Use mocks for database and external services in tests
4. **Follow linting rules**: Fix linting errors before committing
5. **Review coverage reports**: Ensure new code is covered by tests

## Troubleshooting

### Tests Fail in Pipeline
- Check that all dependencies are in `requirements-test.txt`
- Verify test database configuration doesn't require actual MySQL
- Ensure mocks are properly configured

### Linting Errors
- Run `flake8 .` locally to see errors
- Fix formatting issues
- Update `.flake8` config if needed

### Coverage Not Generating
- Verify pytest-cov is installed
- Check that coverage.xml is being generated
- Ensure test files are in the correct directory

## Additional Resources
- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Flake8 Documentation](https://flake8.pycqa.org/)

