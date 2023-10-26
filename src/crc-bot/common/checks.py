from typing import Union

from aiogram.types import Message, User

from db import user_in_db
from .logs import log


async def get_first_name(message: Message) -> Union[str, bool]:
    if isinstance(message.from_user, User):
        return message.from_user.first_name
    log.info("First name not defined")
    return False


async def get_id(message: Message) -> int:
    if isinstance(message.from_user, User):
        return message.from_user.id
    log.info("User not defined")
    return False


async def check_user(message: Message) -> Union[bool, int]:
    telegram_user_id = await get_id(message)
    if telegram_user_id is not False:
        # if the user is not in the database
        if not await user_in_db(telegram_user_id):
            await message.answer(
                "Send `/start` command first!",
                parse_mode="Markdown"
            )
            return False
        # if the user is in the database
        return telegram_user_id
    return False
