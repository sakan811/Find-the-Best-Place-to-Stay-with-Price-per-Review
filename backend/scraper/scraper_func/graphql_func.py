import os

from dotenv import load_dotenv

from logging_config import main_logger

load_dotenv()


def get_header() -> dict:
    """
    Return header.
    :return: Header as a dictionary.
    """
    main_logger.info("Getting header...")
    return {
        "User-Agent": os.getenv("USER_AGENT")
    }


def check_currency_data(data) -> str:
    """
    Check currency data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :return: City name.
    """
    main_logger.info("Checking currency data from the GraphQL response...")
    selected_currency_data = None
    try:
        for result in data['data']['searchQueries']['search']['results']:
            if 'blocks' in result:
                for block in result['blocks']:
                    if 'finalPrice' in block:
                        selected_currency_data = block['finalPrice']['currency']
                        break
    except KeyError:
        main_logger.error('KeyError: Currency data not found')
    except IndexError:
        main_logger.error('IndexError: Currency data not found')
    return selected_currency_data


def check_city_data(data: dict, entered_city: str) -> str:
    """
    Check city data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :param entered_city: City name entered by the user.
    :return: City name.
    """
    main_logger.info("Checking city data from the GraphQL response...")
    city_data = ''

    try:
        # Loop through each breadcrumb in the GraphQL response
        for breadcrumb in data['data']['searchQueries']['search']['breadcrumbs']:
            # Search each key-value pair in the breadcrumb dictionary
            for key, value in breadcrumb.items():
                # Check if the value matches the entered city
                if str(value).lower() == entered_city.lower():
                    city_data = breadcrumb.get('name', value)  # Return city name or the matched value
                    return city_data

        # In case no match is found for the entered city
        if city_data is None:
            main_logger.warning(f"City '{entered_city}' not found in GraphQL breadcrumbs.")
    except KeyError:
        main_logger.error('KeyError: Issue while parsing city data')
        raise KeyError
    except IndexError:
        main_logger.error('IndexError: Issue while parsing city data')
        raise IndexError

    return city_data  # Returns None if no match is found


def check_hotel_filter_data(data) -> bool:
    """
    Check hotel filter data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :return: Hotel filter indicator.
    """
    main_logger.info("Checking hotel filter data from the GraphQL response...")

    try:
        for option in data['data']['searchQueries']['search']['appliedFilterOptions']:
            main_logger.debug(f'Filter options: {option}')
            if 'urlId' in option:
                if option['urlId'] == "ht_id=204":
                    return True
    except KeyError:
        main_logger.error('KeyError: hotel_filter not found')
        return False
    except IndexError:
        main_logger.error('IndexError: hotel_filter not found')
        return False

    return False
