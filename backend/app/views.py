import base64
import io

import pandas as pd
from django.db import connection
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from logging_config import main_logger
from scraper.graphql_scraper import Scraper
from .app_func.db_func import truncate_roomprice_table, save_data_to_db, save_booking_details_to_db, \
    truncate_booking_details_table
from .app_func.utils_func import get_form_data
from .models import RoomPrice


@api_view(['POST'])
def save_scraped_data_view(request):
    main_logger.info('Saving HTML table as Excel...')
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


@api_view(['GET'])
def get_hotel_data_from_db(request):
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


@api_view(['GET'])
def get_booking_details_from_db(request):
    main_logger.info('Fetching hotel booking details from database...')

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT *
            FROM app_bookingdetails
        ''')
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in data]
        return Response({'booking_data': results}, status=status.HTTP_200_OK)


@api_view(['POST'])
def start_web_scraping(request):
    main_logger.info('Starting web-scraping...')
    try:
        data = request.data

        check_in, check_out, city, country, group_adults, group_children, \
            hotel_filter, num_rooms, selected_currency = get_form_data(data)

        truncate_booking_details_table()
        save_booking_details_to_db(check_in=check_in, check_out=check_out, city=city,
                                   num_adults=group_adults, num_children=group_children, num_rooms=num_rooms,
                                   currency=selected_currency, only_hotel=hotel_filter)

        scraper = Scraper(city=city, country=country, check_in=check_in, check_out=check_out,
                          group_adults=group_adults, group_children=group_children,
                          num_rooms=num_rooms, hotel_filter=hotel_filter,
                          selected_currency=selected_currency)
        df = scraper.scrape_graphql()

        truncate_roomprice_table()
        save_data_to_db(df)

        return Response({'success_msg': 'success_msg'}, status=status.HTTP_200_OK)
    except SystemExit as e:
        main_logger.error(e)
        return Response({'error': 'SystemExit'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except IndexError as e:
        main_logger.error(e)
        main_logger.error('IndexError')
        return Response({"error": "IndexError"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        main_logger.error(e)
        main_logger.error('Unexpected error occurred')
        return Response({"error": "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)