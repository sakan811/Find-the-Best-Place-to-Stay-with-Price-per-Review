import datetime

import pytest

from scraper.graphql_scraper import Scraper


def test_graphql_scraper():
    city = "London"
    country = "United Kingdom"

    today = datetime.datetime.now()
    check_in = today.strftime("%Y-%m-%d")
    tomorrow = today + datetime.timedelta(days=1)
    check_out = tomorrow.strftime("%Y-%m-%d")

    group_adults = 1
    num_rooms = 1
    group_children = 0
    selected_currency = "USD"
    hotel_filter = True

    scraper = Scraper(
        city=city,
        country=country,
        check_in=check_in,
        check_out=check_out,
        group_adults=group_adults,
        group_children=group_children,
        num_rooms=num_rooms,
        hotel_filter=hotel_filter,
        selected_currency=selected_currency,
    )
    df = scraper.scrape_graphql()

    assert not df.empty
    # Check column count (updated to match actual columns)
    assert df.shape[1] == 9


def test_graphql_scraper_all_properties():
    city = "London"
    country = "United Kingdom"

    today = datetime.datetime.now()
    check_in = today.strftime("%Y-%m-%d")
    tomorrow = today + datetime.timedelta(days=1)
    check_out = tomorrow.strftime("%Y-%m-%d")

    group_adults = 1
    num_rooms = 1
    group_children = 0
    selected_currency = "USD"
    hotel_filter = False

    scraper = Scraper(
        city=city,
        country=country,
        check_in=check_in,
        check_out=check_out,
        group_adults=group_adults,
        group_children=group_children,
        num_rooms=num_rooms,
        hotel_filter=hotel_filter,
        selected_currency=selected_currency,
    )
    df = scraper.scrape_graphql()

    assert not df.empty
    # Check column count (updated to match actual columns)
    assert df.shape[1] == 9


if __name__ == "__main__":
    pytest.main()
