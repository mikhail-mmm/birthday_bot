from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, kw_only=True)
class BirthdayHuman:
    birthday_human: str
    birthday_date: str


@dataclass(frozen=True, kw_only=True)
class UserTelegram:
    user_name: str
    chat_id: int