"""
Test cases for database operations
"""
import pytest
from unittest.mock import patch, MagicMock
import mysql.connector

class TestDatabaseConnection:
    """Test cases for database connection"""
    
    @patch('mysql.connector.connect')
    def test_get_db_connection_success(self, mock_connect):
        """Test successful database connection"""
        from main import get_db_connection
        
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        connection = get_db_connection()
        
        assert connection is not None
        mock_connect.assert_called_once()
    
    @patch('mysql.connector.connect')
    def test_get_db_connection_failure(self, mock_connect):
        """Test database connection failure"""
        from main import get_db_connection
        
        mock_connect.side_effect = mysql.connector.Error("Connection failed")
        
        with pytest.raises(mysql.connector.Error):
            get_db_connection()

class TestDatabaseQueries:
    """Test cases for database queries"""
    
    @patch('main.get_db_connection')
    def test_user_role_query(self, mock_db):
        """Test query for user role"""
        from main import app
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'role_id': 2}
        
        with app.test_request_context():
            with app.test_client() as client:
                with client.session_transaction() as sess:
                    sess['username'] = 'testuser'
                
                # This will trigger load_user_data()
                client.get('/index')
                
                mock_cursor.execute.assert_called()

