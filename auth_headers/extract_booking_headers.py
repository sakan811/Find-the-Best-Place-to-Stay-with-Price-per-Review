"""
Script to extract Booking.com headers using Playwright.

This script navigates to Booking.com, intercepts requests to extract required headers,
and outputs them as environment variables.
"""

import asyncio
import os
from typing import Dict, Optional

from playwright.async_api import async_playwright, Request, Route

from auth_headers.logging_config import main_logger

# Headers we want to extract from Booking.com
TARGET_HEADERS = [
    "user-agent",
    "x-booking-context-action-name",
    "x-booking-context-aid",
    "x-booking-csrf-token",
    "x-booking-et-serialized-state",
    "x-booking-pageview-id",
    "x-booking-site-type-id",
    "x-booking-topic",
]

# Map from header name to environment variable name
HEADER_TO_ENV = {
    "user-agent": "USER_AGENT",
    "x-booking-context-action-name": "X_BOOKING_CONTEXT_ACTION_NAME",
    "x-booking-context-aid": "X_BOOKING_CONTEXT_AID",
    "x-booking-csrf-token": "X_BOOKING_CSRF_TOKEN",
    "x-booking-et-serialized-state": "X_BOOKING_ET_SERIALIZED_STATE",
    "x-booking-pageview-id": "X_BOOKING_PAGEVIEW_ID",
    "x-booking-site-type-id": "X_BOOKING_SITE_TYPE_ID",
    "x-booking-topic": "X_BOOKING_TOPIC",
}


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

        # Write to a .env file at the same level as the docker-compose file
        try:
            # Get the path to the root directory (where docker-compose.yml is located)
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env_file_path = os.path.join(root_dir, ".env")

            with open(env_file_path, "w") as env_file:
                for key, value in self.headers.items():
                    env_file.write(f"{key}={value}\n")
            main_logger.info(f"Environment variables saved to {env_file_path}")
        except IOError as e:
            main_logger.error(f"Failed to write to .env file: {e}")


async def extract_headers() -> Optional[BookingHeaderExtractor]:
    """Extract headers from Booking.com and return the extractor object."""
    main_logger.info("Starting Booking.com header extraction...")

    try:
        async with async_playwright() as p:
            # Launch the browser
            browser = await p.chromium.launch(
                headless=True
            )  # Set to True for production
            context = await browser.new_context()

            # Create a new page
            page = await context.new_page()

            # Setup the header extractor
            extractor = BookingHeaderExtractor()

            # Route all requests through the handler
            await page.route("**/*", extractor.handle_request)

            # Navigate to Booking.com
            main_logger.info("Navigating to Booking.com...")
            await page.goto("https://www.booking.com/")

            # Wait for navigation and some interaction
            main_logger.info(
                "Waiting for page to load and sending initial interactions..."
            )
            await page.wait_for_load_state("networkidle")

            # Click on some elements to trigger API calls
            try:
                # Click search button using the provided CSS selector
                await page.click(
                    "#indexsearch > div.hero-banner-searchbox > div > form > div > div.e22b782521.d12ff5f5bf > button",
                    timeout=5000,
                )
            except Exception as e:
                main_logger.warning(f"Could not interact with search button: {e}")

            # Wait a bit for requests to be processed
            await asyncio.sleep(5)

            # If headers are not collected yet, try another page
            if not extractor.completed:
                main_logger.info("Trying to navigate to search results page...")
                await page.goto(
                    "https://www.booking.com/searchresults.html?ss=New+York"
                )
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(5)

            # Close the browser
            await browser.close()

            if extractor.completed:
                main_logger.info("Successfully extracted Booking.com headers!")
                return extractor
            else:
                main_logger.error(
                    "Could not extract all required headers. Please try running the script again."
                )
                return None
    except Exception as e:
        main_logger.error(f"Error during header extraction: {e}")
        return None


async def main():
    """Main function to run the header extraction."""
    # Extract headers
    extractor = await extract_headers()

    if extractor:
        # Output as environment variables
        extractor.write_env_variables()


if __name__ == "__main__":
    asyncio.run(main())
