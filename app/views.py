import json
import sys
from datetime import date

import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from loguru import logger

from app.app_func.db_func import truncate_db, save_data_to_db
from app.forms import ScrapingForm
from app.models import RoomPrice
from scraper.graphql_scraper import scrape_graphql
from scraper.scraper_func.utils import save_scraped_data

logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])
logger.add('find_best_place_to_stay.log', level='INFO',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def save_scraped_data_view(request):
    logger.info('Saving HTML table as Excel...')
    if request.method == 'POST':
        try:
            # Query data from the database
            room_prices = RoomPrice.objects.all().values()

            city: dict = RoomPrice.objects.values('city').first()
            check_in: dict = RoomPrice.objects.values('check_in').first()
            check_out: dict = RoomPrice.objects.values('check_out').first()

            if not room_prices:
                return JsonResponse({'error_msg': 'No data found to save'}, status=404)

            # Create a Pandas DataFrame from the data
            df = pd.DataFrame(room_prices)

            save_scraped_data(dataframe=df, city=city, check_in=check_in, check_out=check_out)

            # Return success response as JSON
            return JsonResponse({'success_msg': 'success_msg'})

        except ValueError:
            logger.error('ValueError: Invalid JSON data received')
            return JsonResponse({'error_msg': 'error_msg'}, status=400)

        except Exception as e:
            logger.error(e)
            logger.error('Unexpected error occurred')

            # Return error response as JSON
            return JsonResponse({'error_msg': 'error_msg'}, status=500)
    else:
        return JsonResponse({'error_msg': 'Invalid request method'}, status=405)


def hotel_booking_form(request):
    logger.info('Showing hotel booking form...')

    form = ScrapingForm()

    return render(request, 'form.html', {'form': form})


def start_web_scraping(request):
    logger.info('Starting web-scraping...')
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            try:
                cleaned_data = form.cleaned_data

                city = cleaned_data.get('city')
                check_in = cleaned_data.get('check_in')
                check_out = cleaned_data.get('check_out')
                group_adults = int(cleaned_data.get('group_adults', 0))
                num_rooms = int(cleaned_data.get('num_rooms', 0))
                group_children = int(cleaned_data.get('group_children', 0))
                selected_currency = cleaned_data.get('selected_currency')
                hotel_filter = cleaned_data.get('hotel_filter') == 'on'

                if isinstance(check_in, date):
                    check_in = check_in.strftime('%Y-%m-%d')
                if isinstance(check_out, date):
                    check_out = check_out.strftime('%Y-%m-%d')

                df = scrape_graphql(city=city, check_in=check_in, check_out=check_out,
                                    group_adults=group_adults, group_children=group_children,
                                    num_rooms=num_rooms, hotel_filter=hotel_filter,
                                    selected_currency=selected_currency)

                truncate_db()
                save_data_to_db(df)

                selected_cols = ['City', 'Hotel', 'Review', 'Price', 'Price/Review', 'CheckIn', 'CheckOut']
                df = df[selected_cols]

                df = df.sort_values(by='Price/Review')

                # Convert DataFrame to HTML table
                html_table = df.to_html(index=False)

                return render(request,'table.html', {'html_table': html_table})
            except IndexError as e:
                logger.error(e)
                logger.error('IndexError')
                return JsonResponse({"IndexError": str(e)}, status=500)

            except Exception as e:
                logger.error(e)
                logger.error('Unexpected error occurred')
                return JsonResponse({"Unexpected error occurred": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
