"""
Header extraction functionality using Playwright.
"""

import os
from typing import Dict

from playwright.async_api import Route, Request

from .constants import TARGET_HEADERS, HEADER_TO_ENV
from logging_config import main_logger


class BookingHeaderExtractor:
    """Class for extracting booking.com headers using Playwright."""

    def __init__(self):
        self.headers: Dict[str, str] = {}
        self.completed = False

    async def handle_request(self, route: Route, request: Request) -> None:
        """Intercept requests to collect headers."""
        # Focus on GraphQL requests as they contain authentication headers
        if "graphql" in request.url and not self.completed:
            main_logger.info(f"Intercepted request to: {request.url}")

            # Extract headers
            request_headers = request.headers

            for header_name in TARGET_HEADERS:
                if header_name in request_headers:
                    env_var_name = HEADER_TO_ENV[header_name]
                    self.headers[env_var_name] = request_headers[header_name]

            # Check if we have all the headers we need
            if all(env_var in self.headers for env_var in HEADER_TO_ENV.values()):
                self.completed = True
                main_logger.info("All required headers collected!")

        # Always allow the request to continue
        await route.continue_()

    def write_env_variables(self) -> None:
        """
        save and set headers as environment variables.
        """
        if not self.headers:
            main_logger.warning("No headers collected.")
            return

        # Use USER_AGENT from environment if available
        docker_user_agent = os.environ.get("USER_AGENT")
        if docker_user_agent:
            main_logger.info("Using USER_AGENT from environment variables")
            self.headers["USER_AGENT"] = docker_user_agent

        # Write to a .env file in the application directory
        try:
            # Use the current working directory or /app in Docker
            env_file_path = os.path.join(os.getcwd(), ".env")

            with open(env_file_path, "w") as env_file:
                for key, value in self.headers.items():
                    # Quote the value to handle special characters
                    env_file.write(f'{key}="{value}"\n')
            main_logger.info(f"Environment variables saved to {env_file_path}")
        except IOError as e:
            main_logger.error(f"Failed to write to .env file: {e}")