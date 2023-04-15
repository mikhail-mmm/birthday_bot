from db.config import get_config, get_connection_dsn
from db.db_model import Base

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session


def connect_db() -> tuple[Engine, Session]:
    db = create_engine(get_connection_dsn(get_config()), echo=True)
    Base.metadata.create_all(db)
    session = Session(db)
    return db, session
