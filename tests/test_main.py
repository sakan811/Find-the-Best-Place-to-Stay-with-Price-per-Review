import datetime

import pytest
import pytz

from main import scrape_graphql


def test_graphql_scraper():
    timezone = pytz.timezone('Asia/Tokyo')
    today = datetime.datetime.now(timezone)
    check_in = today.strftime('%Y-%m-%d')
    tomorrow = today + datetime.timedelta(days=1)
    check_out = tomorrow.strftime('%Y-%m-%d')
    df = scrape_graphql(city='Osaka', check_in=check_in, check_out=check_out, selected_currency='USD')

    assert not df.empty
    # Check column
    assert df.shape[1] == 7


if __name__ == '__main__':
    pytest.main()
