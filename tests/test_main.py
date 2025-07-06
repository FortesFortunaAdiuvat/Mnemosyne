import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello_world():
    """Test the hello world endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from Mnemosyne API!"}

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "mnemosyne-api"

def test_api_info():
    """Test the API info endpoint"""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mnemosyne API"
    assert data["version"] == "1.0.0"
    assert "endpoints" in data
