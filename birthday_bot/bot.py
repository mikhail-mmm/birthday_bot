import logging
import schedule
import sentry_sdk
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
import threading
import time
from typing import Type

from birthday_bot.db.models.user_and_event import User
from birthday_bot.db.utils_db import (change_alert_date, change_alert_time,
                                      change_birthday_date, delete_event,
                                      get_coming_event, get_event,
                                      get_events_with_alert_today, get_user,
                                      get_user_id, insert_event, insert_user,
                                      is_event_in_database,
                                      is_user_in_database)
from birthday_bot.utils.settings import API_TOKEN, HELP
from birthday_bot.utils.utils import (create_alert_date, create_alert_markup,
                                      create_alert_time,
                                      create_change_event_markup,
                                      create_main_markup, create_time_markup,
                                      is_str_date)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename="bot.log", filemode="w",
    logger = logging.getLogger(__name__)
)

sentry_sdk.init(
    dsn="https://0364b814666c409aa2891de7f135e9a4@o4505036422971392.ingest.sentry.io/4505036504432640",
    traces_sample_rate=0.85,
)

bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def start(message: Message) -> None:
    bot.send_message(message.chat.id, f"<b>{message.chat.first_name}</b>, привет! 👋", parse_mode="html")
    if not is_user_in_database(message.chat.id):
        user = User(
            name=message.chat.first_name,
            chat_id=message.chat.id,
        )
        insert_user(user)
    a = 1 / 0
    main_markup = create_main_markup()
    bot.send_message(message.chat.id, 'Выберите что вам надо:', reply_markup=main_markup)


@bot.message_handler(regexp="Справка")
def help(message: Message) -> None:
    bot.send_message(message.chat.id, f"{HELP}")


@bot.message_handler(regexp="Добавить напоминание о Дне Рождения")
def add_event(message: Message) -> None:
    if not is_user_in_database(message.chat.id):
        user = User(
            name=message.chat.first_name,
            chat_id=message.chat.id,
        )
        insert_user(user)
    bot.send_message(message.chat.id, "Введите имя именинника", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, input_birthday_human)


def input_birthday_human(message: Message) -> None:
    birthday_human = message.text
    message = bot.send_message(
        message.chat.id,
        """Введите дату рождения в формате <ДД.ММ.ГГГГ>
        Если Вы не знаете год рождения, введите четыре нуля <ДД.ММ.0000>""",
    )
    bot.register_next_step_handler(message, input_birthday_human_date, birthday_human)


def input_birthday_human_date(message: Message, birthday_human: str) -> None:
    birthday_human_date = message.text
    alert_markup = create_alert_markup()
    main_markup = create_main_markup()
    if is_str_date(birthday_human_date) is False:
        bot.send_message(
            message.chat.id,
            "Неверный формат ввода даты! Используйте формат: <ДД.ММ.ГГГГ>",
            reply_markup=main_markup,
        )
    else:
        bot.send_message(
            message.chat.id,
            "Выберете за сколько дней Вам напомнить о Дне Рождения!",
            reply_markup=alert_markup,
        )
        bot.register_next_step_handler(message, input_alert_date, birthday_human, birthday_human_date)


def input_alert_date(message: Message, birthday_human: str, birthday_human_date: str) -> None:
    time_markup = create_time_markup()
    alert_date_str = message.text
    bot.send_message(message.chat.id, "Выберите время оповещения о Дне Рождения:", reply_markup=time_markup)
    bot.register_next_step_handler(message, input_alert_time, birthday_human, birthday_human_date, alert_date_str)


def input_alert_time(message: Message, birthday_human: str, birthday_human_date: str, alert_date_str: str) -> None:
    alert_time_str = message.text
    birthday_day, birthday_month, birthday_year = birthday_human_date.split(".")
    alert_date = create_alert_date(alert_date_str, int(birthday_day), int(birthday_month))
    alert_time = create_alert_time(alert_time_str)
    event = insert_event(
        message.chat.id, birthday_human, int(birthday_day),
        int(birthday_month), int(birthday_year), alert_date, alert_time,
    )
    main_markup = create_main_markup()
    bot.send_message(
        message.chat.id,
        f"Добавлено напоминание о Дне Рождения {event.birthday_human.title()} {event.str_birthday_date()}",
    )
    bot.send_message(
        message.chat.id,
        f"Я напомню Вам об этом событии {event.str_alert_datetime()}",
        reply_markup=main_markup,
    )


@bot.message_handler(regexp="Ближайшие Дни Рождения")
def send_upcoming_birthdays(message: Message) -> None:
    events = get_coming_event(message.chat.id)
    main_markup = create_main_markup()
    if not is_user_in_database(message.chat.id):
        user = User(
            name=message.chat.first_name,
            chat_id=message.chat.id,
        )
        insert_user(user)
    if events:
        for event in events:
            bot.send_message(
                message.chat.id,
                f"{event.birthday_human.title()} - {event.str_birthday_date()}", reply_markup=ReplyKeyboardRemove(),
            )
        bot.send_message(message.chat.id, "Ближайшие Дни Рождения ⬆️", reply_markup=main_markup)
    else:
        bot.send_message(message.chat.id, "Нет добавленных Дней Рождения!", reply_markup=main_markup)


@bot.message_handler(regexp="Изменить напоминание")
def change_event(message: Message) -> None:
    if not is_user_in_database(message.chat.id):
        user = User(
            name=message.chat.first_name,
            chat_id=message.chat.id,
        )
        insert_user(user)
    change_event_markup = create_change_event_markup()
    bot.send_message(message.chat.id, "Выберите что Вы хотите изменить:", reply_markup=change_event_markup)
    bot.register_next_step_handler(message, input_change_birthday_human)


def input_change_birthday_human(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        "Введите имя именника, напоминание о котором Вы хотите изменить", reply_markup=ReplyKeyboardRemove(),
    )
    if message.text == "Изменить дату Рождения":
        bot.register_next_step_handler(message, change_event_date_step_one)
    elif message.text == "Изменить дату оповещения":
        bot.register_next_step_handler(message, change_alert_date_step_one)
    elif message.text == "Изменить время оповещения":
        bot.register_next_step_handler(message, change_alert_time_step_one)


def change_event_date_step_one(message: Message) -> None:
    birthday_human = message.text.lower()
    main_markup = create_main_markup()
    user_id = get_user_id(message.chat.id)
    if is_event_in_database(message.chat.id, birthday_human) and user_id:
        message = bot.send_message(
            message.chat.id,
            """Введите дату рождения в формате <ДД.ММ.ГГГГ>
            Если Вы не знаете год рождения, введите четыре нуля <ДД.ММ.0000>""",
        )
        bot.register_next_step_handler(message, change_event_date_step_two, birthday_human, user_id)
    else:
        bot.send_message(message.chat.id, f"Именинник {birthday_human.title()} не найден!", reply_markup=main_markup)


def change_event_date_step_two(message: Message, birthday_human: str, user_id: int) -> None:
    birthday_human_date = message.text
    birthday_day, birthday_month, birthday_year = birthday_human_date.split(".")
    main_markup = create_main_markup()
    if is_str_date(birthday_human_date) is False:
        bot.send_message(
            message.chat.id,
            "Неверный формат ввода даты! Используйте формат: <ДД.ММ.ГГГГ>",
            reply_markup=main_markup,
        )
    else:
        new_event = change_birthday_date(
            user_id, birthday_human, int(birthday_day), int(birthday_month), int(birthday_year)
        )
        if new_event:
            bot.send_message(
                message.chat.id,
                f"Добавлено напоминание о Дне Рождения {new_event.birthday_human.title()} {new_event.str_birthday_date()}",
                reply_markup=main_markup
            )


def change_alert_date_step_one(message: Message) -> None:
    birthday_human = message.text.lower()
    user_id = get_user_id(message.chat.id)
    if is_event_in_database(message.chat.id, birthday_human) and user_id:
        alert_markup = create_alert_markup()
        bot.send_message(
                message.chat.id,
                "Выберете за сколько дней Вам напомнить о Дне Рождения!",
                reply_markup=alert_markup,
            )
        bot.register_next_step_handler(message, change_alert_date_step_two, birthday_human, user_id)
    else:
        main_markup = create_main_markup()
        bot.send_message(message.chat.id, f"Именинник {birthday_human.title()} не найден!", reply_markup=main_markup)


def change_alert_date_step_two(message: Message, birthday_human: str, user_id: int) -> None:
    alert_date_str = message.text
    event = get_event(user_id, birthday_human)
    main_markup = create_main_markup()
    if event:
        alert_date = create_alert_date(alert_date_str, event.birthday_day, event.birthday_month)
        new_event = change_alert_date(user_id, birthday_human, alert_date)
        if new_event:
            bot.send_message(
                    message.chat.id,
                    f"Напоминание об этом событии изменено, теперь я напомню Вам {new_event.str_alert_datetime()}",
                    reply_markup=main_markup,
                )


def change_alert_time_step_one(message: Message) -> None:
    birthday_human = message.text.lower()
    user_id = get_user_id(message.chat.id)
    if is_event_in_database(message.chat.id, birthday_human) and user_id:
        time_markup = create_time_markup()
        bot.send_message(message.chat.id, "Выберите время оповещения о Дне Рождения:", reply_markup=time_markup)
        bot.register_next_step_handler(message, change_alert_time_step_two, birthday_human, user_id)
    else:
        main_markup = create_main_markup()
        bot.send_message(message.chat.id, f"Именинник {birthday_human.title()} не найден!", reply_markup=main_markup)


def change_alert_time_step_two(message: Message, birthday_human: str, user_id: int) -> None:
    alert_time_str = message.text
    alert_time = create_alert_time(alert_time_str)
    new_event = change_alert_time(user_id, birthday_human, alert_time)
    main_markup = create_main_markup()
    if new_event:
        bot.send_message(
                message.chat.id,
                f"Напоминание об этом событии изменено, теперь я напомню Вам {new_event.str_alert_datetime()}",
                reply_markup=main_markup,
            )


@bot.message_handler(regexp="Удалить напоминание")
def delete_alert(message: Message) -> None:
    if not is_user_in_database(message.chat.id):
        user = User(
            name=message.chat.first_name,
            chat_id=message.chat.id,
        )
        insert_user(user)
    bot.send_message(
        message.chat.id,
        "Введите имя именинника, напоминание о Дне Рождения которого, Вы хотите удалить:",
        reply_markup=ReplyKeyboardRemove(),
    )
    bot.register_next_step_handler(message, input_birthday_human_for_delete)


def input_birthday_human_for_delete(message: Message) -> None:
    birthday_human = message.text.lower()
    delete_event(message.chat.id, birthday_human)
    main_markup = create_main_markup()
    bot.send_message(
        message.chat.id,
        f"Напоминание о Дне Рождения именинника: {birthday_human.title()}, удалено!",
        reply_markup=main_markup,
    )


def alert_today() -> None:
    events = get_events_with_alert_today()
    if events:
        for event in events:
            user = get_user(event.user_id)
            if user:
                alert_message = f"""{user.name.title()},
                                    Напоминаю, День рождение у {event.birthday_human} {event.str_birthday_date()}
                                    {event.str_birhday_human_age()}"""
                schedule.every().day.at(event.alert_time.strftime("%H:%M")).do(send_alert, user.chat_id, alert_message)


def send_alert(chat_id: int, alert_message: str) -> Type[schedule.CancelJob]:
    main_markup = create_main_markup()
    bot.send_message(chat_id, alert_message, reply_markup=main_markup)
    return schedule.CancelJob


def schedule_checker() -> None:
    while True:
        schedule.run_pending()
        time.sleep(60)


def main() -> None:
    bot.enable_save_next_step_handlers(delay=2)

    bot.load_next_step_handlers()

    bot.infinity_polling()


if __name__ == "__main__":
    threading.Thread(target=main, name='bot_infinity_polling', daemon=True).start()
    threading.Thread(target=schedule_checker).start()
    schedule.every().day.at("00:01").do(alert_today)
