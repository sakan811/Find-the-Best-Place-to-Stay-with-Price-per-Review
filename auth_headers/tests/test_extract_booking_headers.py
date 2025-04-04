import pytest
from unittest.mock import patch, MagicMock, AsyncMock, mock_open

from extract_booking_headers import (
    BookingHeaderExtractor,
    extract_headers,
    main,
    TARGET_HEADERS,
    HEADER_TO_ENV,
)


class TestBookingHeaderExtractor:
    """Tests for the BookingHeaderExtractor class."""

    def test_init(self):
        """Test the constructor."""
        extractor = BookingHeaderExtractor()
        assert extractor.headers == {}
        assert extractor.completed is False

    @pytest.mark.asyncio
    async def test_handle_request_graphql_with_headers(self):
        """Test handling a GraphQL request with headers."""
        extractor = BookingHeaderExtractor()

        # Create mock route and request
        mock_route = AsyncMock()
        mock_request = MagicMock()
        mock_request.url = "https://www.booking.com/graphql"

        # Setup headers that would be present in a real request
        mock_headers = {header: f"test-value-{header}" for header in TARGET_HEADERS}
        mock_request.headers = mock_headers

        # Call the method
        await extractor.handle_request(mock_route, mock_request)

        # Verify the headers were collected
        assert extractor.completed is True
        for header, env_name in HEADER_TO_ENV.items():
            assert extractor.headers[env_name] == f"test-value-{header}"

        # Verify the route was continued
        mock_route.continue_.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_request_graphql_partial_headers(self):
        """Test handling a GraphQL request with only some of the needed headers."""
        extractor = BookingHeaderExtractor()

        # Create mock route and request
        mock_route = AsyncMock()
        mock_request = MagicMock()
        mock_request.url = "https://www.booking.com/graphql"

        # Setup only some of the headers
        partial_headers = {TARGET_HEADERS[0]: "test-value"}
        mock_request.headers = partial_headers

        # Call the method
        await extractor.handle_request(mock_route, mock_request)

        # Verify that we collected some headers but not completed
        assert extractor.completed is False
        assert HEADER_TO_ENV[TARGET_HEADERS[0]] in extractor.headers
        assert len(extractor.headers) == 1

        # Verify the route was continued
        mock_route.continue_.assert_called_once()

    @pytest.mark.asyncio
    async def test_handle_request_non_graphql(self):
        """Test handling a non-GraphQL request."""
        extractor = BookingHeaderExtractor()

        # Create mock route and request
        mock_route = AsyncMock()
        mock_request = MagicMock()
        mock_request.url = "https://www.booking.com/some-other-path"

        # Call the method
        await extractor.handle_request(mock_route, mock_request)

        # Verify no headers were collected for non-graphql requests
        assert extractor.headers == {}
        assert extractor.completed is False

        # Verify the route was continued
        mock_route.continue_.assert_called_once()

    @patch("auth_headers.extract_booking_headers.main_logger")
    @patch("os.environ.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.dirname")
    def test_write_env_variables_with_headers(
        self, mock_dirname, mock_file, mock_env_get, mock_logger
    ):
        """Test writing environment variables when headers are present."""
        # Setup
        extractor = BookingHeaderExtractor()
        extractor.headers = {
            "USER_AGENT": "test-user-agent",
            "X_BOOKING_CSRF_TOKEN": "test-csrf-token",
        }
        
        # Make sure mock_env_get returns None to prevent overwriting the USER_AGENT
        mock_env_get.return_value = None

        # Mock directory path for .env file
        mock_dirname.side_effect = lambda x: "/mock/path"

        # Call the method
        extractor.write_env_variables()

        # Verify the file was opened and written to correctly
        mock_file.assert_called_once()
        handle = mock_file()

        # Check that write was called for each header
        expected_calls = [
            f"USER_AGENT=test-user-agent\n",
            f"X_BOOKING_CSRF_TOKEN=test-csrf-token\n",
        ]
        write_calls = [call[0][0] for call in handle.write.call_args_list]
        assert sorted(write_calls) == sorted(expected_calls)

        # Verify that success was logged
        called_with_expected_message = False
        for call in mock_logger.info.call_args_list:
            args = call[0]
            if len(args) > 0 and isinstance(args[0], str) and "Environment variables saved to" in args[0]:
                called_with_expected_message = True
                break
        assert called_with_expected_message, "Log did not contain expected message about saving environment variables"

    @patch("auth_headers.extract_booking_headers.main_logger")
    def test_write_env_variables_no_headers(self, mock_logger):
        """Test trying to write environment variables when no headers are present."""
        # Setup
        extractor = BookingHeaderExtractor()
        extractor.headers = {}

        # Call the method
        extractor.write_env_variables()

        # Verify warning was logged and no further processing occurred
        mock_logger.warning.assert_called_once_with("No headers collected.")


@pytest.mark.asyncio
@patch("auth_headers.extract_booking_headers.async_playwright")
async def test_extract_headers_success(mock_playwright):
    """Test successful header extraction."""
    # Setup mocks
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    # Setup the playwright mock to return our mocked objects
    mock_playwright_instance = AsyncMock()
    mock_playwright.return_value.__aenter__.return_value = mock_playwright_instance
    mock_playwright_instance.chromium.launch.return_value = mock_browser
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    
    # Store the actual extractor when page.route is called
    actual_extractor = None
    
    # Mock page.route to capture and modify the actual extractor
    async def mock_route_func(pattern, handler):
        nonlocal actual_extractor
        # Extract the extractor from the handler (it's the self of the method)
        if hasattr(handler, "__self__"):
            actual_extractor = handler.__self__
            # Set it as completed with headers
            actual_extractor.completed = True
            actual_extractor.headers = {"USER_AGENT": "test-user-agent"}
    
    # Set the mocked route function
    mock_page.route = mock_route_func
    
    # Call the function
    result = await extract_headers()
    
    # Verify the result is a BookingHeaderExtractor with the headers
    assert result is not None
    assert isinstance(result, BookingHeaderExtractor)
    assert result.completed is True
    # Rest of assertions...


@pytest.mark.asyncio
@patch("auth_headers.extract_booking_headers.async_playwright")
async def test_extract_headers_failure(mock_playwright):
    """Test header extraction when an error occurs."""
    # Setup mocks to raise an exception
    mock_playwright.return_value.__aenter__.side_effect = Exception("Test exception")

    # Call the function
    result = await extract_headers()

    # Verify the result is None when an error occurs
    assert result is None


@pytest.mark.asyncio
@patch("auth_headers.extract_booking_headers.extract_headers")
async def test_main_calls_extract_headers(mock_extract_headers):
    """Test that main calls extract_headers and processes the result."""
    # Setup
    mock_extractor = MagicMock()
    mock_extract_headers.return_value = mock_extractor

    # Call the function
    await main()

    # Verify extract_headers was called and the result was processed
    mock_extract_headers.assert_called_once()
    mock_extractor.write_env_variables.assert_called_once()


if __name__ == "__main__":
    pytest.main()
