import datetime
import json
from unittest.mock import patch, MagicMock

import pandas as pd
import pytz
from django.test import TestCase, RequestFactory
from django.urls import reverse

from app.views import start_web_scraping


class TestStartWebScrape(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('app.views.Scraper')
    def test_table_page(self, MockScraper):
        # Configure mock to return a DataFrame
        mock_scraper_instance = MagicMock()
        mock_df = pd.DataFrame({
            'Hotel': ['Test Hotel'],
            'Price': [100],
            'Review': [4.5],
            'Price/Review': [22.22],
            'City': ['London'],
            'AccommodationName': ['Hotel Accommodation'],
            'CheckIn': ['2025-04-07'],
            'CheckOut': ['2025-04-08'],
            'AsOf': ['2025-04-07'],
        })
        mock_scraper_instance.scrape_graphql.return_value = mock_df
        MockScraper.return_value = mock_scraper_instance
        
        japan_tz = pytz.timezone("Asia/Tokyo")

        check_in = datetime.datetime.now(japan_tz).strftime("%Y-%m-%d")
        check_out = datetime.datetime.now(japan_tz) + datetime.timedelta(days=1)
        check_out = check_out.strftime("%Y-%m-%d")

        mock_form = {
            "city": "London",
            "country": "United Kingdom",
            "check_in": check_in,
            "check_out": check_out,
            "group_adults": 2,
            "num_rooms": 1,
            "group_children": 0,
            "selected_currency": "USD",
            "hotel_filter": True,
        }

        json_data = json.dumps(mock_form)

        # Mock the form submission in a POST request
        url = reverse("start_web_scraping")
        request = self.factory.post(
            url, data=json_data, content_type="application/json"
        )

        # Pass the request to your view
        response = start_web_scraping(request)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)

    def test_invalid_request_method(self):
        url = reverse("start_web_scraping")
        request = self.factory.get(url)  # Sending a GET request instead of POST

        # Pass the request to your view
        response = start_web_scraping(request)

        # Assert the response status code and content
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.data["detail"], 'Method "GET" not allowed.')
