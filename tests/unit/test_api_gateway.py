"""Unit tests for API Gateway service."""

import pytest
from fastapi.testclient import TestClient

from src.api_gateway.main import app


@pytest.fixture
def client():
    """Create a test client for the API Gateway."""
    return TestClient(app)


@pytest.fixture
def test_app():
    """Create a test app instance."""
    return app


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_endpoint_returns_healthy(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "api-gateway"}

    def test_health_endpoint_status_code(self, client):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint_returns_info(self, client):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "IaaS Platform API Gateway"
        assert data["version"] == "0.1.0"
        assert data["docs"] == "/api/docs"

    def test_root_endpoint_status_code(self, client):
        """Test that root endpoint returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_endpoint(self, client):
        """Test that OpenAPI endpoint is accessible."""
        response = client.get("/api/openapi.json")
        assert response.status_code == 200

    def test_docs_endpoint(self, client):
        """Test that Swagger UI docs endpoint is accessible."""
        response = client.get("/api/docs")
        assert response.status_code == 200

    def test_redoc_endpoint(self, client):
        """Test that ReDoc endpoint is accessible."""
        response = client.get("/api/redoc")
        assert response.status_code == 200
