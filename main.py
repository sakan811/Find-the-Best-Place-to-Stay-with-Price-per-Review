import re

import bs4
import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, NoSuchWindowException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger.add('find_best_place_to_stay.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def click_pop_up_ad(wait: WebDriverWait, driver: WebDriver) -> None:
    """
    Click pop-up ad.
    :param driver: Selenium WebDriver.
    :param wait: Selenium WebDriverWait object.
    :return: None
    """
    logger.info("Clicking pop-up ad...")

    ads_css_selector = 'div.e93d17c51f:nth-child(1) > button:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
    try:
        ads = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ads_css_selector)))
        ads.click()
    except NoSuchElementException as e:
        logger.error(e)
        logger.error(f'Pop-up ad not found')
    except TimeoutException as e:
        logger.error(e)
        logger.error(f'Pop-up ad timed out')
        logger.error(f'Moving on')
    except Exception as e:
        logger.error(e)
        logger.error(f'Unexpected error occurred')
    else:
        logger.info('Clicked the pop-up ads successfully')


def click_load_more_result_button(wait: WebDriverWait, driver: WebDriver) -> None:
    """
    Click 'load more result' button to load more hotels.
    :param wait: Selenium WebDriverWait object.
    :param driver: Selenium WebDriver.
    :return: None
    """
    logger.info("Click 'load more result' button.")

    load_more_result_css_selector_list = [
        '#bodyconstraint-inner > div:nth-child(8) > div > div.c1cce822c4 > '
        'div.b3869ababc > div.b2c588d242 > div.c1b783d372.b99ea5ed8e > '
        'div.fb4e9b097f > div.fa298e29e2.a1b24d26fa > button > span',
        '#bodyconstraint-inner > div:nth-child(8) > div > div.c1cce822c4 > div.b3869ababc > div.b2c588d242 > '
        'div.c1b783d372.b99ea5ed8e > div.fb4e9b097f > div.fa298e29e2.a1b24d26fa',
        '#bodyconstraint-inner > div:nth-child(8) > div > div.c1cce822c4 > div.b3869ababc > div.b2c588d242 > '
        'div.c1b783d372.b99ea5ed8e > div.fb4e9b097f > div.fa298e29e2.a1b24d26fa > button',
        '#bodyconstraint-inner > div:nth-child(8) > div > div.c1cce822c4 > div.b3869ababc > div.b2c588d242 > '
        'div.c1b783d372.b99ea5ed8e > div.fb4e9b097f > div.fa298e29e2.a1b24d26fa > button > span'
    ]

    for load_more_result_css_selector in load_more_result_css_selector_list:
        try:
            load_more_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, load_more_result_css_selector)))
            load_more_button.click()
        except NoSuchElementException as e:
            logger.error(e)
            logger.error(f'The \'load more result\' button not found. Keep scrolling.')
        except TimeoutException as e:
            logger.error(e)
            logger.error(f'The \'load more result\' button timed out.')
        except Exception as e:
            logger.error(e)
            logger.error(f'Unexpected error occurred')
        else:
            logger.info('Clicked the \'load more result\' button successfully')
            return


def scroll_down_until_page_bottom(wait: WebDriverWait, driver: WebDriver) -> None:
    """
    Scroll down and click 'Load more result' button if present.

    Scroll down until reach the bottom of the page.
    :param wait: Selenium WebDriverWait object.
    :param driver: Selenium WebDriver.
    :return: None.
    """
    logger.info("Scrolling down until the bottom of the page...")
    current_height = 0
    new_height = 0

    while True:
        try:
            # Get current height
            current_height = driver.execute_script("return window.scrollY")
            logger.debug(f'{current_height = }')

            # Scroll down to the bottom
            driver.execute_script("window.scrollBy(0, 2000);")

            # Get current height
            new_height = driver.execute_script("return window.scrollY")
            logger.debug(f'{new_height = }')
        except NoSuchWindowException as e:
            logger.error(e)
            logger.error('No such window: The browsing context has been discarded.')

        if new_height == 0:
            logger.error('Failed to scroll down, refreshing the page...')
            driver.refresh()
        else:
            # If the new height is the same as the last height, then the bottom is reached
            if current_height == new_height:
                logger.info("Reached the bottom of the page.")
                break

        # Click 'load more result' button if present
        click_load_more_result_button(wait, driver)

        logger.info("Clicking pop-up ad in case it appears...")
        click_pop_up_ad(wait, driver)


def scrape_data_from_box_class(
        soup: bs4.BeautifulSoup,
        box_class: str,
        hotel_class: str,
        price_class: str,
        review_class: str,
        data: pd.DataFrame) -> None:
    """
    Scrape data from box class.
    :param soup: bs4.BeautifulSoup object.
    :param box_class: Class name of the box that contains the hotel data.
    :param hotel_class: Class name of the hotel name data.
    :param price_class: Class name of the price data.
    :param review_class: Class name of the review score data.
    :param data: Pandas dataframe.
    :return: None
    """
    logger.info("Scraping data from box class...")

    # Find the box elements
    box_elements = soup.select(f'.{box_class}')

    for box_element in box_elements:
        # Find the elements within the box element
        hotel_element = box_element.select(f'.{hotel_class}')
        price_element = box_element.select(f'.{price_class}')
        review_element = box_element.select(f'.{review_class}')

        # Check if all elements are presented before extracting data
        if hotel_element and price_element and review_element:
            hotel_name = hotel_element[0].text
            price = re.sub(r'[^0-9]', '', price_element[0].text)
            review_score = review_element[0].text.split()[1]

            data['Hotel'].append(hotel_name)
            data['Price'].append(price)
            data['Review'].append(review_score)

            logger.info(f'All elements are presented.')
            logger.debug(f'Hotel: {hotel_element}')
            logger.debug(f'Price: {price_element}')
            logger.debug(f'Review Score: {review_element}')
        else:
            logger.warning(f'Not all elements are presented.')
            logger.debug(f'Hotel: {hotel_element}')
            logger.debug(f'Price: {price_element}')
            logger.debug(f'Review Score: {review_element}')


def connect_to_webdriver() -> WebDriver:
    """
    Connect to the Selenium WebDriver.
    :return: Selenium WebDriver
    """
    # Configure driver options
    options = webdriver.FirefoxOptions()
    # Block image loading
    options.set_preference('permissions.default.stylesheet', 2)
    options.set_preference('permissions.default.image', 2)
    options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    options.add_argument("--headless")
    # Disable blink features related to automation control
    options.add_argument('--disable-blink-features=AutomationControlled')
    # Initialize the driver with the configured options
    driver = webdriver.Firefox(options=options)
    return driver


def scrape(url, data) -> None:
    """
    Scrape hotel data from the website.
    :param url: Website URL.
    :param data: Empty Pandas DataFrame.
    :return: None
    """
    driver = connect_to_webdriver()
    driver.get(url)

    wait = WebDriverWait(driver, timeout=0.01)

    html = None
    try:
        click_pop_up_ad(wait, driver)

        scroll_down_until_page_bottom(wait, driver)

        logger.info('Get the page source after the page has loaded')
        html = driver.page_source
    except Exception as e:
        logger.error(e)
        logger.error(f'Unexpected error occurred')
    finally:
        logger.info('Close the webdriver after obtaining the HTML content')
        driver.quit()

    if html:
        logger.info('Parse the HTML content with BeautifulSoup')
        soup = BeautifulSoup(html, 'html.parser')

        hotel_class = 'fa4a3a8221.b121bc708f'
        price_class = 'fa4a3a8221.b22052b420.f53c51ec80'
        review_class = 'f13857cc8c.e008572b71'
        box_class = 'fa298e29e2.b74446e476.e40c0c68b1.ea1d0cfcb7.d8991ab7ae.e8b7755ec7.ad0e783e41'

        scrape_data_from_box_class(soup, box_class, hotel_class, price_class, review_class, data)


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform scraped hotel data.
    :param df: Pandas dataframe.
    :return: Pandas dataframe.
    """
    logger.info("Transforming data...")

    # Remove duplicate rows from the DataFrame based on 'Hotel' column
    df_filtered = df.drop_duplicates(subset='Hotel')

    # Convert 'Price' and 'Review' columns to numeric using .loc
    df_filtered['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df_filtered['Review'] = pd.to_numeric(df['Review'], errors='coerce')

    # Add a new column for the ratio of Price to Review
    df_filtered['Price/Review'] = df_filtered['Price'] / df_filtered['Review']

    # Sort the DataFrame based on the 'Price/Review' column
    return df_filtered.sort_values(by='Price/Review')


def main(city: str,
         check_in: str,
         check_out: str,
         group_adults: str,
         num_rooms: str,
         group_children: str,
         selected_currency: str,
         hotel_filter: bool) -> None:
    """
    Main function to start the web scraping process.
    :param city: City name.
    :param check_in: Check-in date.
    :param check_out: Check-out date.
    :param group_adults: Number of adults.
    :param num_rooms: Number of rooms.
    :param group_children: Number of children.
    :param selected_currency: Currency name.
    :param hotel_filter: Scrape only hotel property data if True.
    :return: None
    """
    logger.info("Starting web-scraping...")

    hotel_filter_url = '&nflt=ht_id%3D204'

    # Create a DataFrame to store the data
    data = {'Hotel': [], 'Price': [], 'Review': []}

    url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
           f'={check_in}&checkout={check_out}&group_adults={group_adults}'
           f'&no_rooms={num_rooms}&group_children={group_children}'
           f'&selected_currency={selected_currency}')

    if hotel_filter:
        url += hotel_filter_url

    scrape(url, data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    df_filtered = transform_data(df)

    # Save the DataFrame to an Excel file
    excel_filename = f'{city}_hotel_{selected_currency}_sorted.xlsx'
    df_filtered.to_excel(excel_filename, index=False, header=True)
    logger.info(f'Data has been saved to {excel_filename}')


if __name__ == '__main__':
    city = 'Osaka'
    check_in = '2024-08-16'
    check_out = '2024-08-17'
    group_adults = '1'
    num_rooms = '1'
    group_children = '0'
    selected_currency = 'GBP'
    hotel_filter = True

    main(city, check_in, check_out, group_adults, num_rooms, group_children, selected_currency, hotel_filter)
