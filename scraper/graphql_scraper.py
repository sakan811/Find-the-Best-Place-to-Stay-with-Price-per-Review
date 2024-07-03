import pandas as pd
import requests
from loguru import logger

from scraper.scraper_func.data_extractor import extract_hotel_data
from scraper.scraper_func.data_transformer import transform_data_in_df
from scraper.scraper_func.graphql_func import get_header, get_graphql_query, check_info
from scraper.scraper_func.utils import concat_df_list


def scrape_graphql(
        city: str = None,
        check_in: str = None,
        check_out: str = None,
        selected_currency: str = None,
        group_adults: int = 1,
        num_rooms: int = 1,
        group_children: int = 0,
        hotel_filter: bool = False) -> pd.DataFrame:
    """
    Scrape hotel data from GraphQL endpoint.
    :param city: City where the hotels are located.
    :param check_in: Check-in date.
    :param check_out: Check-out date.
    :param selected_currency: Currency of the room price.
    :param group_adults: Number of adults.
                        Default is 1.
    :param num_rooms: Number of rooms.
                    Default is 1.
    :param group_children: Number of children.
                        Default is 0.
    :param hotel_filter: If True, scrape only hotel properties, else scrape all properties.
                        Default is False.
    :return: Pandas DataFrame with hotel data.
    """
    logger.info("Start scraping data from GraphQL endpoint")
    logger.info(f"City: {city} | Check-in: {check_in} | Check-out: {check_out} | Currency: {selected_currency}")
    logger.info(f"Adults: {group_adults} | Children: {group_children} | Rooms: {num_rooms}")
    logger.info(f"Only hotel properties: {hotel_filter}")

    if check_in and check_out and selected_currency:
        # GraphQL endpoint URL
        url = f'https://www.booking.com/dml/graphql?selected_currency={selected_currency}'
        headers = get_header()
        graphql_query = get_graphql_query(city=city, check_in=check_in, check_out=check_out, group_adults=group_adults,
                                          group_children=group_children, num_rooms=num_rooms, hotel_filter=hotel_filter)

        response = requests.post(url, headers=headers, json=graphql_query)

        total_page_num, hotel_data_dict = check_info(
            response, city, check_in, check_out, selected_currency, group_adults, group_children, num_rooms
        )
        logger.debug(f"Total page number: {total_page_num}")
        logger.debug(f"City: {hotel_data_dict['city']}")
        logger.debug(f"Check-in date: {hotel_data_dict['check_in']}")
        logger.debug(f"Check-out date: {hotel_data_dict['check_out']}")
        logger.debug(f"Number of adults: {hotel_data_dict['num_adult']}")
        logger.debug(f"Number of children: {hotel_data_dict['num_children']}")
        logger.debug(f"Number of rooms: {hotel_data_dict['num_room']}")
        logger.debug(f"Currency: {hotel_data_dict['selected_currency']}")

        df_list = []
        logger.info("Scraping data from GraphQL endpoint...")
        for offset in range(0, total_page_num, 100):
            graphql_query = get_graphql_query(city=city, check_in=check_in, check_out=check_out,
                                              group_adults=group_adults,
                                              group_children=group_children, num_rooms=num_rooms,
                                              hotel_filter=hotel_filter,
                                              page_offset=offset)
            response = requests.post(url, headers=headers, json=graphql_query)

            if response.status_code == 200:
                data = response.json()
                hotel_data_list: list = data['data']['searchQueries']['search']['results']

                extract_hotel_data(df_list, hotel_data_list)
            else:
                logger.error(f"Error: {response.status_code}")

        df = concat_df_list(df_list)
        return transform_data_in_df(check_in, check_out, city, df)
    else:
        logger.warning("Error: check_in, check_out and selected_currency are required")
