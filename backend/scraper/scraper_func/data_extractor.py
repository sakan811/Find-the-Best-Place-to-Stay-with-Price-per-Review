import pandas as pd

from logger.logging_config import main_logger


def get_accommodation_type_name(type_id: int) -> str:
    """
    Map accommodation type ID to its description.
    :param type_id: Accommodation type ID from Booking.com
    :return: String description of the accommodation type
    """
    accommodation_types = {
        219: "Entire homes & apartments",
        204: "Hotels",
        201: "Apartments",
        213: "Villas",
        216: "Guesthouses",
        203: "Hostels",
    }
    return accommodation_types.get(type_id, "Other")


def extract_hotel_data(df_list: list, hotel_data_list: list) -> None:
    """
    Extract data from a list of hotel data.
    :param df_list: A list to store Pandas Dataframes.
    :param hotel_data_list: List of results.
    :return:
    """
    main_logger.info("Extracting data...")

    for hotel_data in hotel_data_list:
        main_logger.debug("Initialize lists to store extracted data")
        display_names = []
        review_scores = []
        final_prices = []
        accommodation_names = []

        for key, val in hotel_data.items():
            if key == "displayName":
                if val:
                    display_names.append(val["text"])
                else:
                    display_names.append(None)

            if key == "basicPropertyData":
                if val:
                    review_scores.append(val["reviewScore"]["score"])
                    accom_type_id = val.get("accommodationTypeId")
                    accommodation_names.append(
                        get_accommodation_type_name(accom_type_id)
                    )
                else:
                    review_scores.append(None)
                    accommodation_names.append(None)

            if key == "blocks":
                if val:
                    final_prices.append(val[0]["finalPrice"]["amount"])
                else:
                    final_prices.append(None)

        main_logger.debug("Create a Pandas Dataframe to store extracted data")
        df = pd.DataFrame(
            {
                "Hotel": display_names,
                "Review": review_scores,
                "Price": final_prices,
                "AccommodationName": accommodation_names,
            }
        )

        main_logger.debug("Append dataframe to a df_list")
        df_list.append(df)
