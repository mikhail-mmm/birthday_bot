from birthday_bot.db.config import get_config, get_connection_dsn
from tests.db.conftest import config_test_db


def test_get_config(config_test_db):
    assert get_config() == config_test_db


def test_get_connection_dsn(config_test_db):
    assert get_connection_dsn(config_test_db) == (
        f"postgresql://{config_test_db['POSTGRES_USER']}:{config_test_db['POSTGRES_PASSWORD']}@"
        f"{config_test_db['POSTGRES_HOST']}:{config_test_db['POSTGRES_PORT']}/{config_test_db['POSTGRES_DBNAME']}"
    )