from datetime import date, datetime, timedelta, time

from telebot.types import ReplyKeyboardMarkup, KeyboardButton


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
        date_datetime = datetime.strptime(input_date_str, "%d.%m.%Y").date()
        date_datetime = True
        return date_datetime
    except ValueError:
        return False


def create_alert_datetime(alert: str, alert_time: str, birthday_day: int, birthday_month: int) -> datetime:
    if alert == "День в день":
        delta_date = 0
    elif alert == "За 1 день":
        delta_date = 1
    elif alert == "За 3 дня":
        delta_date = 3
    else:
        delta_date = 7
    hour, minute = alert_time.split(":")
    alert_time = time(int(hour), int(minute))
    event_date = date(date.today().year, birthday_month, birthday_day)
    alert_date = event_date - timedelta(days=delta_date)
    alert_datetime = datetime.combine(alert_date, alert_time)
    return alert_datetime
