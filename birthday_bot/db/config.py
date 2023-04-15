import os

from typing import Mapping, Any


def get_connection_dsn(config: Mapping[str, Any]) -> str:
    return (
        f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}@"
        f"{config['POSTGRES_HOST']}:{config['POSTGRES_PORT']}/{config['POSTGRES_DBNAME']}"
    )


def get_config() -> Mapping[str, Any]:
    return {
        "POSTGRES_DBNAME": os.environ.get("POSTGRES_DBNAME", "birthday_bot"),
        "POSTGRES_HOST": os.environ.get("POSTGRES_HOST", "0.0.0.0"),
        "POSTGRES_PORT": int(os.environ.get("POSTGRES_PORT", 5432)),
        "POSTGRES_USER": os.environ.get("POSTGRES_USER", "username"),
        "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", "123123"),
    }
