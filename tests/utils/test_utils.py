from datetime import date, time

import pytest

from birthday_bot.utils.utils import (create_alert_date, create_alert_time,
                                      is_alert_date_next_year, is_str_date,
                                      is_str_date_without_year, is_coming_new_year)


@pytest.mark.parametrize(
    "test_string,expected",
    [
        ("10.11.1990", True),
        ("test", False),
        ("33.33.33", False),
    ]
)
def test_is_str_date(test_string, expected):
    assert is_str_date(test_string) == expected


@pytest.mark.parametrize(
    "test_string,expected",
    [
        ("10.11", True),
        ("test", False),
        ("33.33", False),
    ]
)
def test_is_str_date_without_year(test_string, expected):
    assert is_str_date_without_year(test_string) == expected


@pytest.mark.parametrize(
    "alert_str,birthday_day,birthday_month,expected",
    [
        ("День в день", 1, 1, date(2024, 1, 1)),
        ("За 1 день", 10, 10, date(2023, 10, 9)),
        ("За 3 дня", 1, 1, date(2023, 12, 29)),
        ("За 7 дней", 10, 10, date(2023, 10, 3)),
    ]
)
def test_create_alert_date(alert_str, birthday_day, birthday_month, expected):
    assert create_alert_date(alert_str, birthday_day, birthday_month) == expected


@pytest.mark.parametrize(
    "alert_time_str,expected",
    [
        ("08:00", time(8, 0)),
        ("10:00", time(10, 0)),
        ("12:00", time(12, 0)),
        ("15:00", time(15, 0)),
    ]
)
def test_create_alert_time(alert_time_str, expected):
    assert create_alert_time(alert_time_str) == expected


@pytest.mark.parametrize(
    "birthday_day,birthday_month,expected",
    [
        (1, 1, True),
        (12, 12, False),
        (date.today().day, date.today().month, True),
    ]
)
def test_is_alert_date_next_year(birthday_day, birthday_month, expected):
    assert is_alert_date_next_year(birthday_day, birthday_month) == expected


@pytest.mark.parametrize(
    "date_today,expected",
    [
        (date(2020, 10, 10), False),
        (date(2020, 1, 1), True),
    ]
)
def test_is_coming_new_year(date_today, expected):
    assert is_coming_new_year(date_today) == expected
