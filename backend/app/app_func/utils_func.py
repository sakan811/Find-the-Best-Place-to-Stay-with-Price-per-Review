from datetime import date
from typing import Any

from logger.logging_config import main_logger


def get_form_data(form_data: dict[str, str | int | bool]) -> tuple[Any, ...]:
    """
    Get data from Django form.
    :param form_data: Form data.
    :return: Tuple of form data:
            check_in, check_out, city, country, group_adults, group_children, hotel_filter, num_rooms, selected_currency
    """
    main_logger.info("Getting form data...")

    city = form_data.get("city")
    country = form_data.get("country")
    check_in = form_data.get("check_in")
    check_out = form_data.get("check_out")
    group_adults = form_data.get("group_adults")
    num_rooms = form_data.get("num_rooms")
    group_children = form_data.get("group_children")
    selected_currency = form_data.get("selected_currency")
    hotel_filter = form_data.get("hotel_filter")

    # Capitalize first letter of each word
    if isinstance(city, str) and len(city) > 0:
        city = city.title()
    if isinstance(country, str) and len(country) > 0:
        country = country.title()

    if isinstance(check_in, date):
        check_in = check_in.strftime("%Y-%m-%d")
    if isinstance(check_out, date):
        check_out = check_out.strftime("%Y-%m-%d")

    if not isinstance(group_adults, int):
        try:
            group_adults = int(group_adults) if group_adults is not None else 1
        except (ValueError, TypeError):
            main_logger.warning("group_adults is not an integer. set it to 1")
            group_adults = 1

    if not isinstance(group_children, int):
        try:
            group_children = int(group_children) if group_children is not None else 0
        except (ValueError, TypeError):
            main_logger.warning("group_children is not an integer. set it to 0")
            group_children = 0

    if not isinstance(num_rooms, int):
        try:
            num_rooms = int(num_rooms) if num_rooms is not None else 1
        except (ValueError, TypeError):
            main_logger.warning("num_rooms is not an integer. set it to 1")
            num_rooms = 1

    return (
        check_in,
        check_out,
        city,
        country,
        group_adults,
        group_children,
        hotel_filter,
        num_rooms,
        selected_currency,
    )
