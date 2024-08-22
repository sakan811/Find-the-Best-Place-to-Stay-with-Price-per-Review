import datetime
import json

import pytz
from django.test import TestCase, RequestFactory
from django.urls import reverse

from app.views import start_web_scraping


class TestStartWebScrape(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_table_page(self):
        japan_tz = pytz.timezone('Asia/Tokyo')

        check_in = datetime.datetime.now(japan_tz).strftime('%Y-%m-%d')
        check_out = datetime.datetime.now(japan_tz) + datetime.timedelta(days=1)
        check_out = check_out.strftime('%Y-%m-%d')

        mock_form = {
            'city': 'London',
            'country': 'United Kingdom',
            'check_in': check_in,
            'check_out': check_out,
            'group_adults': 2,
            'num_rooms': 1,
            'group_children': 0,
            'selected_currency': 'USD',
            'hotel_filter': True,
        }

        json_data = json.dumps(mock_form)

        # Mock the form submission in a POST request
        url = reverse('start_web_scraping')  # Replace with your actual URL name
        request = self.factory.post(url, data=json_data, content_type='application/json')

        # Pass the request to your view
        response = start_web_scraping(request)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)



