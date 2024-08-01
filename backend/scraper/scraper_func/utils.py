import os

import pandas as pd


from logging_config import configure_logging_with_file, main_logger

script_logger = configure_logging_with_file(log_dir='logs', log_file='utils.log', logger_name='utils')


def concat_df_list(df_list: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Concatenate a list of Pandas Dataframes.
    :param df_list: A list of Pandas Dataframes.
    :return: Pandas DataFrame.
    """
    main_logger.info("Concatenate a list of Pandas Dataframes")
    if df_list:
        df_main = pd.concat(df_list)
        return df_main
    else:
        main_logger.warning("No data was scraped.")
        return pd.DataFrame()


def save_scraped_data(
        dataframe: pd.DataFrame,
        city: dict = None,
        check_in: dict = None,
        check_out: dict = None,
        save_dir='../scraped_hotel_data') -> str:
    """
    Save scraped data to CSV files in the given directory.
    The CSV files directory is created automatically if it doesn't exist.
    The default CSV files directory name is depended on the default value of 'save_dir' parameter.
    :param dataframe: Pandas DataFrame.
    :param city: City where the hotels are located.
    :param check_in: Check-in date.
    :param check_out: Check-out date.
    :param save_dir: Directory to save the scraped data as CSV.
                    Default is 'scraped_hotel_data_csv' folder.
    :return: Excel file path
    """
    main_logger.info("Saving scraped data...")
    if not dataframe.empty:
        main_logger.info('Save data to Excel')
        try:
            # Attempt to create the directory
            os.makedirs(save_dir)
            main_logger.info(f'Created {save_dir} directory')
        except FileExistsError:
            # If the directory already exists, log a message and continue
            main_logger.error(f'FileExistsError: {save_dir} directory already exists')

        if city and check_in and check_out:
            city = city['city']
            check_in = check_in['check_in'].strftime('%Y-%m-%d')
            check_out = check_out['check_out'].strftime('%Y-%m-%d')
            return f'{city}_hotel_data_{check_in}_to_{check_out}.xlsx'
        else:
            main_logger.warning("Cannot save data to Excel. "
                           "please enter city, check-in or check-out date. ")
    else:
        main_logger.warning('The dataframe is empty. No data to save')


