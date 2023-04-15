def change_event_date(message: Message) -> None:
    birthday_human = message.text
    change_event_markup = create_change_event_markup()
    bot.send_message(
        message.chat.id,
        "Если Вы хотите изменить дату Дня Рождения, введите дату в формате <ДД.ММ.ГГГГ>\nЕсли Вы не знаете год рождения, введите четыре нуля <ДД.ММ.0000>. Если Вы хотите изменить только время и дату оповещения нажмите 'Пропустить этот шаг' ⬇️",
        reply_markup=change_event_markup,
    )
    bot.register_next_step_handler(message, change_event_alert_date, birthday_human)


def change_event_alert_date(message: Message, birthday_human: str) -> None:
    if message.text != "Пропустить этот шаг":
        birthday_human_date = message.text
        change_alert_markup = create_change_alert_markup()
        main_markup = create_main_markup()
        if is_str_date(birthday_human_date) == False:
            bot.send_message(
                message.chat.id,
                "Неверный формат ввода даты! Используйте формат: <ДД.ММ.ГГГГ>",
                reply_markup=main_markup,
            )
        else:
            birthday_human_date = None
            bot.send_message(
                message.chat.id,
                "Выберете за сколько дней Вам напомнить о Дне Рождения! Или Если Вы хотите изменить только время и дату оповещения нажмите 'Пропустить этот шаг' ⬇️",
                reply_markup=change_alert_markup,
            )
            bot.register_next_step_handler(message, change_event_alert_time, birthday_human, birthday_human_date)
    else:
        birthday_human_date = None
        bot.send_message(
            message.chat.id,
            "Выберете за сколько дней Вам напомнить о Дне Рождения! Или Если Вы хотите изменить только время и дату оповещения нажмите 'Пропустить этот шаг' ⬇️",
            reply_markup=change_alert_markup,
        )
        bot.register_next_step_handler(message, change_event_alert_time, birthday_human, birthday_human_date)



def change_event_alert_time(message: Message, birthday_human: str, birthday_human_date: str | None) -> None:
    if message.text != "Пропустить этот шаг":
        time_markup = create_time_markup()
        alert_different = message.text
        bot.send_message(message.chat.id, "Выберите время оповещения о Дне Рождения:", reply_markup=time_markup)
        bot.register_next_step_handler(message, input_alert_time, birthday_human, birthday_human_date, alert_different)
    else:
        time_markup = create_time_markup()
        alert_different = message.text
        bot.send_message(message.chat.id, "Выберите время оповещения о Дне Рождения:", reply_markup=time_markup)
        bot.register_next_step_handler(message, input_alert_time, birthday_human, birthday_human_date, alert_different)
