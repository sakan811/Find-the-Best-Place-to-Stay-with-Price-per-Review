import pandas as pd

from scraper.scraper_func.data_extractor import extract_hotel_data


def test_extract_hotel_data_multiple_appends():
    # Sample hotel data
    hotel_data_list_1 = [
        {
            "displayName": {"text": "Hotel A"},
            "basicPropertyData": {
                "reviewScore": {"score": 4.5},
                "accommodationTypeId": 204
            },
            "blocks": [{"finalPrice": {"amount": 150}}]
        }
    ]
    hotel_data_list_2 = [
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": {
                "reviewScore": {"score": 4.0},
                "accommodationTypeId": 204
            },
            "blocks": [{"finalPrice": {"amount": 200}}]
        }
    ]

    # Create df_lists for each data set
    df_list_1 = []
    df_list_2 = []

    # Call the function with each data set
    extract_hotel_data(df_list_1, hotel_data_list_1)
    extract_hotel_data(df_list_2, hotel_data_list_2)

    # Assertions
    assert len(df_list_1) == 1
    assert len(df_list_2) == 1
    
    df1 = pd.concat(df_list_1, ignore_index=True)
    df2 = pd.concat(df_list_2, ignore_index=True)

    assert df1.shape == (1, 4)  # 4 columns: Hotel, Review, Price, AccommodationName
    assert df1['Hotel'].tolist() == ['Hotel A']
    assert df1['Review'].tolist() == [4.5]
    assert df1['Price'].tolist() == [150]
    assert df1['AccommodationName'].tolist() == ['Hotels']

    assert df2.shape == (1, 4)
    assert df2['Hotel'].tolist() == ['Hotel B']
    assert df2['Review'].tolist() == [4.0]
    assert df2['Price'].tolist() == [200]
    assert df2['AccommodationName'].tolist() == ['Hotels']


def test_extract_hotel_data_missing_values():
    # Sample hotel data with missing values
    hotel_data_list = [
        {
            "displayName": None,
            "basicPropertyData": {
                "reviewScore": {"score": 4.5},
                "accommodationTypeId": 204
            },
            "blocks": [{"finalPrice": {"amount": 150}}]
        },
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": None,
            "blocks": None
        }
    ]

    # Create df_list
    df_list = []

    # Call the function
    extract_hotel_data(df_list, hotel_data_list)

    # Assertions
    assert len(df_list) == 2
    
    # Define expected dtypes before concatenation
    dtypes = {
        'Hotel': 'object',
        'Review': 'float64',
        'Price': 'float64',
        'AccommodationName': 'object'
    }
    
    # Convert each DataFrame in df_list to have consistent dtypes
    df_list = [df.astype(dtypes) for df in df_list]
    
    # Now concatenate with consistent dtypes
    df = pd.concat(df_list, ignore_index=True)
    
    assert df.shape == (2, 4)  # 4 columns: Hotel, Review, Price, AccommodationName
    assert df['Hotel'].tolist() == [None, 'Hotel B']
    assert df['AccommodationName'].tolist() == ['Hotels', None]

    # Values should already be numeric due to dtype conversion
    assert df['Review'].iloc[0] == 4.5
    assert pd.isna(df['Review'].iloc[1])  # None value
    assert df['Price'].iloc[0] == 150
    assert pd.isna(df['Price'].iloc[1])  # None value


def test_extract_hotel_data_empty_list():
    # Empty hotel data list
    hotel_data_list = []
    df_list = []
    
    # Call the function
    extract_hotel_data(df_list, hotel_data_list)
    
    # Assertions
    assert len(df_list) == 0
    
    # If we concatenate empty list, should get empty DataFrame
    if df_list:
        df = pd.concat(df_list, ignore_index=True)
        assert df.empty


def test_extract_hotel_data_basic():
    # Sample hotel data
    hotel_data_list = [
        {
            "displayName": {"text": "Hotel A"},
            "basicPropertyData": {
                "reviewScore": {"score": 4.5},
                "accommodationTypeId": 204
            },
            "blocks": [{"finalPrice": {"amount": 150}}]
        },
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": {
                "reviewScore": {"score": 4.0},
                "accommodationTypeId": 201
            },
            "blocks": [{"finalPrice": {"amount": 200}}]
        }
    ]

    df_list = []

    # Call the function
    extract_hotel_data(df_list, hotel_data_list)

    # Assertions
    assert len(df_list) == 2
    df = pd.concat(df_list, ignore_index=True)
    assert df.shape == (2, 4)  # Now 4 columns without AccommodationType
    assert df['Hotel'].tolist() == ['Hotel A', 'Hotel B']
    assert df['Review'].tolist() == [4.5, 4.0]
    assert df['Price'].tolist() == [150, 200]
    assert df['AccommodationName'].tolist() == ['Hotels', 'Apartments']


def test_accommodation_type_mapping():
    # Sample hotel data with different accommodation types
    hotel_data_list = [
        {
            "displayName": {"text": "Apartment A"},
            "basicPropertyData": {
                "reviewScore": {"score": 4.5},
                "accommodationTypeId": 219  # Entire homes & apartments
            },
            "blocks": [{"finalPrice": {"amount": 150}}]
        },
        {
            "displayName": {"text": "Hotel B"},
            "basicPropertyData": {
                "reviewScore": {"score": 4.0},
                "accommodationTypeId": 204  # Hotels
            },
            "blocks": [{"finalPrice": {"amount": 200}}]
        }
    ]

    # Create df_list
    df_list = []

    # Call the function
    extract_hotel_data(df_list, hotel_data_list)

    # Assertions
    assert len(df_list) == 2
    df = pd.concat(df_list, ignore_index=True)
    
    assert df.shape == (2, 4)  # 4 columns: Hotel, Review, Price, AccommodationName
    assert df['Hotel'].tolist() == ['Apartment A', 'Hotel B']
    assert df['AccommodationName'].tolist() == ['Entire homes & apartments', 'Hotels']
    assert df['Review'].tolist() == [4.5, 4.0]
    assert df['Price'].tolist() == [150, 200]
