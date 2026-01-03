"""
Unit tests for AIbot API endpoints
Tests the Odoo integration API with mocked dependencies
"""
import pytest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api import api_bp, require_api_key
from app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a test Flask application"""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    os.environ['ODOO_API_KEY'] = 'test-api-key'
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Return headers with valid API key"""
    return {'X-API-Key': 'test-api-key'}


class TestAPIAuthentication:
    """Test API key authentication"""
    
    def test_health_endpoint_without_auth(self, client):
        """Health endpoint should work without authentication"""
        response = client.get('/api/v1/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'AIbot'
    
    def test_generate_endpoint_without_auth(self, client):
        """Generate endpoint should require authentication"""
        response = client.post('/api/v1/generate',
                              json={'prompt': 'test'},
                              content_type='application/json')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        assert 'API key' in data['error']
    
    def test_generate_endpoint_with_invalid_auth(self, client):
        """Generate endpoint should reject invalid API key"""
        response = client.post('/api/v1/generate',
                              json={'prompt': 'test'},
                              headers={'X-API-Key': 'invalid-key'},
                              content_type='application/json')
        assert response.status_code == 401
    
    def test_generate_endpoint_with_valid_auth(self, client, auth_headers):
        """Generate endpoint should accept valid API key"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Test response"
            
            response = client.post('/api/v1/generate',
                                  json={'prompt': 'test'},
                                  headers=auth_headers,
                                  content_type='application/json')
            assert response.status_code == 200


class TestGenerateEndpoint:
    """Test /api/v1/generate endpoint"""
    
    def test_generate_missing_prompt(self, client, auth_headers):
        """Should return error when prompt is missing"""
        response = client.post('/api/v1/generate',
                              json={},
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'prompt' in data['error'].lower()
    
    def test_generate_success(self, client, auth_headers):
        """Should generate response successfully"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "AI generated response"
            
            response = client.post('/api/v1/generate',
                                  json={
                                      'prompt': 'Test question',
                                      'document_type': 'General',
                                      'jurisdiction': 'Federal'
                                  },
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['response'] == "AI generated response"
            assert 'duration_ms' in data
    
    def test_generate_with_error(self, client, auth_headers):
        """Should handle generation errors gracefully"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.side_effect = Exception("API Error")
            
            response = client.post('/api/v1/generate',
                                  json={'prompt': 'Test question'},
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False
            assert 'error' in data


class TestProductDescriptionEndpoint:
    """Test /api/v1/generate/product-description endpoint"""
    
    def test_product_description_missing_name(self, client, auth_headers):
        """Should return error when product_name is missing"""
        response = client.post('/api/v1/generate/product-description',
                              json={'category': 'Electronics'},
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_product_description_success(self, client, auth_headers):
        """Should generate product description successfully"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Premium wireless headphones with noise cancellation"
            
            response = client.post('/api/v1/generate/product-description',
                                  json={
                                      'product_name': 'Wireless Headphones',
                                      'category': 'Electronics',
                                      'features': ['Bluetooth', 'Noise Cancellation']
                                  },
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'description' in data
            assert len(data['description']) > 0
    
    def test_product_description_with_optional_fields(self, client, auth_headers):
        """Should handle optional fields correctly"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Product description"
            
            response = client.post('/api/v1/generate/product-description',
                                  json={
                                      'product_name': 'Test Product',
                                      'category': 'Test Category',
                                      'features': ['Feature 1', 'Feature 2'],
                                      'price': 99.99,
                                      'target_audience': 'Professionals'
                                  },
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True


class TestEmailEndpoint:
    """Test /api/v1/generate/email endpoint"""
    
    def test_email_missing_purpose(self, client, auth_headers):
        """Should return error when purpose is missing"""
        response = client.post('/api/v1/generate/email',
                              json={'recipient_name': 'John'},
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_email_success(self, client, auth_headers):
        """Should generate email successfully"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Dear John,\n\nThank you for your interest..."
            
            response = client.post('/api/v1/generate/email',
                                  json={
                                      'purpose': 'Follow-up',
                                      'recipient_name': 'John Doe',
                                      'tone': 'professional',
                                      'context': 'Previous meeting discussion'
                                  },
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'email_content' in data
    
    def test_email_different_tones(self, client, auth_headers):
        """Should handle different email tones"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Email content"
            
            for tone in ['professional', 'friendly', 'formal']:
                response = client.post('/api/v1/generate/email',
                                      json={
                                          'purpose': 'Test',
                                          'tone': tone
                                      },
                                      headers=auth_headers,
                                      content_type='application/json')
                assert response.status_code == 200


class TestDocumentEndpoint:
    """Test /api/v1/generate/document endpoint"""
    
    def test_document_missing_type(self, client, auth_headers):
        """Should return error when document_type is missing"""
        response = client.post('/api/v1/generate/document',
                              json={'jurisdiction': 'Federal'},
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_document_success(self, client, auth_headers):
        """Should generate document successfully"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "CONTRACT\n\nThis agreement..."
            
            response = client.post('/api/v1/generate/document',
                                  json={
                                      'document_type': 'Contract',
                                      'jurisdiction': 'Federal',
                                      'parties': ['Party A', 'Party B'],
                                      'terms': 'Standard terms and conditions'
                                  },
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'document_content' in data
    
    def test_document_different_types(self, client, auth_headers):
        """Should handle different document types"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Document content"
            
            doc_types = ['Contract', 'Agreement', 'Policy', 'Terms']
            for doc_type in doc_types:
                response = client.post('/api/v1/generate/document',
                                      json={
                                          'document_type': doc_type,
                                          'jurisdiction': 'Federal'
                                      },
                                      headers=auth_headers,
                                      content_type='application/json')
                assert response.status_code == 200


class TestErrorHandling:
    """Test error handling across all endpoints"""
    
    def test_invalid_json(self, client, auth_headers):
        """Should handle invalid JSON gracefully"""
        response = client.post('/api/v1/generate',
                              data='invalid json',
                              headers=auth_headers,
                              content_type='application/json')
        assert response.status_code in [400, 500]
    
    def test_missing_content_type(self, client, auth_headers):
        """Should handle missing content type"""
        response = client.post('/api/v1/generate',
                              data=json.dumps({'prompt': 'test'}),
                              headers=auth_headers)
        # Should still work or return appropriate error
        assert response.status_code in [200, 400, 415]
    
    def test_model_client_unavailable(self, client, auth_headers):
        """Should handle model client errors"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.side_effect = ConnectionError("Service unavailable")
            
            response = client.post('/api/v1/generate',
                                  json={'prompt': 'test'},
                                  headers=auth_headers,
                                  content_type='application/json')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert data['success'] is False


class TestResponseFormat:
    """Test response format consistency"""
    
    def test_success_response_format(self, client, auth_headers):
        """All successful responses should have consistent format"""
        with patch('api.model_client') as mock_client:
            mock_client.generate_response.return_value = "Response"
            
            response = client.post('/api/v1/generate',
                                  json={'prompt': 'test'},
                                  headers=auth_headers,
                                  content_type='application/json')
            
            data = json.loads(response.data)
            assert 'success' in data
            assert 'duration_ms' in data
            assert isinstance(data['success'], bool)
            assert isinstance(data['duration_ms'], (int, float))
    
    def test_error_response_format(self, client, auth_headers):
        """All error responses should have consistent format"""
        response = client.post('/api/v1/generate',
                              json={},
                              headers=auth_headers,
                              content_type='application/json')
        
        data = json.loads(response.data)
        assert 'error' in data or 'success' in data
        if 'success' in data:
            assert data['success'] is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
