from app.models import RoomPrice
from django.test import TestCase, Client
from django.urls import reverse


class SaveScrapedDataViewTests(TestCase):

    def setUp(self):
        # Set up test data
        self.client = Client()
        self.url = reverse('save_scraped_data_view')  # Replace with the name of your URL pattern
        RoomPrice.objects.create(
            hotel='Hotel A',
            room_price=100,
            review_score=4.5,
            price_per_review=22.22,
            check_in='2024-07-10',
            check_out='2024-07-12',
            as_of_date='2024-07-08',
            city='Swansea'
        )
        RoomPrice.objects.create(
            hotel='Hotel B',
            room_price=150,
            review_score=4.0,
            price_per_review=37.5,
            check_in='2024-07-10',
            check_out='2024-07-12',
            as_of_date='2024-07-08',
            city='Swansea'
        )

    def test_save_scraped_data_success(self):
        response = self.client.post(self.url)

        # Check for a successful response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertTrue('Content-Disposition' in response)

        # Check that the filename is correctly set in the Content-Disposition header
        content_disposition = response['Content-Disposition']
        self.assertIn('attachment; filename="Swansea_hotel_data_2024-07-10_to_2024-07-12.xlsx"', content_disposition)

    def test_save_scraped_data_no_data(self):
        # Clear the RoomPrice table
        RoomPrice.objects.all().delete()

        response = self.client.post(self.url)

        # Check for a 404 response when no data is found
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error_msg': 'No data found to save'})

    def test_save_scraped_data_invalid_method(self):
        response = self.client.get(self.url)

        # Check for a 405 response when using an invalid request method
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {'error_msg': 'Invalid request method'})