"""
Pytest configuration file for testing Flask application
"""
import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """Create a test Flask application"""
    from main import app
    app.config['TESTING'] = True
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE'] = 'test_db'
    app.config['MYSQL_USER'] = 'test_user'
    app.config['MYSQL_PASSWORD'] = 'test_password'
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()

@pytest.fixture
def mock_db_connection():
    """Mock database connection"""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.__enter__ = Mock(return_value=mock_cursor)
    mock_cursor.__exit__ = Mock(return_value=False)
    return mock_conn, mock_cursor

@pytest.fixture
def mock_session():
    """Mock Flask session"""
    return {
        'username': 'testuser',
        'role_id': '2'
    }

