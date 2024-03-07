from typing import Union
from aiogram import Bot
from .get_token import get_secrets


def get_bot() -> Union[Bot, bool]:
    bot_token = get_secrets()
    if bot_token:
        bot = Bot(token=bot_token)
        return bot


if __name__ == "__main__":
    pass
else:
    bot = get_bot()
