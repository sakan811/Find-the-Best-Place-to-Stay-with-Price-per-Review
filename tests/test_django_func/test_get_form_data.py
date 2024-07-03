import pytest

from app.app_func.utils_func import get_form_data


def test_get_form_data_basic():
    cleaned_data = {
        'city': 'London',
        'check_in': '2024-07-01',
        'check_out': '2024-07-10',
        'group_adults': 2,
        'num_rooms': 1,
        'group_children': 1,
        'selected_currency': 'GBP',
        'hotel_filter': True
    }
    expected = ('2024-07-01', '2024-07-10', 'London', 2, 1, True, 1, 'GBP')
    assert get_form_data(cleaned_data) == expected


def test_get_form_data_missing_optional_fields():
    cleaned_data = {
        'city': 'Paris',
        'check_in': '2024-08-01',
        'check_out': '2024-08-10',
        'group_adults': '3'
    }
    expected = ('2024-08-01', '2024-08-10', 'Paris', '3', None, None, None, None)
    assert get_form_data(cleaned_data) == expected


def test_get_form_data_invalid_numeric_values():
    cleaned_data = {
        'city': 'Berlin',
        'check_in': '2024-09-01',
        'check_out': '2024-09-10',
        'group_adults': 'not_a_number',
        'num_rooms': 'not_a_number',
        'group_children': 'not_a_number',
        'selected_currency': 'EUR',
        'hotel_filter': True
    }
    expected = ('2024-09-01',
                '2024-09-10',
                'Berlin',
                'not_a_number',
                'not_a_number',
                True,
                'not_a_number',
                'EUR')
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
    expected = ('2024-10-01', '2024-10-10', 'Tokyo', 2, 1, None, None, 'JPY')
    assert get_form_data(cleaned_data) == expected


if __name__ == '__main__':
    pytest.main()
