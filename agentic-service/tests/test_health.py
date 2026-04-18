"""
Tests — Health Endpoint
========================
Basic tests for the agentic service health and ready endpoints.

Run: pytest tests/test_health.py -v
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    from main import app
    return TestClient(app)


def test_health_returns_ok(client):
    """GET /health should return status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "krishi-sakhi-agentic"
    assert data["version"] == "0.1.0"


def test_ready_returns_components(client):
    """GET /ready should return component status."""
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data
    assert "components" in data
    assert "llm" in data["components"]
    assert "backend_api" in data["components"]


def test_root_returns_welcome(client):
    """GET / should return welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Krishi Sakhi" in data["message"]
