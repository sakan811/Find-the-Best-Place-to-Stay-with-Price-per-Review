import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, StaleElementReferenceException
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

    ads_css_selector = ('#b2searchresultsPage > div.b9720ed41e.cdf0a9297c > div > div > div > div.dd5dccd82f > '
                        'div.ffd93a9ecb.dc19f70f85.eb67815534 > div > button')
    try:
        time.sleep(2)
        ads = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ads_css_selector)))
        ads.click()
    except NoSuchElementException as e:
        logger.error(e)
        logger.error(f'{ads_css_selector} not found')
    except TimeoutException as e:
        logger.error(e)
        logger.error(f'{ads_css_selector} timed out')
        driver.refresh()
        logger.info('Refreshed page')
    except Exception as e:
        logger.error(e)
        logger.error(f'{ads_css_selector} failed due to {e}')
    else:
        logger.info('Clicked the pop-up ads successfully')


def click_load_more_result_button(driver: WebDriver) -> None:
    """
    Click 'load more result' button to load more hotels.
    :param driver: Selenium WebDriver.
    :return: None
    """
    logger.info("Clicking 'load more result' button...")

    load_more_result_css_selector = ('#bodyconstraint-inner > div:nth-child(8) > div > div.af5895d4b2 > '
                                     'div.df7e6ba27d > div.bcbf33c5c3 > div.dcf496a7b9.bb2746aad9 > '
                                     'div.d4924c9e74 > div.c82435a4b8.f581fde0b8 > button')

    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR, load_more_result_css_selector)
        load_more_button.click()
    except NoSuchElementException as e:
        logger.error(e)
        logger.error(f'{load_more_result_css_selector} not found. Keep scrolling.')
    except StaleElementReferenceException as e:
        logger.error(e)
        logger.error(f'{load_more_result_css_selector} is no longer valid '
                     f'because it has been modified or removed from the DOM.')
    except Exception as e:
        logger.error(e)
        logger.error(f'{load_more_result_css_selector} failed due to {e}')
    else:
        logger.info(f'{load_more_result_css_selector} clicked successfully')


def scrap(url, data):
    # Configure Chrome options to block image loading and disable automation features
    options = webdriver.ChromeOptions()

    chrome_prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", chrome_prefs)

    # Disable blink features related to automation control
    options.add_argument('--disable-blink-features=AutomationControlled')

    # Initialize the Chrome driver with the configured options
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 5)

    click_pop_up_ad(wait, driver)

    while True:
        # Get current height
        current_height = driver.execute_script("return window.scrollY")
        print(current_height)

        # Scroll down to the bottom
        driver.execute_script("window.scrollBy(0, 2000);")

        # Wait for some time to load more content (adjust as needed)
        time.sleep(1)

        # Get current height
        new_height = driver.execute_script("return window.scrollY")
        print(new_height)

        # If the new height is the same as the last height, then the bottom is reached
        if current_height == new_height:
            break

        time.sleep(2)

        click_load_more_result_button(driver)

    # Get the page source after the page has loaded
    html = driver.page_source

    # Close the webdriver after obtaining the HTML content
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    hotel_class = 'f6431b446c.a15b38c233'
    price_class = 'f6431b446c.fbfd7c1165.e84eb96b1f'
    review_class = 'a3b8729ab1.d86cee9b25'
    box_class = 'c066246e13'

    # Find the box elements
    box_elements = soup.select(f'.{box_class}')

    for box_element in box_elements:
        # Find the elements within the box element
        hotel_element = box_element.select(f'.{hotel_class}')
        price_element = box_element.select(f'.{price_class}')
        review_element = box_element.select(f'.{review_class}')

        # Check if all elements are present before extracting data
        if hotel_element and price_element and review_element:
            hotel_name = hotel_element[0].text
            price = re.sub(r'[^0-9]', '', price_element[0].text)
            review_score = review_element[0].text.split()[1]

            data['Hotel'].append(hotel_name)
            data['Price'].append(price)
            data['Review'].append(review_score)


def main():
    city = 'Osaka'
    check_in = '2024-05-20'
    check_out = '2024-05-21'
    group_adults = '1'
    num_rooms = '1'
    group_children = '0'
    selected_currency = 'GBP'

    url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
           f'={check_in}&checkout={check_out}&group_adults={group_adults}'
           f'&no_rooms={num_rooms}&group_children={group_children}&selected_currency={selected_currency}')

    # Create a DataFrame to store the data
    data = {'Hotel': [], 'Price': [], 'Review': []}

    url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
           f'={check_in}&checkout={check_out}&group_adults={group_adults}'
           f'&no_rooms={num_rooms}&group_children={group_children}'
           f'&selected_currency={selected_currency}')

    scrap(url, data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Remove duplicate rows from the DataFrame based on 'Hotel' column
    df_filtered = df.drop_duplicates(subset='Hotel')

    # Convert 'Price' and 'Review' columns to numeric using .loc
    df_filtered.loc[:, 'Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df_filtered.loc[:, 'Review'] = pd.to_numeric(df['Review'], errors='coerce')

    # Add a new column for the ratio of Price to Review using .loc
    df_filtered.loc[:, 'Price/Review'] = df_filtered['Price'] / df_filtered['Review']

    # Sort the DataFrame based on the 'Price/Review' column
    df_filtered = df_filtered.sort_values(by='Price/Review')

    # Save the DataFrame to an Excel file
    excel_filename = f'{city}_hotel_{selected_currency}_sorted.xlsx'
    df_filtered.to_excel(excel_filename, index=False, header=True)
    print(f'Data has been saved to {excel_filename}')


if __name__ == '__main__':
    main()
