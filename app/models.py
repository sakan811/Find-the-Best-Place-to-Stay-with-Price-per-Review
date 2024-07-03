from django.db import models


class RoomPrice(models.Model):
    hotel = models.CharField(max_length=100)
    room_price = models.FloatField()
    review_score = models.FloatField()
    price_per_review = models.FloatField()
    check_in = models.DateField()
    check_out = models.DateField()
    as_of_date = models.DateField()
    city = models.CharField(max_length=100)

