from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from birthday_bot.db.config import get_config, get_connection_dsn
from birthday_bot.db.models.user_and_event import Base


def connect_db() -> tuple[Engine, Session]:
    db = create_engine(get_connection_dsn(get_config()), echo=True)
    Base.metadata.create_all(db)
    session = Session(db)
    return db, session
