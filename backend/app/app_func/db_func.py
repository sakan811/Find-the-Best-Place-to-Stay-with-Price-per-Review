import datetime

from django.db import connection

from app.models import BookingDetails, RoomPrice
from logging_config import main_logger


def save_data_to_db(df) -> None:
    """
    Save the data into a database.
    :param df: DataFrame.
    :return: None.
    """
    main_logger.info("Saving data to database...")
    for index, row in df.iterrows():
        room_price = RoomPrice(
            hotel=row['Hotel'],
            room_price=row['Price'],
            review_score=row['Review'],
            price_per_review=row['Price/Review'],
            check_in=row['CheckIn'],
            check_out=row['CheckOut'],
            as_of_date=row['AsOf'],
            city=row['City'],
            accommodation_name=row['AccommodationName']
        )
        room_price.save()


def save_booking_details_to_db(
        check_in: str,
        check_out: str,
        city: str,
        num_adults: int,
        num_children: int,
        num_rooms: int,
        currency: str,
        only_hotel: bool) -> None:
    """
    Save the booking details into a database.
    :param check_in: Check-In date.
    :param check_out: Check-Out date.
    :param city: City where the hotels are located.
    :param num_adults: Number of adults.
    :param num_children: Number of children.
    :param num_rooms: Number of rooms.
    :param currency: Currency.
    :param only_hotel: Whether the scraped data consists of hotel properties.
    :return: None.
    """
    main_logger.info("Saving booking details to database...")
    # Convert string dates to date objects
    check_in_date = datetime.datetime.strptime(check_in, "%Y-%m-%d").date()
    check_out_date = datetime.datetime.strptime(check_out, "%Y-%m-%d").date()

    # Create and save the booking detail
    booking_detail = BookingDetails(
        check_in=check_in_date,
        check_out=check_out_date,
        city=city,
        num_adults=num_adults,
        num_children=num_children,
        num_rooms=num_rooms,
        currency=currency,
        only_hotel=only_hotel
    )
    booking_detail.save()


def truncate_roomprice_table() -> None:
    """
    Truncate the app_roomprice table.
    :return: None.
    """
    main_logger.info("Truncating app_roomprice table...")
    RoomPrice.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence")


def truncate_booking_details_table() -> None:
    """
    Truncate the app_bookingdetails table.
    :return: None.
    """
    main_logger.info("Truncating app_bookingdetails table...")
    BookingDetails.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence")

