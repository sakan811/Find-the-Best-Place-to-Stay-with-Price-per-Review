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


class BookingDetails(models.Model):
    check_in = models.DateField()
    check_out = models.DateField()
    city = models.CharField(max_length=100)
    num_adults = models.IntegerField()
    num_children = models.IntegerField()
    num_rooms = models.IntegerField()
    currency = models.CharField(max_length=100)
    only_hotel = models.BooleanField()
