"""Unit tests for Control Plane service."""

import pytest
from fastapi.testclient import TestClient

from src.control_plane.main import app


@pytest.fixture
def client():
    """Create a test client for the Control Plane."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_endpoint_returns_healthy(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy", "service": "control-plane"}

    def test_health_endpoint_status_code(self, client):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint_returns_info(self, client):
        """Test that root endpoint returns service information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "IaaS Platform Control Plane"
        assert data["version"] == "0.1.0"
        assert data["docs"] == "/api/docs"
