import pandas as pd

from scraper.scraper_func.data_transformer import transform_data_in_df


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
    check_out = '2024-06-18'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, check_out, city, df)

    # Assertions
    assert 'City' in result_df.columns
    assert 'CheckIn' in result_df.columns
    assert 'CheckOut' in result_df.columns
    assert 'AsOf' in result_df.columns
    assert 'Price/Review' in result_df.columns
    assert result_df['City'].iloc[0] == city
    assert result_df['CheckIn'].iloc[0] == check_in
    assert result_df['CheckOut'].iloc[0] == check_out
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
    check_out = '2024-06-18'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, check_out, city, df)

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

    # Define parameters
    check_in = '2024-06-17'
    check_out = '2024-06-18'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, check_out, city, df)

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
    check_out = '2024-06-18'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, check_out, city, df)
    # Assertions
    assert 'Price/Review' in result_df.columns
    assert result_df['Price/Review'].iloc[0] == 200 / 4.0
    assert result_df['Price/Review'].iloc[1] == 250 / 5.0


def test_transform_data_in_df_empty():
    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Hotel', 'Review', 'Price'])

    # Define parameters
    check_in = '2024-06-17'
    check_out = '2024-06-18'
    city = 'Tokyo'

    # Transform data
    result_df = transform_data_in_df(check_in, check_out, city, df)

    # Assertions
    assert result_df.empty
