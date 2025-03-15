from django.test import TestCase

from app.models import RoomPrice


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        # Create necessary test data
        self.room_price = RoomPrice.objects.create(
            accommodation_name="Test Hotel",
            # ... other required fields ...
        )
