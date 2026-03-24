import pytest
from app import create_app

def test_create_app_returns_application():
    app = create_app()
    assert app is not None
    assert hasattr(app, 'add_url_rule')

def test_health_check(client):
    """Test the / health check endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'Flask app is running!' in data['message']
