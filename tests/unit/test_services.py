"""Unit tests for IaaS Platform services - Hybrid Architecture."""

import pytest
from fastapi.testclient import TestClient

from src.api_gateway.main import app as api_gateway_app
from src.control_plane.main import app as control_plane_app
from src.failover_manager.main import app as failover_manager_app


# =============================================================================
# API Gateway Tests
# =============================================================================

@pytest.fixture
def api_gateway_client():
    """Create a test client for the API Gateway."""
    return TestClient(api_gateway_app)


class TestAPIGateway:
    """Tests for API Gateway service."""

    def test_health_endpoint(self, api_gateway_client):
        """Test that health endpoint returns healthy status."""
        response = api_gateway_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "api-gateway"
        assert data["architecture"] == "hybrid"
        assert "crossplane" in data["uses"]
        assert "nats" in data["uses"]

    def test_root_endpoint(self, api_gateway_client):
        """Test that root endpoint returns API information."""
        response = api_gateway_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "IaaS Platform API Gateway"
        assert data["version"] == "0.1.0"
        assert data["architecture"] == "hybrid"

    def test_openapi_endpoint(self, api_gateway_client):
        """Test that OpenAPI endpoint is accessible."""
        response = api_gateway_client.get("/api/openapi.json")
        assert response.status_code == 200

    def test_docs_endpoint(self, api_gateway_client):
        """Test that Swagger UI docs endpoint is accessible."""
        response = api_gateway_client.get("/api/docs")
        assert response.status_code == 200


# =============================================================================
# Control Plane Tests
# =============================================================================

@pytest.fixture
def control_plane_client():
    """Create a test client for the Control Plane."""
    return TestClient(control_plane_app)


class TestControlPlane:
    """Tests for Control Plane service."""

    def test_health_endpoint(self, control_plane_client):
        """Test that health endpoint returns healthy status."""
        response = control_plane_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "control-plane"
        assert data["architecture"] == "hybrid"
        assert "crossplane" in data["uses"]

    def test_root_endpoint(self, control_plane_client):
        """Test that root endpoint returns service information."""
        response = control_plane_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "IaaS Platform Control Plane"
        assert data["version"] == "0.1.0"
        assert data["architecture"] == "hybrid"
        assert data["crossplane_integration"] == "enabled"


# =============================================================================
# Failover Manager Tests
# =============================================================================

@pytest.fixture
def failover_manager_client():
    """Create a test client for the Failover Manager."""
    return TestClient(failover_manager_app)


class TestFailoverManager:
    """Tests for Failover Manager service."""

    def test_health_endpoint(self, failover_manager_client):
        """Test that health endpoint returns healthy status."""
        response = failover_manager_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "failover-manager"
        assert data["architecture"] == "hybrid"
        assert data["primary_differentiator"] is True

    def test_root_endpoint(self, failover_manager_client):
        """Test that root endpoint returns service information."""
        response = failover_manager_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "IaaS Platform Failover Manager"
        assert data["version"] == "0.1.0"
        assert data["architecture"] == "hybrid"
        assert data["unique_value"] == "automatic_multi_provider_failover"
