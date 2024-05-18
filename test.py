import pandas as pd
import pytest
from loguru import logger

from main import scrape, transform_data


def test_scrape_all_property():
    city = 'Osaka'
    check_in = '2024-05-20'
    check_out = '2024-05-21'
    group_adults = '1'
    num_rooms = '1'
    group_children = '0'
    selected_currency = 'GBP'
    hotel_filter = False

    hotel_filter_url = '&nflt=ht_id%3D204'

    # Create a DataFrame to store the data
    data = {'Hotel': [], 'Price': [], 'Review': []}

    url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
           f'={check_in}&checkout={check_out}&group_adults={group_adults}'
           f'&no_rooms={num_rooms}&group_children={group_children}'
           f'&selected_currency={selected_currency}')

    if hotel_filter:
        url += hotel_filter_url

    scrape(url, data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    df_filtered = transform_data(df)

    # Save the DataFrame to an Excel file
    excel_filename = f'{city}_hotel_{selected_currency}_sorted.xlsx'
    df_filtered.to_excel(excel_filename, index=False, header=True)
    logger.info(f'Data has been saved to {excel_filename}')

    assert not df_filtered.empty


def test_scrape_only_hotel_property():
    city = 'Osaka'
    check_in = '2024-05-20'
    check_out = '2024-05-21'
    group_adults = '1'
    num_rooms = '1'
    group_children = '0'
    selected_currency = 'GBP'
    hotel_filter = True

    hotel_filter_url = '&nflt=ht_id%3D204'

    # Create a DataFrame to store the data
    data = {'Hotel': [], 'Price': [], 'Review': []}

    url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
           f'={check_in}&checkout={check_out}&group_adults={group_adults}'
           f'&no_rooms={num_rooms}&group_children={group_children}'
           f'&selected_currency={selected_currency}')

    if hotel_filter:
        url += hotel_filter_url

    scrape(url, data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    df_filtered = transform_data(df)

    # Save the DataFrame to an Excel file
    excel_filename = f'{city}_hotel_{selected_currency}_sorted.xlsx'
    df_filtered.to_excel(excel_filename, index=False, header=True)
    logger.info(f'Data has been saved to {excel_filename}')

    assert not df_filtered.empty


if __name__ == '__main__':
    pytest.main()
