from loguru import logger


def get_form_data(cleaned_data: dict) -> tuple:
    """
    Get data from Django form.
    :param cleaned_data: Cleaned form data.
    :return: Tuple of form data.
    """
    logger.info(f'Getting form data...')
    city = cleaned_data.get('city')
    check_in = cleaned_data.get('check_in')
    check_out = cleaned_data.get('check_out')
    group_adults = cleaned_data.get('group_adults')
    num_rooms = cleaned_data.get('num_rooms')
    group_children = cleaned_data.get('group_children')
    selected_currency = cleaned_data.get('selected_currency')
    hotel_filter = cleaned_data.get('hotel_filter')
    return check_in, check_out, city, group_adults, group_children, hotel_filter, num_rooms, selected_currency
