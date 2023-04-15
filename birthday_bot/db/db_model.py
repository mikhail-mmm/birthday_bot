from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.schema import MetaData


class Base(DeclarativeBase):
    metadata = MetaData()


class User(Base):
    Base.metadata

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    events = relationship("Event", backref="user")

    id: Mapped[int]
    name: Mapped[str]
    chat_id: Mapped[int]
    events: Mapped[list["Event"]] = relationship("Event", backref="user")


class Event(Base):
    Base.metadata

    __tablename__ = "event"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    birthday_human = Column(String, nullable=False)
    birthday_day = Column(Integer, nullable=False)
    birthday_month = Column(Integer, nullable=False)
    birthday_year = Column(Integer, nullable=True)
    alert_datetime = Column(DateTime, nullable=False)

    id: Mapped[int]
    user_id: Mapped[int]
    birthday_human: Mapped[str]
    birthday_day: Mapped[int]
    birthday_month: Mapped[int]
    birthday_year: Mapped[int]
    alert_datetime: Mapped[datetime]

    def str_date(self):
        return f"{self.birthday_day}.{self.birthday_month}.{self.birthday_year}"
