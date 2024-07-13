from datetime import datetime
from unittest.mock import patch

from app.models import RoomPrice
from django.test import TestCase, Client
from django.urls import reverse


class SaveScrapedDataViewTestCase(TestCase):

    def setUp(self):
        # Set up mock data for RoomPrice objects
        self.room_prices = [
            {
                'hotel': 'Hotel A',
                'room_price': 100,
                'review_score': 4.5,
                'price_per_review': 22.22,
                'check_in': datetime(2024, 7, 10),
                'check_out': datetime(2024, 7, 12),
                'as_of_date': datetime(2024, 7, 8),
                'city': 'Swansea'
            },
            {
                'hotel': 'Hotel B',
                'room_price': 150,
                'review_score': 4.0,
                'price_per_review': 37.5,
                'check_in': datetime(2024, 7, 10),
                'check_out': datetime(2024, 7, 12),
                'as_of_date': datetime(2024, 7, 8),
                'city': 'Swansea'
            }
        ]
        for room_price_data in self.room_prices:
            RoomPrice.objects.create(**room_price_data)

    def test_save_scraped_data_view_post_success(self):
        client = Client()
        url = reverse('save_scraped_data_view')

        with patch('app.views.RoomPrice.objects.all') as mock_all:
            mock_all.return_value.values.return_value.order_by.return_value = self.room_prices

            response = client.post(url, {})

        self.assertEqual(response.status_code, 200)
        self.assertIn('filename', response.json())
        self.assertIn('file_content', response.json())

    def test_save_scraped_data_view_post_no_data(self):
        client = Client()
        url = reverse('save_scraped_data_view')

        with patch('app.views.RoomPrice.objects.all') as mock_all:
            mock_all.return_value.values.return_value.order_by.return_value = []

            response = client.post(url, {})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error_msg'], 'No data found to save')

    def test_save_scraped_data_view_post_value_error(self):
        client = Client()
        url = reverse('save_scraped_data_view')

        with patch('app.views.RoomPrice.objects.all') as mock_all:
            mock_all.return_value.values.side_effect = ValueError('Invalid JSON data received')

            response = client.post(url, {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error_msg'], 'error_msg')

    def test_save_scraped_data_view_post_unexpected_error(self):
        client = Client()
        url = reverse('save_scraped_data_view')

        with patch('app.views.RoomPrice.objects.all') as mock_all:
            mock_all.return_value.values.side_effect = Exception('Unexpected error occurred')

            response = client.post(url, {})

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error_msg'], 'error_msg')

    def test_save_scraped_data_view_invalid_method(self):
        client = Client()
        url = reverse('save_scraped_data_view')

        response = client.get(url)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error_msg'], 'Invalid request method')

