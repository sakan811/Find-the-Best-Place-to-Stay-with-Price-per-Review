import datetime
import unittest.mock as mock

import pytest
import pandas as pd

from scraper.graphql_scraper import Scraper


def generate_mock_response(city, country, check_in, check_out, adults, children, rooms, currency, hotel_filter=True, results_total=50):
    """Generate a mock response for the GraphQL API"""
    filter_options = []
    if hotel_filter:
        filter_options.append({"urlId": "ht_id=204"})
        
    return {
        "data": {
            "searchQueries": {
                "search": {
                    "appliedFilterOptions": filter_options,
                    "pagination": {"nbResultsTotal": results_total},
                    "breadcrumbs": [
                        {"name": country, "destType": "COUNTRY"},
                        {"name": city, "destType": "CITY"},
                    ],
                    "flexibleDatesConfig": {
                        "dateRangeCalendar": {
                            "checkin": [check_in],
                            "checkout": [check_out],
                        }
                    },
                    "searchMeta": {
                        "nbAdults": adults,
                        "nbChildren": children,
                        "nbRooms": rooms
                    },
                    "results": [{"blocks": [{"finalPrice": {"currency": currency}}]}],
                }
            }
        }
    }


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

    # Create a mock response
    mock_data = generate_mock_response(
        city=city,
        country=country,
        check_in=check_in,
        check_out=check_out,
        adults=group_adults,
        children=group_children,
        rooms=num_rooms,
        currency=selected_currency,
        hotel_filter=hotel_filter
    )
    
    # Create empty DataFrame to return from _scrape_all_pages
    mock_df = pd.DataFrame({
        'Hotel': ['Test Hotel'],
        'Review': [4.5],
        'Price': [100],
        'AccommodationName': ['Hotel'],
        'City': [city],
        'CheckIn': [check_in],
        'CheckOut': [check_out],
        'AsOf': [datetime.datetime.now().strftime("%Y-%m-%d")],
        'Price/Review': [22.22]
    })

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
    
    # Patch the methods that make API requests
    with mock.patch.object(scraper, '_fetch_data', return_value=mock_data):
        with mock.patch.object(scraper, '_scrape_all_pages', return_value=mock_df):
            df = scraper.scrape_graphql()

    assert not df.empty
    # Check column count
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

    # Create a mock response
    mock_data = generate_mock_response(
        city=city,
        country=country,
        check_in=check_in,
        check_out=check_out,
        adults=group_adults,
        children=group_children,
        rooms=num_rooms,
        currency=selected_currency,
        hotel_filter=hotel_filter
    )
    
    # Create empty DataFrame to return from _scrape_all_pages
    mock_df = pd.DataFrame({
        'Hotel': ['Test Hotel'],
        'Review': [4.5],
        'Price': [100],
        'AccommodationName': ['Hotel'],
        'City': [city],
        'CheckIn': [check_in],
        'CheckOut': [check_out],
        'AsOf': [datetime.datetime.now().strftime("%Y-%m-%d")],
        'Price/Review': [22.22]
    })

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
    
    # Patch the methods that make API requests
    with mock.patch.object(scraper, '_fetch_data', return_value=mock_data):
        with mock.patch.object(scraper, '_scrape_all_pages', return_value=mock_df):
            df = scraper.scrape_graphql()

    assert not df.empty
    # Check column count
    assert df.shape[1] == 9


if __name__ == "__main__":
    pytest.main()
