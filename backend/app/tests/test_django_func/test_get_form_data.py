import pytest

from app.app_func.utils_func import get_form_data


def test_get_form_data_basic():
    cleaned_data = {
        'city': 'London',
        'country': 'United Kingdom',
        'check_in': '2024-07-01',
        'check_out': '2024-07-10',
        'group_adults': 2,
        'num_rooms': 1,
        'group_children': 1,
        'selected_currency': 'GBP',
        'hotel_filter': True
    }
    expected = ('2024-07-01', '2024-07-10', 'London', 'United Kingdom', 2, 1, True, 1, 'GBP')
    assert get_form_data(cleaned_data) == expected


def test_get_form_data_missing_optional_fields():
    cleaned_data = {
        'city': 'Paris',
        'check_in': '2024-08-01',
        'check_out': '2024-08-10',
        'group_adults': '3'
    }
    expected = ('2024-08-01', '2024-08-10', 'Paris', None, 3, 0, None, 1, None)
    assert get_form_data(cleaned_data) == expected


def test_get_form_data_invalid_numeric_values():
    cleaned_data = {
        'city': 'Berlin',
        'country': 'Germany',
        'check_in': '2024-09-01',
        'check_out': '2024-09-10',
        'group_adults': 'not_a_number',
        'num_rooms': 'not_a_number',
        'group_children': 'not_a_number',
        'selected_currency': 'EUR',
        'hotel_filter': True
    }
    expected = ('2024-09-01', '2024-09-10', 'Berlin', 'Germany', 1, 0, True, 1, 'EUR')
    assert get_form_data(cleaned_data) == expected


def test_get_form_data_some_fields_missing():
    cleaned_data = {
        'city': 'Tokyo',
        'check_in': '2024-10-01',
        'check_out': '2024-10-10',
        'group_adults': 2,
        'group_children': 1,
        'selected_currency': 'JPY'
    }
    expected = ('2024-10-01', '2024-10-10', 'Tokyo', None, 2, 1, None, 1, 'JPY')
    assert get_form_data(cleaned_data) == expected


if __name__ == '__main__':
    pytest.main()
