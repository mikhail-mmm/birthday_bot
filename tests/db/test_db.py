from conftest import (
    get_user_from_test_db, user, event, get_db_session, delete_user_from_test_db,
    is_event_in_test_db, delete_event_from_test_db, get_event_from_test_db, insert_test_event,
    insert_test_user,
)
from birthday_bot.db.utils_db import (
    insert_user, insert_event, get_event, get_coming_event, get_user_id,
    change_birthday_date, change_alert_date, change_alert_time, delete_event,
    get_events_with_alert_today, get_user, is_user_in_database, is_event_in_database,
    change_event_alert_date_because_new_year,
)
from birthday_bot.db.models.user_and_event import Event
from datetime import date, time



def test_insert_user_in_db(get_db_session, user):
    insert_user(user)

    getting_user_name = get_user_from_test_db(get_db_session, user.name).name
    getting_user_chat_id = get_user_from_test_db(get_db_session, user.name).chat_id
    delete_user_from_test_db(get_db_session, user)

    assert user.name == getting_user_name
    assert user.chat_id == getting_user_chat_id


def test_insert_event_in_db(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    adding_event = insert_event(
        chat_id=user.chat_id,
        birthday_human=event.birthday_human,
        birthday_day=event.birthday_day,
        birthday_month=event.birthday_month,
        birthday_year=event.birthday_year,
        alert_date=event.alert_date,
        alert_time=event.alert_time,
    )

    event_from_test_db = get_event_from_test_db(get_db_session, event.birthday_human)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)

    assert event_from_test_db.birthday_human == event.birthday_human


def test_get_event(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    getting_exist_event = get_event(user_id=getting_user_id, birthday_human=event.birthday_human)
    getting_not_exist_event = get_event(user_id=getting_user_id, birthday_human="not_exist")
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)

    assert getting_exist_event.birthday_human == event.birthday_human
    assert getting_not_exist_event == None


def test_get_coming_event(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    event_exist_in_test_db = get_coming_event(user.chat_id)
    event_not_exist_in_test_db = get_coming_event(user.chat_id + 1)

    new_event_first = Event(
        birthday_human="test",
        birthday_day=2,
        birthday_month=2,
        birthday_year=1999,
        alert_date=date(date.today().year, 2, 2),
        alert_time=time(10, 0),
        user=user,
    )
    new_event_second = Event(
        birthday_human="test_2",
        birthday_day=3,
        birthday_month=3,
        birthday_year=2001,
        alert_date=date(date.today().year, 3, 2),
        alert_time=time(15, 0),
        user=user,
    )
    insert_test_event(get_db_session, new_event_first)
    insert_test_event(get_db_session, new_event_second)
    events_exist_in_test_db = get_coming_event(user.chat_id)
    
    delete_event_from_test_db(get_db_session, event)
    delete_event_from_test_db(get_db_session, new_event_first)
    delete_event_from_test_db(get_db_session, new_event_second)
    delete_user_from_test_db(get_db_session, user)

    assert event_exist_in_test_db[0].birthday_human == event.birthday_human
    assert events_exist_in_test_db[0].birthday_human == event.birthday_human
    assert events_exist_in_test_db[1].birthday_human == new_event_first.birthday_human
    assert events_exist_in_test_db[2].birthday_human == new_event_second.birthday_human
    assert event_not_exist_in_test_db == []


def test_get_user_id(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_user_id_from_test_db = get_user_from_test_db(get_db_session, user.name).id
    getting_exist_user_id = get_user_id(user.chat_id)
    getting_not_exist_user_id = get_user_id(123)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)

    assert getting_exist_user_id == getting_user_id_from_test_db
    assert getting_not_exist_user_id == None


def test_change_birthday_date(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

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
    delete_event_from_test_db(get_db_session, getting_change_event_exist_test_db)
    delete_user_from_test_db(get_db_session, user)

    assert getting_change_event_exist_test_db.birthday_human == event.birthday_human
    assert getting_change_event_exist_test_db.birthday_day == 2
    assert getting_change_event_exist_test_db.birthday_month == 2
    assert getting_change_event_exist_test_db.birthday_year == 1999
    assert getting_change_event_not_exist_test_db == None


def test_change_alert_date(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    getting_change_event_exist_test_db = change_alert_date(
        user_id=getting_user_id, birthday_human=event.birthday_human,
        alert_date=date(2000, 1, 2),
    )
    getting_change_event_not_exist_test_db = change_alert_date(
        user_id=(getting_user_id + 1), birthday_human=event.birthday_human,
        alert_date=date(2000, 1, 2),
    )
    delete_event_from_test_db(get_db_session, getting_change_event_exist_test_db)
    delete_user_from_test_db(get_db_session, user)

    assert getting_change_event_exist_test_db.birthday_human == event.birthday_human
    assert getting_change_event_exist_test_db.alert_date == date(2000, 1, 2)
    assert getting_change_event_not_exist_test_db == None


def test_change_alert_time(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    getting_change_event_exist_test_db = change_alert_time(
        user_id=getting_user_id, birthday_human=event.birthday_human,
        alert_time=time(10, 0),
    )
    getting_change_event_not_exist_test_db = change_alert_time(
        user_id=(getting_user_id + 1), birthday_human=event.birthday_human,
        alert_time=time(10, 0),
    )
    delete_event_from_test_db(get_db_session, getting_change_event_exist_test_db)
    delete_user_from_test_db(get_db_session, user)

    assert getting_change_event_exist_test_db.birthday_human == event.birthday_human
    assert getting_change_event_exist_test_db.alert_time == time(10, 0)
    assert getting_change_event_not_exist_test_db == None


def test_delete_event(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    delete_event(chat_id=user.chat_id, birthday_human=event.birthday_human)
    delete_user_from_test_db(get_db_session, user)

    assert is_event_in_test_db(get_db_session, getting_user_id) == False


def test_get_events_with_alert_today(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_events_with_alert_today_not_exist_in_test_db = get_events_with_alert_today()
    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    getting_change_event_exist_test_db = change_alert_date(
        user_id=getting_user_id, birthday_human=event.birthday_human,
        alert_date=date.today(),
    )
    getting_events_with_alert_today_exist_in_test_db = get_events_with_alert_today()

    delete_event_from_test_db(get_db_session, getting_change_event_exist_test_db)
    delete_user_from_test_db(get_db_session, user)

    assert getting_events_with_alert_today_not_exist_in_test_db == None
    assert getting_events_with_alert_today_exist_in_test_db[0].birthday_human == event.birthday_human


def test_get_user(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    getting_user_id = get_user_from_test_db(get_db_session, user.name).id
    user_exist_test_db = get_user(getting_user_id)
    user_not_exist_test_db = get_user(getting_user_id + 1)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)

    assert user_exist_test_db.name == user.name
    assert user_not_exist_test_db == None


def test_is_user_in_database(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    user_exist_in_test_db = is_user_in_database(user.chat_id)
    user_not_exist_in_test_db = is_user_in_database(user.chat_id + 1)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)

    assert user_exist_in_test_db == True
    assert user_not_exist_in_test_db == False


def test_is_event_in_database(get_db_session, user, event):
    insert_test_user(get_db_session, user)
    insert_test_event(get_db_session, event)

    event_exist_in_test_db = is_event_in_database(chat_id=user.chat_id, birthday_human=event.birthday_human)
    event_not_exist_in_test_db = is_event_in_database(chat_id=user.chat_id + 1, birthday_human=event.birthday_human)
    delete_event_from_test_db(get_db_session, event)
    delete_user_from_test_db(get_db_session, user)

    assert event_exist_in_test_db == True
    assert event_not_exist_in_test_db == False


def test_change_event_alert_date_because_new_year(get_db_session, user):
    insert_test_user(get_db_session, user)
    test_event_1 = Event(
        birthday_human="test",
        birthday_day=2,
        birthday_month=2,
        birthday_year=2000,
        alert_date=date(date.today().year, 2, 2),
        alert_time=time(10, 0),
        user=user,
    )
    test_event_2 = Event(
        birthday_human="test_2",
        birthday_day=12,
        birthday_month=12,
        birthday_year=2000,
        alert_date=date(date.today().year, 12, 12),
        alert_time=time(15, 0),
        user=user,
    )
    insert_test_event(get_db_session, test_event_1)
    insert_test_event(get_db_session, test_event_2)

    getting_user_id = get_user_id(user.chat_id)
    change_event_alert_date_because_new_year()
    changing_event = get_event(user_id=getting_user_id, birthday_human=test_event_1.birthday_human)
    not_changing_event = get_event(user_id=getting_user_id, birthday_human=test_event_2.birthday_human)

    delete_event_from_test_db(get_db_session, test_event_1)
    delete_event_from_test_db(get_db_session, test_event_2)
    delete_user_from_test_db(get_db_session, user)

    assert changing_event.alert_date == date(2024, 2, 2)
    assert not_changing_event.alert_date == date(2023, 12, 12)
