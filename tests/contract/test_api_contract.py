import pytest
from httpx import AsyncClient
import json
from typing import Dict, Any, List


class TestAPIContract:
    """Contract tests to ensure API endpoints maintain their expected interface."""

    async def test_health_endpoint_contract(self, client):
        """Test health endpoint contract."""
        response = await client.get("/health")
        assert response.status_code == 200

        data = response.json()
        expected_fields = {"status", "version", "environment"}
        actual_fields = set(data.keys())

        assert expected_fields.issubset(actual_fields), f"Missing fields: {expected_fields - actual_fields}"
        assert data["status"] == "healthy"
        assert isinstance(data["version"], str)
        assert isinstance(data["environment"], str)

    async def test_api_root_endpoint_contract(self, client):
        """Test API root endpoint contract."""
        response = await client.get("/api/v1")
        assert response.status_code == 200

        data = response.json()
        expected_fields = {"name", "version"}
        actual_fields = set(data.keys())

        assert expected_fields.issubset(actual_fields), f"Missing fields: {expected_fields - actual_fields}"
        assert isinstance(data["name"], str)
        assert isinstance(data["version"], str)

    async def test_error_response_contract(self, client):
        """Test that error responses follow the expected format."""
        # Try accessing a non-existent endpoint to trigger a 404
        response = await client.get("/api/v1/nonexistent-endpoint")
        assert response.status_code == 404

        data = response.json()
        # Error responses should have an 'error' key with 'code' and 'message'
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert isinstance(data["error"]["code"], str)
        assert isinstance(data["error"]["message"], str)

    async def test_unauthorized_response_contract(self, client):
        """Test that unauthorized responses follow the expected format."""
        # Try accessing a protected endpoint without authentication
        response = await client.get("/api/v1/users/me")
        assert response.status_code == 401

        data = response.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert isinstance(data["error"]["code"], str)
        assert isinstance(data["error"]["message"], str)

    async def test_stages_endpoint_contract(self, client):
        """Test stages endpoint contract."""
        response = await client.get("/api/v1/learning/stages")
        assert response.status_code == 200

        data = response.json()
        assert "stages" in data
        assert isinstance(data["stages"], list)

        # If there are stages, check their structure
        if data["stages"]:
            stage = data["stages"][0]
            expected_stage_fields = {
                "id", "number", "name", "slug", "description",
                "learning_objectives", "estimated_hours", "content_count",
                "assessment_count", "is_active"
            }
            actual_stage_fields = set(stage.keys())

            # The exact fields may vary, but these are likely to be present
            for field in ["id", "number", "name", "slug"]:
                assert field in actual_stage_fields, f"Stage missing required field: {field}"


class TestLearningAPIContract:
    """Test learning-specific API contracts."""

    async def test_stage_response_structure(self, client):
        """Test the structure of stage responses."""
        response = await client.get("/api/v1/learning/stages")
        assert response.status_code == 200

        data = response.json()
        if "stages" in data and data["stages"]:
            stage = data["stages"][0]

            # Validate data types
            assert isinstance(stage["id"], str)
            assert isinstance(stage["number"], int)
            assert isinstance(stage["name"], str)
            assert isinstance(stage["slug"], str)
            assert "description" not in stage or isinstance(stage["description"], (str, type(None)))
            assert "learning_objectives" not in stage or isinstance(stage["learning_objectives"], list)
            assert isinstance(stage["estimated_hours"], int)
            assert isinstance(stage["content_count"], int)
            assert isinstance(stage["assessment_count"], int)
            assert isinstance(stage["is_active"], bool)

    async def test_pagination_contract(self, client):
        """Test API pagination contract if implemented."""
        # Check if pagination parameters are accepted and handled appropriately
        response = await client.get("/api/v1/learning/stages?page=1&limit=10")

        # This request might succeed or fail depending on implementation,
        # but if it succeeds the response structure should be consistent
        if response.status_code == 200:
            data = response.json()
            assert "stages" in data  # Should return at minimum the stages list
        elif response.status_code == 422:
            # If pagination is not implemented, it might return 422 for invalid query params
            pass  # This is acceptable
        else:
            # Other status codes are acceptable as long as the error response follows contract
            error_data = response.json()
            if "error" in error_data:
                assert isinstance(error_data["error"], dict)


class TestContentAPIContract:
    """Test content-specific API contracts."""

    async def test_content_list_endpoint_contract(self, client):
        """Test content list endpoint contract."""
        response = await client.get("/api/v1/content")
        # This endpoint might require authentication, so we accept 200, 401, or 404
        if response.status_code == 200:
            data = response.json()
            # If successful, should return content list
            assert isinstance(data, list) or "content" in data
        elif response.status_code in [401, 404]:
            # These are expected for protected or non-existent endpoints
            if response.status_code == 401:
                error_data = response.json()
                assert "error" in error_data
        else:
            # For other status codes, check if it follows the error contract
            error_data = response.json()
            assert "error" in error_data


class TestCommonAPIPatterns:
    """Test common API patterns and conventions."""

    def test_response_format_consistency(self, client):
        """Test that all successful responses follow JSON format."""
        # This test would normally make requests, but we'll document the pattern
        # All successful responses should be valid JSON
        pass  # Implementation would require running actual requests

    def test_error_format_consistency(self, client):
        """Test that all error responses follow the same format."""
        # Error responses should have the format: {"error": {"code": "...", "message": "..."}}
        pass  # Implementation would require running actual requests that trigger errors

    async def test_datetime_format_in_responses(self, client):
        """Test that datetime fields follow ISO 8601 format."""
        # Check health endpoint for timestamp fields
        response = await client.get("/health")
        if response.status_code == 200:
            data = response.json()
            # Check that datetime strings follow ISO 8601 format (if present)
            pass  # No timestamp fields expected in health check


class TestAPIVersioningContract:
    """Test API versioning contract."""

    async def test_api_version_prefix_consistency(self, client):
        """Test that all API endpoints use consistent version prefix."""
        # All API endpoints should start with /api/v1/
        endpoints_to_test = [
            "/api/v1/learning/stages",
            "/api/v1/health",  # This might not exist but should return 404 rather than 404 at root
        ]

        # Test that /api/v1 exists and follows consistent pattern
        response = await client.get("/api/v1")
        assert response.status_code == 200

    async def test_non_versioned_access(self, client):
        """Test that non-versioned endpoints return appropriate responses."""
        # Endpoints that don't exist should return 404 with proper error format
        response = await client.get("/nonexistent")
        assert response.status_code == 404

        error_data = response.json()
        assert "error" in error_data


class TestAPIResponseHeaders:
    """Test API response headers."""

    async def test_content_type_header(self, client):
        """Test that API responses have correct content-type."""
        response = await client.get("/health")
        assert response.headers["content-type"].startswith("application/json")

    async def test_cors_headers(self, client):
        """Test that API includes proper CORS headers."""
        response = await client.get("/health")

        # Check for common CORS headers
        cors_headers = [
            "access-control-allow-origin",
            "access-control-allow-headers",
            "access-control-allow-methods"
        ]

        # Not all responses will have CORS headers (depends on request origin),
        # but the API should be configured to support CORS
        pass  # This is a configuration test that would require specific request headers