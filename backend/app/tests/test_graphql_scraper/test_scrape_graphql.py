import datetime
import pytest
import pytz
from scraper.graphql_scraper import Scraper
from requests.exceptions import RequestException

MAX_RETRIES = 3  # Retry up to 3 times for transient errors


def get_today_and_tomorrow(timezone='Asia/Tokyo'):
    """Helper function to get today's and tomorrow's dates in the given timezone."""
    tz = pytz.timezone(timezone)
    today = datetime.datetime.now(tz)
    tomorrow = today + datetime.timedelta(days=1)
    return today.strftime('%Y-%m-%d'), tomorrow.strftime('%Y-%m-%d')


def scrape_with_retries(scraper, max_retries=MAX_RETRIES):
    """Helper function to add retry logic for transient errors."""
    for attempt in range(1, max_retries + 1):
        try:
            df = scraper.scrape_graphql()
            if not df.empty:
                return df  # Successful scrape
        except RequestException as e:
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt == max_retries:
                raise  # Raise the exception if max retries are reached
    raise Exception("All retry attempts failed.")


@pytest.mark.parametrize("hotel_filter", [True, False])
def test_graphql_scraper(hotel_filter):
    """Test scraper with and without filtering hotels."""
    city = 'Tokyo'
    country = 'Japan'
    check_in, check_out = get_today_and_tomorrow()

    scraper = Scraper(
        city=city, country=country, check_in=check_in, check_out=check_out,
        group_adults=1, group_children=0, num_rooms=1,
        hotel_filter=hotel_filter, selected_currency='USD'
    )

    df = scrape_with_retries(scraper)

    assert not df.empty, "The scraped DataFrame is empty."
    assert df.shape[1] == 8, f"Expected 8 columns but got {df.shape[1]}."


if __name__ == '__main__':
    pytest.main()
