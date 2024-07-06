from django.urls import path

from . import views

urlpatterns = [
    path('', views.hotel_booking_form, name='hotel_booking_form'),
    path('scraping/', views.start_web_scraping, name='start_web_scraping'),
    path('hotel_data_table_page/', views.hotel_data_table_page, name='hotel_data_table_page'),
    path('get_hotel_data_from_db/', views.get_hotel_data_from_db, name='get_hotel_data_from_db'),
    path('save/', views.save_scraped_data_view, name='save_scraped_data_view')
]
