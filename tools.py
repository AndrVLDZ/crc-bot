from db import check_user_id
from aiogram.types import Message

async def check_user(message: Message) -> bool:
    user_id = message.from_user.id
    if not await check_user_id(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
        )
        return False
    return True
