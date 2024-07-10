from django.test import TestCase, RequestFactory
from django.urls import reverse


class TestForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_form_page(self):
        url = reverse('hotel_booking_form')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_form_page_failure(self):
        # Simulate a non-existent URL or another failure scenario
        url = '/non-existent-url/'  # Replace with a non-existent URL or other failure condition
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)