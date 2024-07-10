import datetime

import pytest
import pytz

from scraper.graphql_scraper import scrape_graphql


def test_graphql_scraper():
    city = 'Tokyo'

    timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.datetime.now(timezone)
    check_in = today.strftime('%Y-%m-%d')
    tomorrow = today + datetime.timedelta(days=1)
    check_out = tomorrow.strftime('%Y-%m-%d')

    group_adults = 1
    num_rooms = 1
    group_children = 0
    selected_currency = 'USD'
    hotel_filter = True

    df = scrape_graphql(city=city, check_in=check_in, check_out=check_out,
                        group_adults=group_adults, group_children=group_children,
                        num_rooms=num_rooms, hotel_filter=hotel_filter,
                        selected_currency=selected_currency)

    assert not df.empty
    # Check column
    assert df.shape[1] == 8


if __name__ == '__main__':
    pytest.main()
