# Generated by Django 5.0.6 on 2024-07-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('city', models.CharField(max_length=100)),
                ('num_adults', models.IntegerField()),
                ('num_children', models.IntegerField()),
                ('num_rooms', models.IntegerField()),
                ('currency', models.CharField(max_length=100)),
                ('only_hotel', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='RoomPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.CharField(max_length=100)),
                ('room_price', models.FloatField()),
                ('review_score', models.FloatField()),
                ('price_per_review', models.FloatField()),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('as_of_date', models.DateField()),
                ('city', models.CharField(max_length=100)),
            ],
        ),
    ]