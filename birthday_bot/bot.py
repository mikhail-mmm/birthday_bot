import logging

from db.utils_db import (insert_user, is_user_in_database, insert_event,
                         get_coming_event, change_birthday_date, change_alert_datetime,
                         get_birthday_date, is_event_in_database, delete_event)
from db.db_model import User

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove

from utils.settings import API_TOKEN
from utils.utils import (create_main_markup, create_alert_markup, create_time_markup,
                        is_str_date, create_alert_datetime, create_change_event_markup)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, filename="bot.log"
)
logger = logging.getLogger(__name__)

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
    main_markup = create_main_markup()
    bot.send_message(message.chat.id, 'Выберите что вам надо:', reply_markup=main_markup)


@bot.message_handler(regexp="Добавить напоминание о Дне Рождения")
def add_event(message: Message) -> None:
    bot.send_message(message.chat.id, "Введите имя именинника", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, input_birthday_human)


def input_birthday_human(message: Message) -> None:
    birthday_human = message.text
    message = bot.send_message(message.chat.id, "Введите дату рождения в формате <ДД.ММ.ГГГГ>\nЕсли Вы не знаете год рождения, введите четыре нуля <ДД.ММ.0000>")
    bot.register_next_step_handler(message, input_birthday_human_date, birthday_human)


def input_birthday_human_date(message: Message, birthday_human: str) -> None:
    birthday_human_date = message.text
    alert_markup = create_alert_markup()
    main_markup = create_main_markup()
    if is_str_date(birthday_human_date) == False:
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
    alert_datetime = create_alert_datetime(alert_date_str, alert_time_str, int(birthday_day), int(birthday_month))
    event = insert_event(
        message.chat.id, birthday_human, int(birthday_day),
        int(birthday_month), int(birthday_year), alert_datetime,
    )
    main_markup = create_main_markup()
    bot.send_message(message.chat.id, f"Добавлено напоминание о Дне Рождения {event.birthday_human.title()} {birthday_day}.{birthday_month}")
    bot.send_message(message.chat.id, 
        f"Я напомню Вам об этом событии {event.alert_datetime.strftime('%d.%m.%Y')} в {event.alert_datetime.strftime('%H:%M')}",
        reply_markup=main_markup,
    )


@bot.message_handler(regexp="Ближайшие Дни Рождения")
def send_upcoming_birthdays(message: Message) -> None:
    events = get_coming_event(message.chat.id)
    main_markup = create_main_markup()
    for event in events:
        bot.send_message(message.chat.id, f"{event.birthday_human.title()} - {event.str_date()}", reply_markup=ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "Ближайшие Дни Рождения ⬆️", reply_markup=main_markup)


@bot.message_handler(regexp="Изменить напоминание")
def change_event(message: Message) -> None:
    change_event_markup = create_change_event_markup()
    bot.send_message(message.chat.id, "Выберите что Вы хотите изменить:", reply_markup=change_event_markup)
    bot.register_next_step_handler(message, input_change_birthday_human)


def input_change_birthday_human(message: Message) -> None:
    bot.send_message(message.chat.id, "Введите имя именника, напоминание о котором Вы хотите изменить", reply_markup=ReplyKeyboardRemove())
    if message.text == "Изменить дату Рождения":
        bot.register_next_step_handler(message, change_event_date_step_one)
    elif message.text == "Изменить дату оповещения":
        bot.register_next_step_handler(message, change_alert_date_step_one)
    elif message.text == "Изменить время оповещения":
        bot.register_next_step_handler(message, change_alert_time_step_one)


def change_event_date_step_one(message: Message) -> None:
    birthday_human = message.text.lower()
    main_markup = create_main_markup()
    if is_event_in_database(message.chat.id, birthday_human):
        message = bot.send_message(message.chat.id, "Введите дату рождения в формате <ДД.ММ.ГГГГ>\nЕсли Вы не знаете год рождения, введите четыре нуля <ДД.ММ.0000>")
        bot.register_next_step_handler(message, change_event_date_step_two, birthday_human)
    else:
        bot.send_message(message.chat.id, f"Именинник {birthday_human.capitalize()} не найден!", reply_markup=main_markup)


def change_event_date_step_two(message: Message, birthday_human: str) -> None:
    birthday_human_date = message.text
    birthday_day, birthday_month, birthday_year = birthday_human_date.split(".")
    main_markup = create_main_markup()
    if is_str_date(birthday_human_date) == False:
        bot.send_message(
            message.chat.id,
            "Неверный формат ввода даты! Используйте формат: <ДД.ММ.ГГГГ>",
            reply_markup=main_markup,
        )
    else:
        new_event = change_birthday_date(
            message.chat.id, birthday_human, int(birthday_day), int(birthday_month), int(birthday_year)
        )
        bot.send_message(
            message.chat.id,
            f"Добавлено напоминание о Дне Рождения {new_event.birthday_human.title()} {birthday_day}.{birthday_month}",
            reply_markup=main_markup
        )


def change_alert_date_step_one(message: Message) -> None:
    birthday_human = message.text.lower()
    if is_event_in_database(message.chat.id, birthday_human):
        alert_markup = create_alert_markup()
        bot.send_message(
                message.chat.id,
                "Выберете за сколько дней Вам напомнить о Дне Рождения!",
                reply_markup=alert_markup,
            )
        bot.register_next_step_handler(message, change_alert_date_step_two, birthday_human)
    else:
        main_markup = create_main_markup()
        bot.send_message(message.chat.id, f"Именинник {birthday_human.capitalize()} не найден!", reply_markup=main_markup)


def change_alert_date_step_two(message: Message, birthday_human: str) -> None:
    alert_date_str = message.text
    birthday_day, birthday_month, alert_time_str = get_birthday_date(message.chat.id, birthday_human, geting_alert_time_str=True)
    alert_datetime = create_alert_datetime(alert_date_str, alert_time_str, birthday_day, birthday_month)
    new_event = change_alert_datetime(message.chat.id, birthday_human, alert_datetime)
    main_markup = create_main_markup()
    bot.send_message(message.chat.id, 
        f"Напоминание об этом событии изменено, теперь я напомню Вам {new_event.alert_datetime.strftime('%d.%m.%Y')} в {new_event.alert_datetime.strftime('%H:%M')}",
        reply_markup=main_markup,
    )


def change_alert_time_step_one(message: Message) -> None:
    birthday_human = message.text.lower()
    if is_event_in_database(message.chat.id, birthday_human):
        time_markup = create_time_markup()
        bot.send_message(message.chat.id, "Выберите время оповещения о Дне Рождения:", reply_markup=time_markup)
        bot.register_next_step_handler(message, change_alert_time_step_two, birthday_human)
    else:
        main_markup = create_main_markup()
        bot.send_message(message.chat.id, f"Именинник {birthday_human.capitalize()} не найден!", reply_markup=main_markup)

    time_markup = create_time_markup()
    bot.send_message(message.chat.id, "Выберите время оповещения о Дне Рождения:", reply_markup=time_markup)
    bot.register_next_step_handler(message, change_alert_time_step_two, birthday_human)


def change_alert_time_step_two(message: Message, birthday_human: str) -> None:
    alert_time_str = message.text
    birthday_day, birthday_month, alert_date_str = get_birthday_date(message.chat.id, birthday_human, geting_alert_date_str=True)
    alert_datetime = create_alert_datetime(alert_date_str, alert_time_str, birthday_day, birthday_month)
    new_event = change_alert_datetime(message.chat.id, birthday_human, alert_datetime)
    main_markup = create_main_markup()
    bot.send_message(message.chat.id, 
        f"Напоминание об этом событии изменено, теперь я напомню Вам {new_event.alert_datetime.strftime('%d.%m.%Y')} в {new_event.alert_datetime.strftime('%H:%M')}",
        reply_markup=main_markup,
    )


@bot.message_handler(regexp="Удалить напоминание")
def delete_alert(message: Message) -> None:
    bot.send_message(message.chat.id, "Введите имя именинника, напоминание о Дне Рождения которого, Вы хотите удалить:", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, input_birthday_human_for_delete)


def input_birthday_human_for_delete(message: Message) -> None:
    birthday_human = message.text.lower()
    delete_event(message.chat.id, birthday_human)
    main_markup = create_main_markup()
    bot.send_message(message.chat.id, f"Напоминание о Дне Рождения именинника: {birthday_human.capitalize()}, удалено!", reply_markup=main_markup)


@bot.message_handler(commands=["help"], regexp="Справка")
def help(message: Message) -> None:
    bot.send_message(message.chat.id, "Справка")


def main() -> None:
    bot.enable_save_next_step_handlers(delay=2)

    bot.load_next_step_handlers()

    bot.infinity_polling()


if __name__ == "__main__":
    main()
