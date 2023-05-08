from conftest import (
    get_user_from_test_db, user, event, get_db_session, delete_user_from_test_db,
    is_event_in_test_db, delete_event_from_test_db, get_event_from_test_db, insert_test_event,
)
from birthday_bot.db.utils_db import (
    insert_user, insert_event, get_event, get_coming_event, get_user_id,
    change_birthday_date, change_alert_date, change_alert_time, delete_event,
    get_events_with_alert_today, get_user, is_user_in_database, is_event_in_database,
)
from datetime import date, time


def test_insert_user_in_db(get_db_session, user):
    insert_user(user)
    getting_user_name = get_user_from_test_db(get_db_session, user.name).name
    getting_user_chat_id = get_user_from_test_db(get_db_session, user.name).chat_id
    delete_user_from_test_db(get_db_session, user)
    assert user.name == getting_user_name
    assert user.chat_id == getting_user_chat_id


def test_insert_event_in_db(get_db_session, user, event):
    insert_user(user)
    adding_event = insert_event(
        chat_id=user.chat_id,
        birthday_human=event.birthday_human,
        birthday_day=event.birthday_day,
        birthday_month=event.birthday_month,
        birthday_year=event.birthday_year,
        alert_date=event.alert_date,
        alert_time=event.alert_time,
    )
    event_from_test_db = get_event_from_test_db(get_db_session, event)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)
    assert event_from_test_db.birthday_human == event.birthday_human


def test_get_event(get_db_session, user, event):
    insert_user(user)
    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    adding_event = insert_event(
        chat_id=user.chat_id,
        birthday_human=event.birthday_human,
        birthday_day=event.birthday_day,
        birthday_month=event.birthday_month,
        birthday_year=event.birthday_year,
        alert_date=event.alert_date,
        alert_time=event.alert_time,
    )
    getting_exist_event = get_event(user_id=getting_user_id, birthday_human=adding_event.birthday_human)
    getting_not_exist_event = get_event(user_id=getting_user_id, birthday_human="not_exist")
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)
    assert getting_exist_event.birthday_human == adding_event.birthday_human
    assert getting_not_exist_event == None


def test_get_coming_event(get_db_session, user, event):
    # insert_user(user)
    # getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    # adding_event = insert_event(
    #     chat_id=user.chat_id,
    #     birthday_human=event.birthday_human,
    #     birthday_day=event.birthday_day,
    #     birthday_month=event.birthday_month,
    #     birthday_year=event.birthday_year,
    #     alert_date=event.alert_date,
    #     alert_time=event.alert_time,
    # )
    # getting_exist_event = get_event(user_id=getting_user_id, birthday_human=adding_event.birthday_human)
    # getting_not_exist_event = get_event(user_id=getting_user_id, birthday_human="not_exist")
    # delete_event_from_test_db(get_db_session, event)
    # delete_user_from_test_db(get_db_session, user)
    # assert getting_exist_event.birthday_human == adding_event.birthday_human
    # assert getting_not_exist_event == None
    assert True


def test_get_user_id(get_db_session, user, event):
    insert_user(user)
    adding_event = insert_event(
        chat_id=user.chat_id,
        birthday_human=event.birthday_human,
        birthday_day=event.birthday_day,
        birthday_month=event.birthday_month,
        birthday_year=event.birthday_year,
        alert_date=event.alert_date,
        alert_time=event.alert_time,
    )
    getting_user_id_from_test_db = get_user_from_test_db(get_db_session, user.name).id
    getting_exist_user_id = get_user_id(user.chat_id)
    getting_not_exist_user_id = get_user_id(123)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)
    assert getting_exist_user_id == getting_user_id_from_test_db
    assert getting_not_exist_user_id == None


def test_change_birthday_date(get_db_session, user, event):
    insert_user(user)
    adding_event = insert_event(
        chat_id=user.chat_id,
        birthday_human=event.birthday_human,
        birthday_day=event.birthday_day,
        birthday_month=event.birthday_month,
        birthday_year=event.birthday_year,
        alert_date=event.alert_date,
        alert_time=event.alert_time,
    )
    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    getting_change_event_exist_test_db = change_birthday_date(
        user_id=getting_user_id, birthday_human=event.birthday_human, 
        birthday_day=2,
        birthday_month=2,
        birthday_year=1999,
    )
    getting_change_event_not_exist_test_db = change_birthday_date(
        user_id=(getting_user_id + 1), birthday_human=event.birthday_human, 
        birthday_day=2,
        birthday_month=2,
        birthday_year=1999,
    )
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)
    assert getting_change_event_exist_test_db.birthday_human == event.birthday_human
    assert getting_change_event_exist_test_db.birthday_day == 2
    assert getting_change_event_exist_test_db.birthday_month == 2
    assert getting_change_event_exist_test_db.birthday_year == 1999
    assert getting_change_event_not_exist_test_db == None


def test_change_alert_date(get_db_session, user, event):
    insert_user(user)
    adding_event = insert_event(
        chat_id=user.chat_id,
        birthday_human=event.birthday_human,
        birthday_day=event.birthday_day,
        birthday_month=event.birthday_month,
        birthday_year=event.birthday_year,
        alert_date=event.alert_date,
        alert_time=event.alert_time,
    )
    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    getting_change_event_exist_test_db = change_alert_date(
        user_id=getting_user_id, birthday_human=event.birthday_human,
        alert_date=date(2000, 1, 2),
    )
    getting_change_event_not_exist_test_db = change_alert_date(
        user_id=(getting_user_id + 1), birthday_human=event.birthday_human,
        alert_date=date(2000, 1, 2),
    )
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)
    assert getting_change_event_exist_test_db.birthday_human == event.birthday_human
    assert getting_change_event_exist_test_db.alert_date == date(2000, 1, 2)
    assert getting_change_event_not_exist_test_db == None
