import re
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrap(url, data):
    try:
        # Configure Chrome options to block image loading and disable automation features
        options = webdriver.ChromeOptions()

        # Disable image loading
        options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.images": 2,
            }
        )

        # Disable blink features related to automation control
        options.add_argument('--disable-blink-features=AutomationControlled')

        # Initialize the Chrome driver with the configured options
        driver = webdriver.Chrome(options=options)
        driver.get(url)

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
                review_score = review_element[0].text

                data['Hotel'].append(hotel_name)
                data['Price'].append(price)
                data['Review'].append(review_score)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


def find_page_num_and_property_num(url):
    try:
        # Configure Chrome options to block image loading and disable automation features
        options = webdriver.ChromeOptions()

        # Disable image loading
        options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.images": 2,
            }
        )

        # Disable blink features related to automation control
        options.add_argument('--disable-blink-features=AutomationControlled')

        # Initialize the Chrome driver with the configured options
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Get the page source after the page has loaded
        html = driver.page_source

        # Close the webdriver after obtaining the HTML content
        driver.quit()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        property_selector = ('#bodyconstraint-inner > div:nth-child(8) > div > div.af5895d4b2 > div.df7e6ba27d > '
                          'div.bcbf33c5c3')
        property_element = soup.select_one(property_selector)
        property_num = int(property_element.text.split()[1])
        page_num = property_num // 26

        return page_num, property_num

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None, None


def main():
    city = 'London'
    check_in = '2023-12-22'
    check_out = '2023-12-23'
    group_adults = '2'
    num_rooms = '1'
    group_children = '0'
    selected_currency = 'GBP'

    url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
           f'={check_in}&checkout={check_out}&group_adults={group_adults}'
           f'&no_rooms={num_rooms}&group_children={group_children}&selected_currency={selected_currency}')
    page_num, property_num = find_page_num_and_property_num(url)
    offset = page_num * 25

    # Create a DataFrame to store the data
    data = {'Hotel': [], 'Price': [], 'Review': []}

    try:
        for page in range(0, offset + 25, 25):
            url = (f'https://www.booking.com/searchresults.en-gb.html?ss={city}&checkin'
                   f'={check_in}&checkout={check_out}&group_adults={group_adults}'
                   f'&no_rooms={num_rooms}&group_children={group_children}&offset={page}'
                   f'&selected_currency={selected_currency}')
            scrap(url, data)

    except Exception as e:
        logger.error(f"An error occurred in the main loop: {str(e)}")

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Remove duplicate rows from the DataFrame based on 'Hotel' column
    df_filtered = df.drop_duplicates(subset='Hotel')

    # Convert 'Price' and 'Review' columns to numeric using .loc
    df_filtered.loc[:, 'Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df_filtered.loc[:, 'Review'] = pd.to_numeric(df['Review'], errors='coerce')

    # Add a new column for the ratio of Price to Review using .loc
    df_filtered.loc[:, 'Price/Review'] = df_filtered['Price'] / df_filtered['Review']

    # Filter the DataFrame to include only the first property_num rows
    # In case the website shows properties outside the desired location
    df_filtered = df_filtered.head(property_num)

    # Sort the DataFrame based on the 'Price/Review' column
    df_filtered = df_filtered.sort_values(by='Price/Review')

    # Save the DataFrame to an Excel file
    excel_filename = f'{city}_hotel_{selected_currency}_sorted.xlsx'
    df_filtered.to_excel(excel_filename, index=False, header=True)
    print(f'Data has been saved to {excel_filename}')


if __name__ == '__main__':
    main()
