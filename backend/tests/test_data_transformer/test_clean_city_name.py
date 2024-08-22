import pytest

from scraper.scraper_func.data_transformer import clean_city_name


@pytest.fixture
def city_data():
    return [
        ('San Francisco, USA', 'San Francisco'),
        ('Los Angeles, CA, USA', 'Los Angeles'),
        ('New York, NY, USA', 'New York'),
        ('Tokyo, Japan', 'Tokyo'),
        ('Osaka, Osaka, Japan', 'Osaka'),
        ('Test City, Test District, Test Country', 'Test City')
    ]


def test_clean_city_name(city_data):
    for city, expected_cleaned_city in city_data:
        assert clean_city_name(city) == expected_cleaned_city
