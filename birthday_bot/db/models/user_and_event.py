from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
from sqlalchemy.schema import MetaData


class Base(DeclarativeBase):
    metadata = MetaData()


class Base(DeclarativeBase):
    metadata = MetaData()


class User(Base):
    Base.metadata

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
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
    alert_date = Column(Date, nullable=False)
    alert_time = Column(Time, nullable=False)

    def str_birthday_date(self) -> str:
        if self.birthday_month < 10:
            return f"{self.birthday_day}.0{self.birthday_month}"
        else:
            return f"{self.birthday_day}.{self.birthday_month}"

    def str_alert_datetime(self) -> str:
        return f"{self.alert_date.strftime('%d.%m.%Y')} в {self.alert_time.strftime('%H:%M')}."

    def str_birhday_human_age(self) -> str:
        if self.birthday_year != 0:
            return f"Исполняется {date.today().year - self.birthday_year} год (лет)."
        else:
            return ""
