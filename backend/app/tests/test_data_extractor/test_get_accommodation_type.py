import pytest

from scraper.scraper_func.data_extractor import get_accommodation_type_name


def test_get_accommodation_type_name_hotels():
    assert get_accommodation_type_name(204) == "Hotels"


def test_get_accommodation_type_name_apartments():
    assert get_accommodation_type_name(201) == "Apartments"


def test_get_accommodation_type_name_villas():
    assert get_accommodation_type_name(213) == "Villas"


def test_get_accommodation_type_name_guesthouses():
    assert get_accommodation_type_name(216) == "Guesthouses"


def test_get_accommodation_type_name_hostels():
    assert get_accommodation_type_name(203) == "Hostels"


def test_get_accommodation_type_name_entire_homes():
    assert get_accommodation_type_name(219) == "Entire homes & apartments"


def test_get_accommodation_type_name_unknown():
    assert get_accommodation_type_name(999) == "Other"


def test_get_accommodation_type_name_zero():
    assert get_accommodation_type_name(0) == "Other"


def test_get_accommodation_type_name_negative():
    assert get_accommodation_type_name(-1) == "Other"


if __name__ == "__main__":
    pytest.main()
