from conftest import (
    get_user_from_test_db, user, event, get_db_session, delete_user_from_test_db,
    is_event_in_test_db, delete_event_from_test_db,
)
from birthday_bot.db.utils_db import insert_user, insert_event


def test_insert_user_in_db(get_db_session, user):
    insert_user(user)
    assert user.name == get_user_from_test_db(get_db_session, user.name).name
    assert user.chat_id == get_user_from_test_db(get_db_session, user.name).chat_id


# def test_insert_event_in_db(get_db_session, user, event):
#     adding_event = insert_event(
#         chat_id=user.chat_id,
#         birthday_human=event.birthday_human,
#         birthday_day=event.birthday_day,
#         birthday_month=event.birthday_month,
#         birthday_year=event.birthday_year,
#         alert_date=event.alert_date,
#         alert_time=event.alert_time,
#     ) 
#     assert adding_event.birthday_human == event.birthday_human
#     assert is_event_in_test_db(get_db_session, user.id)
#     # delete_user_from_test_db(get_db_session, user.name)
#     # delete_event_from_test_db(get_db_session, user.name)
