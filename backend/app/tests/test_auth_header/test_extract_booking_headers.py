"""
Tests for the extract_booking_headers module.
"""
import asyncio
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
from io import StringIO

from auth_header.extract_booking_headers import (
    BookingHeaderExtractor,
    extract_headers,
    HEADER_TO_ENV,
    TARGET_HEADERS,
)


@pytest.fixture
def header_extractor():
    """Fixture that returns a BookingHeaderExtractor instance."""
    return BookingHeaderExtractor()


class TestBookingHeaderExtractor:
    """Tests for the BookingHeaderExtractor class."""

    def test_init(self, header_extractor):
        """Test that the constructor initializes properties correctly."""
        assert header_extractor.headers == {}
        assert header_extractor.completed is False

    @pytest.mark.asyncio(loop_scope="session")
    async def test_handle_request_non_graphql(self, header_extractor):
        """Test that non-GraphQL requests don't extract headers."""
        # Setup mocks
        route_mock = AsyncMock()
        request_mock = MagicMock()
        request_mock.url = "https://booking.com/some/path"
        request_mock.headers = {}

        # Call the function
        await header_extractor.handle_request(route_mock, request_mock)

        # Assert
        assert header_extractor.headers == {}
        assert not header_extractor.completed
        route_mock.continue_.assert_called_once()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_handle_request_graphql_with_headers(self, header_extractor):
        """Test that GraphQL requests extract headers."""
        # Setup mock headers
        mock_headers = {header: f"value-{header}" for header in TARGET_HEADERS}
        
        # Setup mocks
        route_mock = AsyncMock()
        request_mock = MagicMock()
        request_mock.url = "https://booking.com/graphql"
        request_mock.headers = mock_headers

        # Call the function
        await header_extractor.handle_request(route_mock, request_mock)

        # Assert
        expected_headers = {HEADER_TO_ENV[h]: mock_headers[h] for h in TARGET_HEADERS}
        assert header_extractor.headers == expected_headers
        assert header_extractor.completed
        route_mock.continue_.assert_called_once()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_handle_request_graphql_partial_headers(self, header_extractor):
        """Test that GraphQL requests with partial headers are handled correctly."""
        # Use only the first header
        partial_headers = {TARGET_HEADERS[0]: f"value-{TARGET_HEADERS[0]}"}
        
        # Setup mocks
        route_mock = AsyncMock()
        request_mock = MagicMock()
        request_mock.url = "https://booking.com/graphql"
        request_mock.headers = partial_headers

        # Call the function
        await header_extractor.handle_request(route_mock, request_mock)

        # Assert
        expected_headers = {HEADER_TO_ENV[TARGET_HEADERS[0]]: partial_headers[TARGET_HEADERS[0]]}
        assert header_extractor.headers == expected_headers
        assert not header_extractor.completed  # Should not be complete with partial headers
        route_mock.continue_.assert_called_once()

    def test_print_env_variables_with_headers(self, header_extractor, monkeypatch):
        """Test that headers are properly formatted as environment variables."""
        # Setup mock headers
        header_extractor.headers = {
            "USER_AGENT": "test-user-agent",
            "X_BOOKING_CONTEXT_AID": "test-aid",
        }
        
        # Capture stdout
        captured_stdout = StringIO()
        monkeypatch.setattr(sys, "stdout", captured_stdout)
        
        # Call the function
        header_extractor.print_env_variables()
        
        # Assert
        output = captured_stdout.getvalue().strip().split('\n')
        assert len(output) == 2
        assert "USER_AGENT=test-user-agent" in output
        assert "X_BOOKING_CONTEXT_AID=test-aid" in output

    def test_print_env_variables_no_headers(self, header_extractor, monkeypatch):
        """Test that no output is produced when no headers are collected."""
        # Capture stdout and stderr
        captured_stdout = StringIO()
        captured_stderr = StringIO()
        monkeypatch.setattr(sys, "stdout", captured_stdout)
        monkeypatch.setattr(sys, "stderr", captured_stderr)
        
        # Call the function
        header_extractor.print_env_variables()
        
        # Assert
        assert captured_stdout.getvalue() == ""
        assert "No headers collected." in captured_stderr.getvalue()


@patch('auth_header.extract_booking_headers.async_playwright')
@pytest.mark.asyncio(loop_scope="session")
async def test_extract_headers_success(mock_playwright):
    """Test successful header extraction."""
    # Setup mocks
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    # Configure mock chain
    mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Make route handler trigger completion
    async def side_effect(url_pattern, handler):
        # Create mock route and request
        mock_route = AsyncMock()
        mock_request = MagicMock()
        mock_request.url = "https://booking.com/graphql"
        mock_request.headers = {header: f"value-{header}" for header in TARGET_HEADERS}
        
        # Call the handler
        await handler(mock_route, mock_request)
    
    # Assign side effect to route method
    mock_page.route.side_effect = side_effect
    
    # Call the function
    result = await extract_headers()
    
    # Assert
    assert result is not None
    assert result.completed
    assert len(result.headers) == len(TARGET_HEADERS)
    mock_browser.close.assert_called_once()


@patch('auth_header.extract_booking_headers.async_playwright')
@pytest.mark.asyncio(loop_scope="session")
async def test_extract_headers_failure(mock_playwright):
    """Test header extraction failure."""
    # Setup mocks
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    # Configure mock chain
    mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Make route handler NOT trigger completion (no headers)
    async def side_effect(url_pattern, handler):
        # Create mock route and request with no headers
        mock_route = AsyncMock()
        mock_request = MagicMock()
        mock_request.url = "https://booking.com/graphql"
        mock_request.headers = {}
        
        # Call the handler
        await handler(mock_route, mock_request)
    
    # Assign side effect to route method
    mock_page.route.side_effect = side_effect
    
    # Call the function
    result = await extract_headers()
    
    # Assert
    assert result is None
    mock_browser.close.assert_called_once()


@patch('auth_header.extract_booking_headers.extract_headers')
@patch('auth_header.extract_booking_headers.asyncio.run')
def test_main_calls_extract_headers(mock_run, mock_extract_headers):
    """Test that main calls extract_headers and prints output."""
    # Import the function to test
    from auth_header.extract_booking_headers import main
    
    # Setup mocks
    extractor_mock = MagicMock()
    mock_extract_headers.return_value = extractor_mock
    
    # Create a mock event loop that runs main directly
    def run_main(coro):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
    
    mock_run.side_effect = run_main
    
    # Call the function (via asyncio.run which we've mocked)
    asyncio.run(main())
    
    # Assert
    mock_extract_headers.assert_called_once()
    extractor_mock.print_env_variables.assert_called_once()


if __name__ == "__main__":
    pytest.main() 