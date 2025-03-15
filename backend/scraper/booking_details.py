from pydantic import BaseModel


class BookingDetails(BaseModel):
    """
    Pydantic model for Booking.com search details.

    Attributes:
        city (str): The city where the hotel is located.
        country (str): The country where the hotel is located.
        check_in (str): The check-in date for the hotel stay.
        check_out (str): The check-out date for the hotel stay.
        group_adults (int): The number of adults in the group.
        group_children (int): The number of children in the group.
        num_rooms (int): The number of rooms required.
        selected_currency (str): The currency for the booking.
        hotel_filter (bool): Whether to filter only hotel properties.
    """

    city: str
    country: str
    check_in: str
    check_out: str
    group_adults: int
    group_children: int
    num_rooms: int
    selected_currency: str
    hotel_filter: bool
