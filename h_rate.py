from qiwi import get_rate
from tools import check_user
from db import get_from, get_to
from aiogram import F, Router
from aiogram.types import Message
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message(F.text == "Rate")
async def rate(message: Message) -> DeleteMessage:
    if await check_user(message):
        user_id = message.from_user.id
        rate = await get_rate(user_id)
        if not rate: 
            await message.answer(
                "Set different currencies!",
            )
        else:
            currency_from = await get_from(user_id)
            currency_to = await get_to(user_id)
            if currency_from != currency_to:
                await message.answer(
                    f"**1 {currency_to}  ==  `{rate}` {currency_from} ",
                    parse_mode="Markdown",
                )
    # removing user input for better readability of rate responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
