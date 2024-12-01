import re

from playwright import sync_api
from playwright.sync_api import sync_playwright

# Global flag to track if we've intercepted a request
intercepted = False

ENV_FILENAME = '.env'


def extract_x_headers() -> None:
    """
    Extract X-headers from Booking.com using Playwright.

    This function launches a Chromium browser, navigates to Booking.com,
    performs a search for "Tokyo", and intercepts network requests to
    extract X-headers used in GraphQL requests.

    The function uses the global 'intercepted' flag to track if a request
    has been intercepted, and the 'handle_request' function to process
    intercepted requests.

    :return: None
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Enable request interception
        page.on("request", handle_request)

        # Navigate to Booking.com
        page.goto("https://www.booking.com")

        # Perform a search to trigger GraphQL requests
        page.fill('input[name="ss"]', "Tokyo")
        page.press('input[name="ss"]', "Enter")

        # Wait for navigation and GraphQL requests
        page.wait_for_load_state("networkidle")

        browser.close()


def handle_request(request: sync_api.Request) -> None:
    """
    Handle intercepted requests from Booking.com to extract X-headers.

    This function is called for each intercepted request. It checks if the request
    is a GraphQL request to Booking.com and hasn't been intercepted before. If so,
    it extracts the relevant headers and updates the environment variables.

    :param request: The intercepted request object.
    :return: None
    """
    global intercepted
    if not intercepted and re.match(r"https://www\.booking\.com/dml/graphql.*", request.url):
        headers = request.headers
        env_vars = {}
        for key, value in headers.items():
            if key.startswith('x-') or key == 'user-agent':
                env_key = key.upper().replace('-', '_')
                env_vars[env_key] = value

        update_env_example(env_vars)
        intercepted = True  # Set the flag to True after intercepting


def update_env_example(env_vars: dict[str, str]) -> None:
    """
    Update the environment variables file with new X-headers.

    This function reads the '.env.example' file, updates the values of existing keys
    with new values from env_vars, and writes the result to a new file (ENV_FILENAME).

    :param env_vars: A dictionary of environment variables to update.
    :return: None
    """
    # Read from .env.example
    with open('.env.example', 'r') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        key = line.split('=')[0].strip()
        if key in env_vars:
            updated_lines.append(f"{key}={env_vars[key]}\n")
        else:
            updated_lines.append(line)

    # Write to .env instead of .env.example
    with open(ENV_FILENAME, 'w') as f:
        f.writelines(updated_lines)

    print(f"Headers updated in {ENV_FILENAME} file")


if __name__ == "__main__":
    extract_x_headers()