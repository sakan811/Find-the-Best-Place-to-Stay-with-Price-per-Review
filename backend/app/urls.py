from django.urls import path

from . import views

urlpatterns = [
    path('scraping/', views.start_web_scraping, name='start_web_scraping'),
    path('get_hotel_data_from_db/', views.get_hotel_data_from_db, name='get_hotel_data_from_db'),
    path('get_booking_details_from_db/', views.get_booking_details_from_db, name='get_booking_details_from_db'),
    path('save/', views.save_scraped_data_view, name='save_scraped_data_view')
]
