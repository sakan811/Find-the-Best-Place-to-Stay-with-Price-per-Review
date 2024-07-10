from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from app.models import RoomPrice


class TestSaveScrapedData(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create test data
        RoomPrice.objects.create(
            hotel="Test Hotel 1",
            room_price=100.0,
            review_score=4.5,
            price_per_review=22.22,
            check_in="2024-01-01",
            check_out="2024-01-02",
            as_of_date="2024-01-01",
            city="London"
        )
        RoomPrice.objects.create(
            hotel="Test Hotel 2",
            room_price=200.0,
            review_score=4.0,
            price_per_review=50.0,
            check_in="2024-01-03",
            check_out="2024-01-04",
            as_of_date="2024-01-03",
            city="London"
        )

        self.client = Client()

    def test_save_scraped_data_success(self):
        # Test the successful saving of scraped data
        response = self.client.post(reverse('save_scraped_data_view'))  # Ensure the URL name is correct
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success_msg': 'success_msg'})

    def test_save_scraped_data_no_data(self):
        # Test when there is no data to save
        RoomPrice.objects.all().delete()  # Delete all test data
        response = self.client.post(reverse('save_scraped_data_view'))
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error_msg': 'No data found to save'})

    def test_save_scraped_data_invalid_method(self):
        # Test when the request method is not POST
        response = self.client.get(reverse('save_scraped_data_view'))
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'error_msg': 'Invalid request method'})

    def test_save_scraped_data_unexpected_error(self):
        # Test for unexpected errors (e.g., database error, etc.)
        with self.assertRaises(Exception):
            response = self.client.post(reverse('save_scraped_data_view'))
            self.assertEqual(response.status_code, 500)
            self.assertJSONEqual(response.content, {'error_msg': 'error_msg'})
