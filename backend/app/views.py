import base64
import io
import json

import pandas as pd
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from logging_config import configure_logging_with_file, main_logger
from scraper.graphql_scraper import Scraper
from .app_func.db_func import truncate_roomprice_table, save_data_to_db, save_booking_details_to_db, \
    truncate_booking_details_table
from .app_func.utils_func import get_form_data
from .models import RoomPrice

script_logger = configure_logging_with_file(log_dir='logs', log_file='django_views.log', logger_name='django_views')


@csrf_exempt
def save_scraped_data_view(request):
    main_logger.info('Saving HTML table as Excel...')
    if request.method == 'POST':
        try:
            # Query data from the database
            room_prices = RoomPrice.objects.all().values().order_by('price_per_review')

            city: dict = RoomPrice.objects.values('city').first()
            check_in: dict = RoomPrice.objects.values('check_in').first()
            check_out: dict = RoomPrice.objects.values('check_out').first()

            if not room_prices:
                return JsonResponse({'error_msg': 'No data found to save'}, status=404)

            city = city['city']
            check_in = check_in['check_in'].strftime('%Y-%m-%d')
            check_out = check_out['check_out'].strftime('%Y-%m-%d')

            excel_file_path = f'{city}_hotel_data_{check_in}_to_{check_out}.xlsx'

            # Create a Pandas DataFrame from the data
            df = pd.DataFrame(room_prices)

            # Create an in-memory Excel file
            excel_file = io.BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)

            # Set the filename for download
            filename = excel_file_path

            return JsonResponse({
                'filename': filename,
                'file_content': base64.b64encode(excel_file.getvalue()).decode('utf-8')
            })

        except ValueError:
            main_logger.error('ValueError: Invalid JSON data received')
            return JsonResponse({'error_msg': 'error_msg'}, status=400)

        except Exception as e:
            main_logger.error(e)
            main_logger.error('Unexpected error occurred')

            # Return error response as JSON
            return JsonResponse({'error_msg': 'error_msg'}, status=500)
    else:
        return JsonResponse({'error_msg': 'Invalid request method'}, status=405)


@csrf_exempt
def get_hotel_data_from_db(request):
    if request.method == 'GET':
        main_logger.info('Fetching hotel data from database...')

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
        main_logger.error('Invalid request method')
        return JsonResponse({'error_msg': 'Invalid request method'}, status=405)


@csrf_exempt
def get_booking_details_from_db(request):
    if request.method == 'GET':
        main_logger.info('Fetching hotel booking details from database...')

        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT *
            FROM app_bookingdetails
            ''')
            data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in data]
            return JsonResponse({'booking_data': results})
    else:
        main_logger.error('Invalid request method')
        return JsonResponse({'error_msg': 'Invalid request method'}, status=405)


@csrf_exempt
def start_web_scraping(request):
    main_logger.info('Starting web-scraping...')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            check_in, check_out, city, group_adults, group_children, hotel_filter, num_rooms, selected_currency = get_form_data(
                data)

            truncate_booking_details_table()
            save_booking_details_to_db(check_in=check_in, check_out=check_out, city=city,
                                       num_adults=group_adults, num_children=group_children, num_rooms=num_rooms,
                                       currency=selected_currency, only_hotel=hotel_filter)

            scraper = Scraper(city=city, check_in=check_in, check_out=check_out,
                              group_adults=group_adults, group_children=group_children,
                              num_rooms=num_rooms, hotel_filter=hotel_filter,
                              selected_currency=selected_currency)
            df = scraper.scrape_graphql()

            truncate_roomprice_table()
            save_data_to_db(df)

            return JsonResponse({'success_msg': 'success_msg'})
        except SystemExit as e:
            main_logger.error(e)
            return JsonResponse({'error': 'SystemExit'}, status=500)
        except IndexError as e:
            main_logger.error(e)
            main_logger.error('IndexError')
            return JsonResponse({"error": "IndexError"}, status=500)
        except Exception as e:
            main_logger.error(e)
            main_logger.error('Unexpected error occurred')
            return JsonResponse({"error": "Unexpected error occurred"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
