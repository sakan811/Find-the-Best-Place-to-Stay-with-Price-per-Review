import pytest
import os
from unittest.mock import patch, MagicMock, AsyncMock, mock_open

# Update imports to use the modular components
from components.constants import TARGET_HEADERS, HEADER_TO_ENV
from components.extractor import BookingHeaderExtractor


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

    # Update patch paths to use components.extractor
    @patch("components.extractor.main_logger")
    @patch("os.environ.get")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.getcwd")
    def test_write_env_variables_with_headers(
        self, mock_getcwd, mock_file, mock_env_get, mock_logger
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
        mock_getcwd.return_value = "/mock/path"

        # Call the method
        extractor.write_env_variables()

        # Verify the file was opened and written to correctly
        mock_file.assert_called_once_with(os.path.join("/mock/path", ".env"), "w")
        handle = mock_file()

        # Check that write was called for each header
        expected_calls = [
            'USER_AGENT="test-user-agent"\n',
            'X_BOOKING_CSRF_TOKEN="test-csrf-token"\n',
        ]
        write_calls = [call[0][0] for call in handle.write.call_args_list]
        assert sorted(write_calls) == sorted(expected_calls)

        # Verify that success was logged
        called_with_expected_message = False
        for call in mock_logger.info.call_args_list:
            args = call[0]
            if (
                len(args) > 0
                and isinstance(args[0], str)
                and "Environment variables saved to" in args[0]
            ):
                called_with_expected_message = True
                break
        assert called_with_expected_message, (
            "Log did not contain expected message about saving environment variables"
        )

    # Update patch path to use components.extractor
    @patch("components.extractor.main_logger")
    def test_write_env_variables_no_headers(self, mock_logger):
        """Test trying to write environment variables when no headers are present."""
        # Setup
        extractor = BookingHeaderExtractor()
        extractor.headers = {}

        # Call the method
        extractor.write_env_variables()

        # Verify warning was logged and no further processing occurred
        mock_logger.warning.assert_called_once_with("No headers collected.")


if __name__ == "__main__":
    pytest.main()