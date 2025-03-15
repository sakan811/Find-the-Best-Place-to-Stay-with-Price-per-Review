"""
Global pytest configuration for the backend.
"""
import pytest

# Define pytest plugins at the top level
pytest_plugins = ["pytest_asyncio"]

# Configure pytest-asyncio to use session scope by default
def pytest_configure(config):
    """Configure pytest-asyncio to use session-scoped event loops by default."""
    # Set the default event loop scope for asyncio marker
    config.addinivalue_line(
        "markers",
        "asyncio: mark test to run with asyncio, default loop_scope=session"
    )

# This tells pytest-asyncio to use session scope for fixture event loops
def pytest_addoption(parser):
    """Add pytest-asyncio options to the command line."""
    parser.addini(
        "asyncio_default_fixture_loop_scope",
        help="default event loop scope for async fixtures",
        default="function"  # Using function scope as recommended in the warning
    )

@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio to use asyncio backend."""
    return "asyncio" 