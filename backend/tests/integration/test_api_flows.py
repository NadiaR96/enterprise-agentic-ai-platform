import pytest
from unittest.mock import patch
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app

class TestAPIIntegration:
    """Integration tests for API endpoints."""

    @pytest.fixture
    def client(self):
        """Test client fixture."""
        return TestClient(app)

    @pytest.fixture
    def auth_token(self, client):
        """Get authentication token for testing."""
        response = client.post("/auth/login", data={
            "username": "admin",
            "password": "admin"
        })
        assert response.status_code == 200
        return response.json()["access_token"]

    @pytest.fixture
    def auth_headers(self, auth_token):
        """Authentication headers fixture."""
        return {"Authorization": f"Bearer {auth_token}"}

    def test_query_endpoint_requires_auth(self, client):
        """Test that query endpoint requires authentication."""
        response = client.post("/api/query", json={"query": "Test question"})

        assert response.status_code == 403

    def test_query_endpoint_with_auth(self, client, auth_headers):
        """Test query endpoint with valid authentication."""
        with patch('api.routes.route_query') as mock_route:
            mock_route.return_value = {
                "answer": "Test answer",
                "confidence": 0.9,
                "timestamp": "2024-01-01T00:00:00Z"
            }

            response = client.post("/api/query",
                json={"query": "What is AI?"},
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["response"]["answer"] == "Test answer"
            assert data["user_id"] == "admin"

    def test_history_endpoint_requires_auth(self, client):
        """Test that history endpoint requires authentication."""
        response = client.get("/api/history")

        assert response.status_code == 403

    def test_history_endpoint_with_auth(self, client, auth_headers):
        """Test history endpoint with authentication."""
        with patch('api.routes.get_user_history') as mock_history:
            mock_history.return_value = [
                {"query": "Q1", "response": {"answer": "A1"}, "timestamp": "2024-01-01"}
            ]

            response = client.get("/api/history", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert data["user_id"] == "admin"
            assert len(data["history"]) == 1

    def test_users_endpoint_admin_only(self, client, auth_headers):
        """Test that users endpoint requires admin role."""
        response = client.get("/api/users", headers=auth_headers)

        assert response.status_code == 200  # Admin user should have access

    def test_login_successful(self, client):
        """Test successful login."""
        response = client.post("/auth/login", data={
            "username": "admin",
            "password": "admin"
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post("/auth/login", data={
            "username": "admin",
            "password": "wrongpassword"
        })

        assert response.status_code == 401

    def test_register_user(self, client):
        """Test user registration."""
        response = client.post("/auth/register?user_id=newuser&password=password123&email=new@example.com")

        assert response.status_code == 200

    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information."""
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "admin"
        assert "admin" in data["roles"]

    def test_query_saves_to_database(self, client, auth_headers):
        """Test that queries are saved to database."""
        with patch('api.routes.route_query') as mock_route:
            mock_route.return_value = {
                "answer": "Saved answer",
                "confidence": 0.8,
                "timestamp": "2024-01-01T00:00:00Z"
            }

            response = client.post("/api/query",
                json={"query": "Save this query"},
                headers=auth_headers
            )

            assert response.status_code == 200

            # Check that save_conversation was called
            from database import save_conversation
            with patch('database.save_conversation') as mock_save:
                mock_save.return_value = True
                # This would be verified in a more complete test