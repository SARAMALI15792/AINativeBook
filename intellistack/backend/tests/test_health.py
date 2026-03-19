import pytest
from fastapi.testclient import TestClient
from src.main import create_app


def test_app_creation():
    """Test that the FastAPI app can be created successfully."""
    app = create_app()
    assert app is not None
    assert app.title == "IntelliStack API"


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data