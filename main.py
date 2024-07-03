import sys

from loguru import logger

from scraper.graphql_scraper import scrape_graphql
from scraper.scraper_func.utils import save_scraped_data

logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])
logger.add('find_best_place_to_stay.log', level='INFO',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')

if __name__ == '__main__':
    city = 'Swansea'
    check_in = '2024-08-16'
    check_out = '2024-08-17'
    group_adults = 1
    num_rooms = 1
    group_children = 0
    selected_currency = 'USD'
    hotel_filter = True

    df = scrape_graphql(city=city, check_in=check_in, check_out=check_out, group_adults=group_adults,
                        group_children=group_children, num_rooms=num_rooms, hotel_filter=hotel_filter,
                        selected_currency=selected_currency)

    save_scraped_data(dataframe=df, city=city, check_in=check_in, check_out=check_out)
