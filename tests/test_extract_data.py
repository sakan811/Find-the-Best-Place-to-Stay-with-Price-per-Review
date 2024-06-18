import numpy as np
import pandas as pd

from main import extract_hotel_data


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
