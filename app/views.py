import json
import sys

import pandas as pd
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from loguru import logger

from app.app_func.db_func import truncate_db, save_data_to_db
from app.app_func.utils_func import get_form_data
from app.models import RoomPrice
from scraper.graphql_scraper import scrape_graphql
from scraper.scraper_func.utils import save_scraped_data

logger.configure(handlers=[{"sink": sys.stdout, "level": "INFO"}])
logger.add('find_best_place_to_stay.log', level='INFO',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


@csrf_exempt
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


@csrf_exempt
def hotel_booking_form(request):
    logger.info('Rendering hotel booking form...')
    return render(request, 'form.html')


@csrf_exempt
def get_hotel_data_from_db(request):
    if request.method == 'GET':
        logger.info('Fetching hotel data from database...')

        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT hotel, room_price, review_score, price_per_review, check_in, check_out, city 
            FROM app_roomprice
            order by price_per_review
            ''')
            data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in data]
            return JsonResponse({'hotel_data': results})
    else:
        logger.error('Invalid request method')
        return JsonResponse({'error_msg': 'Invalid request method'}, status=405)


@csrf_exempt
def hotel_data_table_page(request):
    if request.method == 'GET':
        logger.info('Rendering hotel table page...')
        return render(request, 'table.html')
    else:
        logger.error('Invalid request method')
        return JsonResponse({'error_msg': 'Invalid request method'}, status=405)


@csrf_exempt
def start_web_scraping(request):
    logger.info('Starting web-scraping...')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            check_in, check_out, city, group_adults, group_children, hotel_filter, num_rooms, selected_currency = get_form_data(data)

            df = scrape_graphql(city=city, check_in=check_in, check_out=check_out,
                                group_adults=group_adults, group_children=group_children,
                                num_rooms=num_rooms, hotel_filter=hotel_filter,
                                selected_currency=selected_currency)

            truncate_db()
            save_data_to_db(df)

            return JsonResponse({'success_msg': 'success_msg'})
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
