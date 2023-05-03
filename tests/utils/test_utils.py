import pytest

from birthday_bot.utils.utils import is_str_date, create_alert_date, create_alert_time
from datetime import date, time

@pytest.mark.parametrize(
    "test_string,expected",
    [
        ("10.11.1990", True),
        ("test", False),
        ("33.33.33", False)
    ]
)
def test_is_str_date(test_string, expected):
    assert is_str_date(test_string) == expected


@pytest.mark.parametrize(
    "alert_str,birthday_day,birthday_month,expected",
    [
        ("День в день", 10, 10, date(2023, 10, 10)),
        ("За 1 день", 10, 10, date(2023, 10, 9)),
        ("За 3 дня", 10, 10, date(2023, 10, 7)),
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
