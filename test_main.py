import datetime
from unittest.mock import Mock

import numpy as np
import pandas as pd
import pytest
import pytz
import requests

from main import scrape_graphql, transform_data_in_df, extract_hotel_data, check_info, concat_df_list


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


def test_transform_data_in_df_basic():
    # Create a sample DataFrame
    data = {
        'Hotel': ['Hotel A', 'Hotel B', 'Hotel C', 'Hotel A'],
        'Review': [4.5, 3.0, 4.0, 4.5],
        'Price': [150, 200, 250, 150]
    }
    df = pd.DataFrame(data)

    # Define parameters
    check_in = '2024-06-17'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, city, df)

    # Assertions
    assert 'City' in result_df.columns
    assert 'Date' in result_df.columns
    assert 'AsOf' in result_df.columns
    assert 'Price/Review' in result_df.columns
    assert result_df['City'].iloc[0] == city
    assert result_df['Date'].iloc[0] == check_in
    assert (result_df['AsOf'].notna()).all()
    assert len(result_df) == 3  # Since one duplicate 'Hotel A' should be removed


def test_transform_data_in_df_dropna():
    # Create a sample DataFrame with None values
    data = {
        'Hotel': ['Hotel A', 'Hotel B', 'Hotel C', None],
        'Review': [4.5, None, 4.0, 3.5],
        'Price': [150, 200, None, 175]
    }
    df = pd.DataFrame(data)

    # Define parameters
    check_in = '2024-06-17'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, city, df)

    # Assertions
    assert len(result_df) == 1  # Only 'Hotel A'


def test_drop_rows_with_zero_price_or_review():
    # Given
    data = {
        'Hotel': ['Hotel A', 'Hotel B', 'Hotel C'],
        'Review': [4.0, 0, 5.0],
        'Price': [200, 0, 250]
    }
    df = pd.DataFrame(data)

    # When
    result_df = transform_data_in_df('2024-06-17', 'Tokyo', df)

    # Then
    assert len(result_df) == 2  # Only 'Hotel A' and 'Hotel C' should remain
    assert 'Hotel B' not in result_df['Hotel'].values  # 'Hotel B' with 0 price should be dropped


def test_transform_data_in_df_calculation():
    # Create a sample DataFrame
    data = {
        'Hotel': ['Hotel A', 'Hotel B'],
        'Review': [4.0, 5.0],
        'Price': [200, 250]
    }
    df = pd.DataFrame(data)

    # Define parameters
    check_in = '2024-06-17'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, city, df)

    # Assertions
    assert 'Price/Review' in result_df.columns
    assert result_df['Price/Review'].iloc[0] == 200 / 4.0
    assert result_df['Price/Review'].iloc[1] == 250 / 5.0


def test_transform_data_in_df_empty():
    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Hotel', 'Review', 'Price'])

    # Define parameters
    check_in = '2024-06-17'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, city, df)

    # Assertions
    assert result_df.empty


def test_extract_hotel_data_basic():
    # Sample hotel data
    hotel_data_list = [
        {
            "displayName": {"text": "Hotel A"},
            "basicPropertyData": {"reviewScore": {"score": 4.5}},
            "blocks": [{"finalPrice": {"amount": 150}}]
        },
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": {"reviewScore": {"score": 4.0}},
            "blocks": [{"finalPrice": {"amount": 200}}]
        }
    ]

    df_list = []

    # Call the function
    extract_hotel_data(df_list, hotel_data_list)

    # Assertions
    assert len(df_list) == 2
    df = pd.concat(df_list, ignore_index=True)
    assert df.shape == (2, 3)
    assert df['Hotel'].tolist() == ['Hotel A', 'Hotel B']
    assert df['Review'].tolist() == [4.5, 4.0]
    assert df['Price'].tolist() == [150, 200]


def test_extract_hotel_data_missing_values():
    # Sample hotel data with missing values
    hotel_data_list = [
        {
            "displayName": None,
            "basicPropertyData": {"reviewScore": {"score": 4.5}},
            "blocks": [{"finalPrice": {"amount": 150}}]
        },
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": None,
            "blocks": None
        }
    ]

    df_list = []

    # Call the function
    extract_hotel_data(df_list, hotel_data_list)

    # Assertions
    assert len(df_list) == 2
    df = pd.concat(df_list, ignore_index=True)
    assert df.shape == (2, 3)
    assert df['Hotel'].tolist() == [None, 'Hotel B']

    # Convert columns to numeric, coercing errors to NaN
    df['Review'] = pd.to_numeric(df['Review'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # Check for NaN values
    assert df['Review'][0] == 4.5
    assert np.isnan(df['Review'][1])
    assert df['Price'][0] == 150
    assert np.isnan(df['Price'][1])


def test_extract_hotel_data_empty_list():
    # Empty hotel data list
    hotel_data_list = []

    df_list = []

    # Call the function
    extract_hotel_data(df_list, hotel_data_list)

    # Assertions
    assert len(df_list) == 0
    assert df_list == []


def test_extract_hotel_data_multiple_appends():
    # Sample hotel data
    hotel_data_list_1 = [
        {
            "displayName": {"text": "Hotel A"},
            "basicPropertyData": {"reviewScore": {"score": 4.5}},
            "blocks": [{"finalPrice": {"amount": 150}}]
        }
    ]
    hotel_data_list_2 = [
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": {"reviewScore": {"score": 4.0}},
            "blocks": [{"finalPrice": {"amount": 200}}]
        }
    ]

    df_list = []

    # Call the function twice with different data
    extract_hotel_data(df_list, hotel_data_list_1)
    extract_hotel_data(df_list, hotel_data_list_2)

    # Assertions
    assert len(df_list) == 2
    df1 = df_list[0]
    df2 = df_list[1]

    assert df1.shape == (1, 3)
    assert df1['Hotel'].tolist() == ['Hotel A']
    assert df1['Review'].tolist() == [4.5]
    assert df1['Price'].tolist() == [150]

    assert df2.shape == (1, 3)
    assert df2['Hotel'].tolist() == ['Hotel B']
    assert df2['Review'].tolist() == [4.0]
    assert df2['Price'].tolist() == [200]


def test_returns_correct_total_page_number_and_data_mapping():
    # Given
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'data': {
            'searchQueries': {
                'search': {
                    'pagination': {'nbResultsTotal': 1},
                    'breadcrumbs': [{}, {}, {'name': 'Test City'}],
                    'flexibleDatesConfig': {
                        'dateRangeCalendar': {
                            'checkin': ['2023-01-01'],
                            'checkout': ['2023-01-02']
                        }
                    },
                    'searchMeta': {
                        'nbAdults': 2,
                        'nbChildren': 1,
                        'nbRooms': 1
                    },
                    'results': [{
                        'blocks': [{
                            'finalPrice': {'currency': 'USD'}
                        }]
                    }]
                }
            }
        }
    }
    entered_city = "Test City"
    entered_check_in = "2023-01-01"
    entered_check_out = "2023-01-02"
    entered_selected_currency = "USD"
    entered_num_adult = 2
    entered_num_children = 1
    entered_num_room = 1

    # When
    result = check_info(
        response_mock, entered_city, entered_check_in, entered_check_out,
        entered_selected_currency, entered_num_adult, entered_num_children,
        entered_num_room
    )

    # Then
    assert result == (1, {
        "city": "Test City",
        "check_in": "2023-01-01",
        "check_out": "2023-01-02",
        "num_adult": 2,
        "num_children": 1,
        "num_room": 1,
        "selected_currency": "USD"
    })


def test_handles_response_with_missing_or_null_fields_gracefully():
    # Given
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'data': {
            'searchQueries': {
                'search': {
                    'pagination': {'nbResultsTotal': 1},
                    'breadcrumbs': [{}, {}, {'name': None}],
                    'flexibleDatesConfig': {
                        'dateRangeCalendar': {
                            'checkin': [None],
                            'checkout': [None]
                        }
                    },
                    'searchMeta': {
                        'nbAdults': None,
                        'nbChildren': None,
                        'nbRooms': None
                    },
                    'results': [{
                        'blocks': [{
                            'finalPrice': {'currency': None}
                        }]
                    }]
                }
            }
        }
    }
    entered_city = "Test City"
    entered_check_in = "2023-01-01"
    entered_check_out = "2023-01-02"
    entered_selected_currency = "USD"
    entered_num_adult = 2
    entered_num_children = 1
    entered_num_room = 1

    # When
    error_message = ''
    try:
        check_info(
            response_mock, entered_city, entered_check_in, entered_check_out,
            entered_selected_currency, entered_num_adult, entered_num_children,
            entered_num_room
        )
    except SystemExit as e:
        error_message = str(e)

    # Then
    assert error_message == "Error City not match: Test City != None"


def test_concatenate_multiple_non_empty_dataframes():
    # Given
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    df_list = [df1, df2]

    # When
    result = concat_df_list(df_list)

    # Then
    assert not result.empty
    assert result.equals(pd.concat([df1, df2]))


def test_concatenate_empty_list():
    # Given
    df_list = []

    # When
    result = concat_df_list(df_list)

    # Then
    assert len(result) == 0


if __name__ == '__main__':
    pytest.main()
