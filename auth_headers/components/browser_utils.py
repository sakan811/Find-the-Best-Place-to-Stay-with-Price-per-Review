"""
Browser interaction utilities using Playwright.
"""

import asyncio
from typing import Optional

from playwright.async_api import async_playwright

from .extractor import BookingHeaderExtractor
from logging_config import main_logger


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