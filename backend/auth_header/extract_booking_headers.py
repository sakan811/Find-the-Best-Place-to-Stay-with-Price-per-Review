#!/usr/bin/env python3
"""
Script to extract Booking.com headers using Playwright.

This script navigates to Booking.com, intercepts requests to extract required headers,
and outputs them as environment variables.
"""

import asyncio
import sys
from typing import Dict, Optional

from playwright.async_api import async_playwright, Request, Route


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
            print(f"Intercepted request to: {request.url}", file=sys.stderr)

            # Extract headers
            request_headers = request.headers

            for header_name in TARGET_HEADERS:
                if header_name in request_headers:
                    env_var_name = HEADER_TO_ENV[header_name]
                    self.headers[env_var_name] = request_headers[header_name]

            # Check if we have all the headers we need
            if all(env_var in self.headers for env_var in HEADER_TO_ENV.values()):
                self.completed = True
                print("All required headers collected!", file=sys.stderr)

        # Always allow the request to continue
        await route.continue_()

    def print_env_variables(self) -> None:
        """
        Print headers as environment variables.
        """
        if not self.headers:
            print("No headers collected.", file=sys.stderr)
            return

        # Output plain environment variables (KEY=VALUE format)
        for key, value in self.headers.items():
            print(f"{key}={value}")


async def extract_headers() -> Optional[BookingHeaderExtractor]:
    """Extract headers from Booking.com and return the extractor object."""
    print("Starting Booking.com header extraction...", file=sys.stderr)

    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=True)  # Set to True for production
        context = await browser.new_context()

        # Create a new page
        page = await context.new_page()

        # Setup the header extractor
        extractor = BookingHeaderExtractor()

        # Route all requests through the handler
        await page.route("**/*", extractor.handle_request)

        # Navigate to Booking.com
        print("Navigating to Booking.com...", file=sys.stderr)
        await page.goto("https://www.booking.com/")

        # Wait for navigation and some interaction
        print("Waiting for page to load and sending initial interactions...", file=sys.stderr)
        await page.wait_for_load_state("networkidle")

        # Click on some elements to trigger API calls
        try:
            # Click search button using the provided CSS selector
            await page.click('#indexsearch > div.hero-banner-searchbox > div > form > div > div.e22b782521.d12ff5f5bf > button', timeout=5000)
        except Exception as e:
            print(f"Could not interact with search button: {e}", file=sys.stderr)

        # Wait a bit for requests to be processed
        await asyncio.sleep(5)

        # If headers are not collected yet, try another page
        if not extractor.completed:
            print("Trying to navigate to search results page...", file=sys.stderr)
            await page.goto("https://www.booking.com/searchresults.html?ss=New+York")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(5)

        # Close the browser
        await browser.close()

        if extractor.completed:
            print("Successfully extracted Booking.com headers!", file=sys.stderr)
            return extractor
        else:
            print("Could not extract all required headers. Please try running the script again.", file=sys.stderr)
            return None


async def main():
    """Main function to run the header extraction."""
    # Extract headers
    extractor = await extract_headers()
    
    if extractor:
        # Output as environment variables
        extractor.print_env_variables()


if __name__ == "__main__":
    asyncio.run(main())
