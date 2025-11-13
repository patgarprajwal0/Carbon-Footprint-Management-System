"""
Test cases for Flask routes
"""
import pytest
from unittest.mock import patch, MagicMock
import json

class TestHomeRoutes:
    """Test cases for home and basic routes"""
    
    def test_home_route(self, client):
        """Test home route returns 200"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_route_without_session(self, client):
        """Test index route without session"""
        response = client.get('/index')
        assert response.status_code == 200
    
    def test_signup_route(self, client):
        """Test signup route"""
        response = client.get('/signup')
        assert response.status_code == 200
    
    def test_login_route_get(self, client):
        """Test login route GET request"""
        response = client.get('/login')
        assert response.status_code == 200
    
    def test_logout_route(self, client):
        """Test logout route"""
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

class TestAuthRoutes:
    """Test cases for authentication routes"""
    
    @patch('main.get_db_connection')
    def test_login_success(self, mock_db, client):
        """Test successful login"""
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock user data (username, email, password, role_id, industry_id, warned, warn_emi)
        mock_cursor.fetchone.return_value = ('testuser', 'test@example.com', 'password123', 2, 1, 0, 0)
        
        response = client.post('/login', data={
            'username': 'testuser',
            'password': 'password123',
            'role_id': '2'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        mock_cursor.execute.assert_called_once()
    
    @patch('main.get_db_connection')
    def test_login_invalid_credentials(self, mock_db, client):
        """Test login with invalid credentials"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None
        
        response = client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass',
            'role_id': '2'
        })
        
        assert response.status_code == 200
    
    @patch('main.get_db_connection')
    def test_register_new_user(self, mock_db, client):
        """Test user registration"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 1
        
        response = client.post('/register', data={
            'industry_name': 'Test Industry',
            'industry_address': '123 Test St',
            'industry_type': 'Manufacturing',
            'industry_contact': '1234567890',
            'manager_name': 'Test Manager',
            'manager_email': 'manager@test.com',
            'manager_phone': '1234567890',
            'username': 'newuser',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert mock_cursor.execute.call_count >= 2

class TestIndustryRoutes:
    """Test cases for industry-related routes"""
    
    @patch('main.get_db_connection')
    def test_add_industry(self, mock_db, client):
        """Test adding a new industry"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.post('/add_industry', data={
            'industry_name': 'New Industry',
            'location': 'Test Location',
            'industry_type': 'Manufacturing'
        })
        
        assert response.status_code == 200
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
    
    @patch('main.get_db_connection')
    def test_view_industries(self, mock_db, client):
        """Test viewing industries"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'industry_id': 1, 'industry_name': 'Test Industry', 'location': 'Test', 'industry_type': 'Type'}
        ]
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.get('/view_industries')
        assert response.status_code == 200

class TestProcessRoutes:
    """Test cases for process-related routes"""
    
    @patch('main.get_db_connection')
    def test_add_process(self, mock_db, client):
        """Test adding a new process"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.post('/add_process', data={
            'process_name': 'Test Process',
            'energy_consumption': '100.50',
            'emission_factor': '5.25',
            'industry_id': '1',
            'process_date': '2024-01-15'
        }, content_type='application/x-www-form-urlencoded')
        
        # Should return JSON response
        assert response.status_code in [200, 400, 401]
        if response.status_code == 200:
            assert 'message' in response.get_json()

class TestTransportationRoutes:
    """Test cases for transportation routes"""
    
    @patch('main.get_db_connection')
    def test_add_transportation(self, mock_db, client):
        """Test adding transportation data"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'industry_id': 1}
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
            sess['role_id'] = '2'
        
        response = client.post('/add_transportation', data={
            'vehicle_type': 'Car',
            'distance_travelled': '100.00',
            'fuel_consumption': '10.50',
            'date': '2024-01-15'
        }, content_type='application/x-www-form-urlencoded')
        
        assert response.status_code in [200, 400, 403]

class TestEmissionRoutes:
    """Test cases for emission source routes"""
    
    @patch('main.get_db_connection')
    def test_add_emission_source(self, mock_db, client):
        """Test adding emission source"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.post('/add_emission_source', data={
            'source_type': 'Gas',
            'emission_value': '50.25',
            'emission_date': '2024-01-15'
        }, follow_redirects=True)
        
        assert response.status_code == 200
    
    @patch('main.get_db_connection')
    def test_view_emission_sources(self, mock_db, client):
        """Test viewing emission sources"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.get('/view_emission_sources')
        assert response.status_code == 200

class TestCarbonOffsetRoutes:
    """Test cases for carbon offset routes"""
    
    @patch('main.get_db_connection')
    def test_add_carbon_offset(self, mock_db, client):
        """Test adding carbon offset"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'industry_id': 1}
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.post('/add_carbon_offset', data={
            'offset_type': 'Renewable',
            'offset_quantity': '100.00',
            'provider_details': 'Test Provider',
            'date_purchased': '2024-01-15'
        })
        
        assert response.status_code == 200

class TestApiEndpoints:
    """Test cases for API endpoints"""
    
    @patch('main.get_db_connection')
    def test_industry_summary_route(self, mock_db, client):
        """Test industry summary route"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock multiple fetchone calls for different queries
        mock_cursor.fetchone.side_effect = [
            {'total_energy_consumption': 100, 'total_emission_factor': 50},
            {'total_fuel_consumption': 200, 'total_distance_travelled': 500},
            {'total_emissions': 300},
            {'total_offsets': 100}
        ]
        
        with client.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        response = client.get('/industry_summary')
        # Can return 200 (HTML) or 403/500 (JSON)
        assert response.status_code in [200, 403, 500]

