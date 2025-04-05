import pytest
import os
import json
from unittest.mock import patch, MagicMock

# No need to import client fixture as it's in conftest.py


# Update patch path to use components.api
@patch("components.api.run_async")
def test_health_check(mock_run_async, client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert data["message"] == "API is running"


# Update patch path to use components.api
@patch("components.api.run_async")
def test_extract_headers_endpoint_success(mock_run_async, client):
    """Test successful header extraction via the API endpoint."""
    # Setup mock extractor with headers
    mock_extractor = MagicMock()
    mock_extractor.headers = {
        "USER_AGENT": "test-user-agent",
        "X_BOOKING_CSRF_TOKEN": "test-csrf-token",
    }
    mock_run_async.return_value = mock_extractor

    # Make the request without save parameter
    response = client.get("/extract-headers")

    # Assertions
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["headers"] == mock_extractor.headers
    assert data["saved_to_file"] is False

    # Make sure write_env_variables was not called
    mock_extractor.write_env_variables.assert_not_called()


# Update patch path to use components.api
@patch("components.api.run_async")
def test_extract_headers_endpoint_with_save(mock_run_async, client):
    """Test header extraction with save parameter."""
    # Setup mock extractor with headers
    mock_extractor = MagicMock()
    mock_extractor.headers = {
        "USER_AGENT": "test-user-agent",
        "X_BOOKING_CSRF_TOKEN": "test-csrf-token",
    }
    mock_run_async.return_value = mock_extractor

    # Make the request with save=true
    response = client.get("/extract-headers?save=true")

    # Assertions
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["headers"] == mock_extractor.headers
    assert data["saved_to_file"] is True

    # Verify write_env_variables was called
    mock_extractor.write_env_variables.assert_called_once()


# Update patch path to use components.api
@patch("components.api.run_async")
def test_extract_headers_endpoint_failure(mock_run_async, client):
    """Test handling extraction failure via the API endpoint."""
    # Setup mock to return None (extraction failed)
    mock_run_async.return_value = None

    # Make the request
    response = client.get("/extract-headers")

    # Assertions
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["success"] is False
    assert "error" in data


# Update patch path to use components.api
@patch("components.api.run_async")
def test_extract_headers_endpoint_exception(mock_run_async, client):
    """Test handling exceptions in the extract-headers endpoint."""
    # Setup mock to raise an exception
    mock_run_async.side_effect = Exception("Test exception")

    # Make the request
    response = client.get("/extract-headers")

    # Assertions
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["success"] is False
    assert data["error"] == "Test exception"


@patch("os.path.exists")
@patch("builtins.open")
@patch("os.getcwd")
def test_get_headers_endpoint_success(mock_getcwd, mock_file, mock_exists, client):
    """Test successful header retrieval from .env file."""
    # Setup mocks
    mock_getcwd.return_value = "/mock/path"
    mock_exists.return_value = True
    
    # Mock file content properly for line-by-line reading
    mock_file_content = [
        'USER_AGENT="test-user-agent"\n',
        'X_BOOKING_CSRF_TOKEN="test-csrf-token"\n'
    ]
    
    # Configure the mock to return appropriate data when opened and read line by line
    mock_file.return_value.__enter__.return_value = mock_file_content
    mock_file.return_value.__iter__.return_value = iter(mock_file_content)
    
    # Make the request
    response = client.get("/get-headers")
    
    # Assertions
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["headers"] == {
        "USER_AGENT": "test-user-agent",
        "X_BOOKING_CSRF_TOKEN": "test-csrf-token"
    }


@patch("os.path.exists")
def test_get_headers_endpoint_no_file(mock_exists, client):
    """Test handling missing .env file in get-headers endpoint."""
    # Setup mock to indicate file doesn't exist
    mock_exists.return_value = False

    # Make the request
    response = client.get("/get-headers")

    # Assertions
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["success"] is False
    assert "No headers file found" in data["error"]


@patch("os.path.exists")
@patch("builtins.open")
def test_get_headers_endpoint_exception(mock_open, mock_exists, client):
    """Test handling exceptions in the get-headers endpoint."""
    # Setup mocks
    mock_exists.return_value = True
    mock_open.side_effect = Exception("Test exception")

    # Make the request
    response = client.get("/get-headers")

    # Assertions
    assert response.status_code == 500
    data = json.loads(response.data)
    assert data["success"] is False
    # Update to match the generic error message from the API
    assert data["error"] == "Error reading headers from file."


if __name__ == "__main__":
    pytest.main()