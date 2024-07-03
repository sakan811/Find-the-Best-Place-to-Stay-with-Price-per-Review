from django.urls import path

from . import views

urlpatterns = [
    path('', views.hotel_booking_form, name='hotel_booking_form'),
    path('scraping/', views.start_web_scraping, name='start_web_scraping'),
    path('save/', views.save_scraped_data_view, name='save_scraped_data_view')
]
