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
    headers = {
        "User-Agent": os.getenv("USER_AGENT"),
        "x-booking-context-action-name": os.getenv("X_BOOKING_CONTEXT_ACTION_NAME"),
        "x-booking-context-aid": os.getenv("X_BOOKING_CONTEXT_AID"),
        "x-booking-csrf-token": os.getenv("X_BOOKING_CSRF_TOKEN"),
        "x-booking-et-serialized-state": os.getenv("X_BOOKING_ET_SERIALIZED_STATE"),
        "x-booking-pageview-id": os.getenv("X_BOOKING_PAGEVIEW_ID"),
        "x-booking-site-type-id": os.getenv("X_BOOKING_SITE_TYPE_ID"),
        "x-booking-topic": os.getenv("X_BOOKING_TOPIC"),
    }
    return headers


def check_currency_data(data) -> str:
    """
    Check currency data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :return: City name.
    """
    main_logger.info("Checking currency data from the GraphQL response...")
    selected_currency_data = None
    try:
        for result in data["data"]["searchQueries"]["search"]["results"]:
            if "blocks" in result:
                for block in result["blocks"]:
                    if "finalPrice" in block:
                        selected_currency_data = block["finalPrice"]["currency"]
                        break
    except KeyError:
        main_logger.error("KeyError: Currency data not found")
    except IndexError:
        main_logger.error("IndexError: Currency data not found")
    return selected_currency_data


def check_city_data(data: dict, entered_city: str) -> str:
    """
    Check city data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :param entered_city: City name entered by the user.
    :return: City name.
    """
    main_logger.info("Checking city data from the GraphQL response...")
    city_data = "Not Match"

    try:
        # Loop through each breadcrumb in the GraphQL response
        for breadcrumb in data["data"]["searchQueries"]["search"]["breadcrumbs"]:
            main_logger.debug(f"Breadcrumb data: {breadcrumb}")

            if breadcrumb.get("name") is None:
                continue

            # Compare the 'name' field specifically with the entered city
            if breadcrumb.get("name", "").lower() == entered_city.lower():
                city_data = breadcrumb[
                    "name"
                ]  # Return the city name if a match is found
                return city_data

        # In case no match is found for the entered city
        if city_data == "Not Match":
            main_logger.warning(
                f"City '{entered_city}' not found in GraphQL breadcrumbs."
            )
    except KeyError:
        main_logger.error("KeyError: Issue while parsing city data")
        raise KeyError
    except IndexError:
        main_logger.error("IndexError: Issue while parsing city data")
        raise IndexError

    return city_data  # Returns None if no match is found


def check_country_data(data: dict, entered_country: str) -> str:
    """
    Check country data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :param entered_country: Country name entered by the user.
    :return: Country name.
    """
    main_logger.info("Checking country data from the GraphQL response...")
    country_data = "Not Match"

    try:
        # Loop through each breadcrumb in the GraphQL response
        for breadcrumb in data["data"]["searchQueries"]["search"]["breadcrumbs"]:
            main_logger.debug(f"Breadcrumb data: {breadcrumb}")

            if breadcrumb.get("name") is None:
                continue

            # Compare the 'name' field specifically with the entered country
            if breadcrumb.get("name", "").lower() == entered_country.lower():
                country_data = breadcrumb[
                    "name"
                ]  # Return the country name if a match is found
                return country_data

        # In case no match is found for the entered city
        if country_data == "Not Match":
            main_logger.warning("Country name not found in GraphQL breadcrumbs.")
    except KeyError:
        main_logger.error("KeyError: Issue while parsing country data")
        raise KeyError
    except IndexError:
        main_logger.error("IndexError: Issue while parsing country data")
        raise IndexError

    return country_data  # Returns None if no match is found


def check_hotel_filter_data(data) -> bool:
    """
    Check hotel filter data from the GraphQL response.
    :param data: GraphQL response as JSON.
    :return: Hotel filter indicator.
    """
    main_logger.info("Checking hotel filter data from the GraphQL response...")

    try:
        for option in data["data"]["searchQueries"]["search"]["appliedFilterOptions"]:
            main_logger.debug(f"Filter options: {option}")
            if "urlId" in option:
                if option["urlId"] == "ht_id=204":
                    return True
    except KeyError:
        main_logger.error("KeyError: hotel_filter not found")
        return False
    except IndexError:
        main_logger.error("IndexError: hotel_filter not found")
        return False

    return False
