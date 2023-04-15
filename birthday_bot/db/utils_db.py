from datetime import date, datetime

from db.db_creation import connect_db
from db.db_model import User, Event

from sqlalchemy import select, delete, desc
from sqlalchemy.exc import OperationalError

DB, SESSION = connect_db()


def insert_user(user: User) -> User:
    SESSION.add(user)
    SESSION.commit()


def insert_event(
        chat_id: int, birthday_human: str, birthday_day: int,
        birthday_month: int, birthday_year: int, alert_datetime: datetime,
) -> Event:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    event = Event(
        birthday_human=birthday_human.lower(),
        birthday_day=int(birthday_day),
        birthday_month=int(birthday_month),
        birthday_year=int(birthday_year),
        alert_datetime=alert_datetime,
        user=user
    )
    SESSION.add(event)
    SESSION.commit()
    return event


def get_coming_event(chat_id: int) -> list[Event]:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    amount_events = len(user.events)
    if amount_events >=3:
        coming_birthdays = 3
    else:
        coming_birthdays = amount_events
    events = SESSION.query(Event).where(Event.user_id == user.id).order_by(Event.birthday_month).order_by(Event.birthday_day).limit(coming_birthdays).all()
    return events


def get_birthday_date(chat_id: int, birthday_human: str, geting_alert_date_str: bool = False, geting_alert_time_str: bool = False) -> tuple[int, str]:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    row = SESSION.scalars(select(Event).where(Event.user_id == user.id).where(Event.birthday_human == birthday_human)).first()
    alert_time_str = row.alert_datetime.strftime("%H:%M")
    alert_date_str = row.alert_datetime.strftime("%d.%m.%Y")
    if geting_alert_date_str:
        return row.birthday_day, row.birthday_month, alert_date_str
    elif geting_alert_time_str:
        return row.birthday_day, row.birthday_month, alert_time_str


def change_birthday_date(chat_id: int, birthday_human: str, birthday_day: int, birthday_month: int, birthday_year: int) -> Event | None:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    row = SESSION.scalars(select(Event).where(Event.user_id == user.id).where(Event.birthday_human == birthday_human)).first()
    row.birthday_day = birthday_day
    row.birthday_month = birthday_month
    row.birthday_year = birthday_year
    SESSION.commit()
    return row


def change_alert_datetime(chat_id: int, birthday_human: str, alert_datetime: datetime) -> Event:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    row = SESSION.scalars(select(Event).where(Event.user_id == user.id).where(Event.birthday_human == birthday_human)).first()
    row.alert_datetime = alert_datetime
    SESSION.commit()
    return row


def delete_event(chat_id: int, birthday_human: str) -> None:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    SESSION.query(Event).where(Event.user_id == user.id).where(Event.birthday_human == birthday_human).delete()
    SESSION.commit()


def is_user_in_database(chat_id: int) -> bool:
    if SESSION.query(User).filter_by(chat_id=chat_id).first() is not None:
        return True
    return False


def is_event_in_database(chat_id: int, birthday_human: str) -> bool:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    if SESSION.query(Event).filter_by(user_id=user.id).filter_by(birthday_human=birthday_human).first() is not None:
        return True
    return False