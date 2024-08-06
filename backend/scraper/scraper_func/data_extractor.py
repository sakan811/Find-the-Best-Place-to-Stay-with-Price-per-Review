import pandas as pd

from logging_config import main_logger


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
        for key, val in hotel_data.items():
            if key == "displayName":
                if val:
                    display_names.append(val['text'])
                else:
                    display_names.append(None)

            if key == "basicPropertyData":
                if val:
                    review_scores.append(val['reviewScore']['score'])
                else:
                    review_scores.append(None)

            if key == "blocks":
                if val:
                    final_prices.append(val[0]['finalPrice']['amount'])
                else:
                    final_prices.append(None)

        main_logger.debug("Create a Pandas Dataframe to store extracted data")
        df = pd.DataFrame({
            "Hotel": display_names,
            "Review": review_scores,
            "Price": final_prices
        })

        main_logger.debug("Append dataframe to a df_list")
        df_list.append(df)
