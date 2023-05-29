from datetime import date, datetime, timedelta, time

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from birthday_bot.db.models.user_and_event import Event


def create_main_markup() -> ReplyKeyboardMarkup:
    main_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    first_title = KeyboardButton("Добавить напоминание о Дне Рождения")
    second_title = KeyboardButton("Ближайшие Дни Рождения")
    third_title = KeyboardButton("Изменить напоминание")
    fourth_title = KeyboardButton("Удалить напоминание")
    fifth_title = KeyboardButton("Справка")
    main_markup.row(first_title)
    main_markup.row(second_title, third_title)
    main_markup.row(fourth_title, fifth_title)
    return main_markup


def create_alert_markup() -> ReplyKeyboardMarkup:
    alert_date_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    first_title = KeyboardButton("День в день")
    second_title = KeyboardButton("За 1 день")
    third_title = KeyboardButton("За 3 дня")
    fourth_title = KeyboardButton("За 7 дней")
    alert_date_markup.row(first_title, second_title)
    alert_date_markup.row(third_title, fourth_title)
    return alert_date_markup


def create_time_markup() -> ReplyKeyboardMarkup:
    alert_time_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    first_title = KeyboardButton("8:00")
    second_title = KeyboardButton("10:00")
    third_title = KeyboardButton("12:00")
    fourth_title = KeyboardButton("15:00")
    alert_time_markup.row(first_title, second_title)
    alert_time_markup.row(third_title, fourth_title)
    return alert_time_markup


def create_change_event_markup() -> ReplyKeyboardMarkup:
    change_event_markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    first_title = KeyboardButton("Изменить дату Рождения")
    second_title = KeyboardButton("Изменить дату оповещения")
    third_title = KeyboardButton("Изменить время оповещения")
    change_event_markup.row(first_title)
    change_event_markup.row(second_title, third_title)
    return change_event_markup


def is_str_date(input_date_str: str) -> bool:
    try:
        datetime.strptime(input_date_str, "%d.%m.%Y").date()
        return True
    except ValueError:
        return False


def is_str_date_without_year(input_date_str_with_unknown_year: str) -> bool:
    date_str = input_date_str_with_unknown_year + "." + str(date.today().year)
    try:
        datetime.strptime(date_str, "%d.%m.%Y").date()
        return True
    except ValueError:
        return False


def create_alert_date(alert_str: str, birthday_day: int, birthday_month: int) -> date:
    if alert_str == "День в день":
        delta_date = 0
    elif alert_str == "За 1 день":
        delta_date = 1
    elif alert_str == "За 3 дня":
        delta_date = 3
    else:
        delta_date = 7
    if is_alert_date_next_year(birthday_day, birthday_month):
        event_date = date((date.today().year + 1), birthday_month, birthday_day)
    else:
        event_date = date(date.today().year, birthday_month, birthday_day)
    alert_date = event_date - timedelta(days=delta_date)
    return alert_date


def create_alert_time(alert_time_str: str) -> time:
    hour, minute = alert_time_str.split(":")
    alert_time = time(int(hour), int(minute))
    return alert_time


def is_alert_date_next_year(birthday_day: int, birthday_month: int) -> bool:
    if date(date.today().year, birthday_month, birthday_day) <= date.today():
        return True
    return False


def is_coming_new_year(date_today: date) -> bool:
    yesterday = date_today - timedelta(days=1)
    if date_today.year > yesterday.year:
        return True
    return False


def sorting_events(events: list[Event]) -> list[Event]:
    coming_events = []
    for event in events:
        if date(date.today().year, event.birthday_month, event.birthday_day) > date.today():
            coming_events.append(event)
    for event in events:
        if date(date.today().year, event.birthday_month, event.birthday_day) <= date.today():
            coming_events.append(event)
    return coming_events
