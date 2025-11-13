# Test Suite Documentation

## Overview
This test suite uses pytest to test the Carbon Footprint Management System Flask application. All tests use mocks to avoid requiring a live database connection, making them perfect for CI/CD environments.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest fixtures and configuration
├── test_routes.py       # Route endpoint tests
└── test_database.py     # Database operation tests
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_routes.py
```

### Run Specific Test Class
```bash
pytest tests/test_routes.py::TestHomeRoutes
```

### Run Specific Test
```bash
pytest tests/test_routes.py::TestHomeRoutes::test_home_route
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Run with Verbose Output
```bash
pytest -v
```

## Test Categories

### Unit Tests
- Test individual functions and methods
- Use mocks for external dependencies
- Fast execution
- No database connection required

### Integration Tests (Future)
- Test multiple components together
- May require test database
- Slower execution
- Marked with `@pytest.mark.integration`

## Fixtures

### app
Provides a configured Flask test application

### client
Provides a test client for making requests

### mock_db_connection
Provides a mocked database connection and cursor

### mock_session
Provides a mock Flask session with test data

## Mocking Strategy

### Database Mocking
All database operations are mocked to:
- Avoid requiring MySQL in CI/CD
- Speed up test execution
- Make tests deterministic
- Isolate unit tests from database

### Session Mocking
Flask sessions are mocked to test authenticated routes without requiring actual login flow.

## Writing New Tests

1. **Import necessary modules**:
```python
import pytest
from unittest.mock import patch, MagicMock
```

2. **Use fixtures**:
```python
def test_my_route(client, mock_db_connection):
    # Test code here
```

3. **Mock database calls**:
```python
@patch('main.get_db_connection')
def test_my_function(mock_db):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    # Configure mock responses
```

4. **Assert expected behavior**:
```python
assert response.status_code == 200
assert 'expected_text' in response.get_data(as_text=True)
```

## Coverage

The test suite aims to cover:
- All route endpoints
- Authentication flows
- CRUD operations
- Error handling
- Session management

## Best Practices

1. **One assertion per test** (when possible)
2. **Use descriptive test names**: `test_login_with_invalid_credentials`
3. **Test edge cases**: empty inputs, invalid data, missing sessions
4. **Keep tests independent**: Each test should work in isolation
5. **Mock external dependencies**: Database, APIs, file system
6. **Follow AAA pattern**: Arrange, Act, Assert

## Continuous Integration

Tests run automatically in Azure DevOps pipeline on:
- Every push to main/develop branches
- Pull requests
- Manual pipeline runs

The pipeline generates:
- Test results (JUnit XML)
- Coverage reports (HTML/XML)
- Linting reports

