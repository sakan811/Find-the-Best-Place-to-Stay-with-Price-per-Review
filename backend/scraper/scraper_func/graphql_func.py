from logging_config import configure_logging_with_file, main_logger

script_logger = configure_logging_with_file(log_dir='logs', log_file='graphql_func.log', logger_name='graphql_func')


def get_header() -> dict:
    """
    Return header.
    :return: Header as a dictionary.
    """
    main_logger.info("Getting header...")
    return {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
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


def check_city_data(data) -> str:
    """
    Check city data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :return: City name.
    """
    main_logger.info("Checking city data from the GraphQL response...")
    city_data = None
    try:
        for breadcrumb in data['data']['searchQueries']['search']['breadcrumbs']:
            if 'destType' in breadcrumb:
                if breadcrumb['destType'] == 'CITY':
                    city_data = breadcrumb['name']
                    break
    except KeyError:
        main_logger.error('KeyError: City not found')
    except IndexError:
        main_logger.error('IndexError: City not found')
    return city_data


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