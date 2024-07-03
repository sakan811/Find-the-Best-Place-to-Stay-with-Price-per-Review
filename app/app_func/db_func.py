from django.db import connection
from loguru import logger

from app.models import RoomPrice


def save_data_to_db(df) -> None:
    """
    Save the data into a database.
    :param df: DataFrame.
    :return: None.
    """
    logger.info("Saving data to database...")
    for index, row in df.iterrows():
        room_price = RoomPrice(
            hotel=row['Hotel'],
            room_price=row['Price'],
            review_score=row['Review'],
            price_per_review=row['Price/Review'],
            check_in=row['CheckIn'],
            check_out=row['CheckOut'],
            as_of_date=row['AsOf'],
            city=row['City']
        )
        room_price.save()


def truncate_db() -> None:
    """
    Truncate the database.
    :return: None.
    """
    logger.info("Truncating app_roomprice table...")
    RoomPrice.objects.all().delete()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence")


