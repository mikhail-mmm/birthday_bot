import pytest

from birthday_bot.db.models.user_and_event import Base, Event, User
from birthday_bot.db.config import get_connection_dsn

from datetime import date, time
from faker import Faker
from random import randint

from sqlalchemy import create_engine, Engine, select, delete
from sqlalchemy.orm import Session


@pytest.fixture
def config_test_db():
    return {
        "POSTGRES_DBNAME": "test_birthday_bot",
        "POSTGRES_HOST": "0.0.0.0",
        "POSTGRES_PORT": 5432,
        "POSTGRES_USER": "username",
        "POSTGRES_PASSWORD": "123321",
    }


@pytest.fixture
def get_db_session(config_test_db):
    db = create_engine(get_connection_dsn(config_test_db), echo=True)
    Base.metadata.create_all(db)
    session = Session(db)
    try:
        yield session
    finally:
        session.close()


def delete_user_from_test_db(session, user):
    session.query(User).where(User.name == user.name).delete()


def delete_event_from_test_db(session, id):
    session.query(Event).where(Event.id == id).delete()


def get_user_from_test_db(session, test_user_name):
    user = session.scalars(select(User).where(User.name == test_user_name)).first()
    return user


def is_event_in_test_db(session, user_id):
    event = session.scalar(select(Event).where(Event.user_id == user_id))
    if event:
        return True


@pytest.fixture
def user():
    faker = Faker()
    user = User(name=faker.name().lower(), chat_id=randint(100000, 999999))
    return user


@pytest.fixture
def event(user):
    faker = Faker()
    event = Event(
        birthday_human=faker.name().lower(),
        birthday_day=1,
        birthday_month=1,
        birthday_year=2000,
        alert_date=date(2000, 1, 1),
        alert_time=time(12, 00),
        user=user,
    )
    return event
