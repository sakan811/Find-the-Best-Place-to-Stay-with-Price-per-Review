from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import RoomPrice


class GetHotelDataFromDbTests(APITestCase):
    def setUp(self):
        # Create some test data
        RoomPrice.objects.create(
            hotel="Hotel A",
            room_price=100.0,
            review_score=4.5,
            price_per_review=22.22,
            check_in="2023-10-01",
            check_out="2023-10-05",
            as_of_date="2023-09-30",
            city="City A",
        )
        RoomPrice.objects.create(
            hotel="Hotel B",
            room_price=150.0,
            review_score=4.0,
            price_per_review=37.5,
            check_in="2023-10-01",
            check_out="2023-10-05",
            as_of_date="2023-09-30",
            city="City B",
        )

    def test_get_hotel_data_success(self):
        url = reverse("get_hotel_data_from_db")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("hotel_data", response_data)
        self.assertEqual(len(response_data["hotel_data"]), 2)

    def test_invalid_request_method(self):
        url = reverse("get_hotel_data_from_db")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()["detail"], 'Method "POST" not allowed.')
