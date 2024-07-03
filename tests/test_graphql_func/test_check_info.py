from unittest.mock import Mock

import pytest

from scraper.scraper_func.graphql_func import check_info


def test_returns_correct_total_page_number_and_data_mapping():
    # Given
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'data': {
            'searchQueries': {
                'search': {
                    'pagination': {'nbResultsTotal': 1},
                    'breadcrumbs': [{}, {}, {'name': 'Test City'}],
                    'flexibleDatesConfig': {
                        'dateRangeCalendar': {
                            'checkin': ['2023-01-01'],
                            'checkout': ['2023-01-02']
                        }
                    },
                    'searchMeta': {
                        'nbAdults': 2,
                        'nbChildren': 1,
                        'nbRooms': 1
                    },
                    'results': [{
                        'blocks': [{
                            'finalPrice': {'currency': 'USD'}
                        }]
                    }]
                }
            }
        }
    }
    entered_city = "Test City"
    entered_check_in = "2023-01-01"
    entered_check_out = "2023-01-02"
    entered_selected_currency = "USD"
    entered_num_adult = 2
    entered_num_children = 1
    entered_num_room = 1

    # When
    result = check_info(
        response_mock, entered_city, entered_check_in, entered_check_out,
        entered_selected_currency, entered_num_adult, entered_num_children,
        entered_num_room
    )

    # Then
    assert result == (1, {
        "city": "Test City",
        "check_in": "2023-01-01",
        "check_out": "2023-01-02",
        "num_adult": 2,
        "num_children": 1,
        "num_room": 1,
        "selected_currency": "USD"
    })


def test_handles_response_with_missing_or_null_fields_gracefully():
    # Given
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'data': {
            'searchQueries': {
                'search': {
                    'pagination': {'nbResultsTotal': 1},
                    'breadcrumbs': [{}, {}, {'name': None}],
                    'flexibleDatesConfig': {
                        'dateRangeCalendar': {
                            'checkin': [None],
                            'checkout': [None]
                        }
                    },
                    'searchMeta': {
                        'nbAdults': None,
                        'nbChildren': None,
                        'nbRooms': None
                    },
                    'results': [{
                        'blocks': [{
                            'finalPrice': {'currency': None}
                        }]
                    }]
                }
            }
        }
    }
    entered_city = "Test City"
    entered_check_in = "2023-01-01"
    entered_check_out = "2023-01-02"
    entered_selected_currency = "USD"
    entered_num_adult = 2
    entered_num_children = 1
    entered_num_room = 1

    # When
    error_message = ''
    try:
        check_info(
            response_mock, entered_city, entered_check_in, entered_check_out,
            entered_selected_currency, entered_num_adult, entered_num_children,
            entered_num_room
        )
    except SystemExit as e:
        error_message = str(e)

    # Then
    assert error_message == "Error City not match: Test City != None"


def test_data_mapping_dictionary_keys():
    # Given
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'data': {
            'searchQueries': {
                'search': {
                    'pagination': {'nbResultsTotal': 1},
                    'breadcrumbs': [{}, {}, {'name': 'Test City'}],
                    'flexibleDatesConfig': {
                        'dateRangeCalendar': {
                            'checkin': ['2023-01-01'],
                            'checkout': ['2023-01-02']
                        }
                    },
                    'searchMeta': {
                        'nbAdults': 2,
                        'nbChildren': 1,
                        'nbRooms': 1
                    },
                    'results': [{
                        'blocks': [{
                            'finalPrice': {'currency': 'USD'}
                        }]
                    }]
                }
            }
        }
    }
    entered_city = "Test City"
    entered_check_in = "2023-01-01"
    entered_check_out = "2023-01-02"
    entered_selected_currency = "USD"
    entered_num_adult = 2
    entered_num_children = 1
    entered_num_room = 1

    # When
    result = check_info(
        response_mock, entered_city, entered_check_in, entered_check_out,
        entered_selected_currency, entered_num_adult, entered_num_children,
        entered_num_room
    )

    # Then
    assert result == (1, {
        "city": "Test City",
        "check_in": "2023-01-01",
        "check_out": "2023-01-02",
        "num_adult": 2,
        "num_children": 1,
        "num_room": 1,
        "selected_currency": "USD"
    })


def test_data_mapping_extraction():
    # Given
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'data': {
            'searchQueries': {
                'search': {
                    'pagination': {'nbResultsTotal': 1},
                    'breadcrumbs': [{}, {}, {'name': 'Test City'}],
                    'flexibleDatesConfig': {
                        'dateRangeCalendar': {
                            'checkin': ['2023-01-01'],
                            'checkout': ['2023-01-02']
                        }
                    },
                    'searchMeta': {
                        'nbAdults': 2,
                        'nbChildren': 1,
                        'nbRooms': 1
                    },
                    'results': [{
                        'blocks': [{
                            'finalPrice': {'currency': 'USD'}
                        }]
                    }]
                }
            }
        }
    }
    entered_city = "Test City"
    entered_check_in = "2023-01-01"
    entered_check_out = "2023-01-02"
    entered_selected_currency = "USD"
    entered_num_adult = 2
    entered_num_children = 1
    entered_num_room = 1

    # When
    result = check_info(
        response_mock, entered_city, entered_check_in, entered_check_out,
        entered_selected_currency, entered_num_adult, entered_num_children,
        entered_num_room
    )

    # Then
    assert result == (1, {
        "city": "Test City",
        "check_in": "2023-01-01",
        "check_out": "2023-01-02",
        "num_adult": 2,
        "num_children": 1,
        "num_room": 1,
        "selected_currency": "USD"
    })


if __name__ == '__main__':
    pytest.main()