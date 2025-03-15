from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import BookingDetails


class GetBookingDetailsFromDbTests(APITestCase):
    def setUp(self):
        # Create some test data
        BookingDetails.objects.create(
            check_in="2023-10-01",
            check_out="2023-10-05",
            city="City A",
            num_adults=2,
            num_children=1,
            num_rooms=1,
            currency="USD",
            only_hotel=True,
        )
        BookingDetails.objects.create(
            check_in="2023-10-10",
            check_out="2023-10-15",
            city="City B",
            num_adults=3,
            num_children=2,
            num_rooms=2,
            currency="EUR",
            only_hotel=False,
        )

    def test_get_booking_details_success(self):
        url = reverse("get_booking_details_from_db")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("booking_data", response_data)
        self.assertEqual(len(response_data["booking_data"]), 2)

    def test_invalid_request_method(self):
        url = reverse("get_booking_details_from_db")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["detail"], 'Method "POST" not allowed.')
