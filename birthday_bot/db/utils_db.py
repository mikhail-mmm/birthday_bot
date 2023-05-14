from datetime import date, time
from sqlalchemy import select
from typing import Optional

from birthday_bot.db.db_creation import connect_db
from birthday_bot.db.models.user_and_event import Event, User

DB, SESSION = connect_db()


def insert_user(user: User) -> None:
    SESSION.add(user)
    SESSION.commit()


def insert_event(
        chat_id: int, birthday_human: str, birthday_day: int,
        birthday_month: int, birthday_year: int, alert_date: date,
        alert_time: time,
) -> Event:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    event = Event(
        birthday_human=birthday_human.lower(),
        birthday_day=int(birthday_day),
        birthday_month=int(birthday_month),
        birthday_year=int(birthday_year),
        alert_date=alert_date,
        alert_time=alert_time,
        user=user,
    )
    SESSION.add(event)
    SESSION.commit()
    return event


def get_event(user_id: int, birthday_human: str) -> Optional[Event]:
    event = SESSION.scalar(select(Event).where(Event.user_id == user_id).where(Event.birthday_human == birthday_human))
    if event:
        return event
    return None


def get_coming_event(chat_id: int) -> Optional[list[Event]]:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    if user:
        amount_events = len(user.events)
        if amount_events >= 3:
            coming_birthdays = 3
        else:
            coming_birthdays = amount_events
        events = SESSION.query(Event).where(Event.user_id == user.id).order_by(Event.birthday_month).order_by(Event.birthday_day).limit(coming_birthdays).all()
        return events
    events = []
    return events


def get_user_id(chat_id: int) -> Optional[int]:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    if user:
        return user.id
    return None


def change_birthday_date(user_id: int, birthday_human: str, birthday_day: int, birthday_month: int, birthday_year: int) -> Optional[Event]:
    row = SESSION.scalars(select(Event).where(Event.user_id == user_id).where(Event.birthday_human == birthday_human)).first()
    if row:
        row.birthday_day = birthday_day
        row.birthday_month = birthday_month
        row.birthday_year = birthday_year
        SESSION.commit()
        return row
    return None


def change_alert_date(user_id: int, birthday_human: str, alert_date: date) -> Optional[Event]:
    row = SESSION.scalars(select(Event).where(Event.user_id == user_id).where(Event.birthday_human == birthday_human)).first()
    if row:
        row.alert_date = alert_date
        SESSION.commit()
        return row
    return None


def change_alert_time(user_id: int, birthday_human: str, alert_time: time) -> Optional[Event]:
    row = SESSION.scalars(select(Event).where(Event.user_id == user_id).where(Event.birthday_human == birthday_human)).first()
    if row:
        row.alert_time = alert_time
        SESSION.commit()
        return row
    return None


def delete_event(chat_id: int, birthday_human: str) -> None:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    if user:
        SESSION.query(Event).where(Event.user_id == user.id).where(Event.birthday_human == birthday_human).delete()
        SESSION.commit()


def get_events_with_alert_today() -> Optional[list[Event]]:
    events = SESSION.query(Event).where(Event.alert_date == date.today()).all()
    return events if events else None


def get_user(id: int) -> Optional[User]:
    user = SESSION.query(User).get(id)
    if user:
        return user
    return None


def is_user_in_database(chat_id: int) -> bool:
    if SESSION.query(User).filter_by(chat_id=chat_id).first() is not None:
        return True
    return False


def is_event_in_database(chat_id: int, birthday_human: str) -> bool:
    user = SESSION.scalars(select(User).where(User.chat_id == chat_id)).first()
    if user:
        if SESSION.query(Event).filter_by(user_id=user.id).filter_by(birthday_human=birthday_human).first() is not None:
            return True
    return False
